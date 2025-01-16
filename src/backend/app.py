from flask import Flask, request, jsonify
import logging
import os
import requests
from elasticsearch import Elasticsearch
from openai import OpenAI

# Configure logging
log_file_path = "/var/log/app.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file_path),  # Write logs to /var/log/app.log
        logging.StreamHandler()  # Also log to the console
    ]
)
logger = logging.getLogger(__name__)

# Flask app setup
app = Flask(__name__)


# Environment variables
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
ELASTIC_ENDPOINT = os.getenv("ELASTIC_ENDPOINT")
ELASTIC_API_KEY = os.getenv("ELASTIC_API_KEY")

# OpenTelemetry environment variables
OTEL_EXPORTER_OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
OTEL_EXPORTER_OTLP_HEADERS = os.getenv("OTEL_EXPORTER_OTLP_HEADERS", "")

# Parse OTEL_EXPORTER_OTLP_HEADERS into a dictionary if provided
if OTEL_EXPORTER_OTLP_HEADERS:
    otel_headers_dict = dict(
        item.split("=") for item in OTEL_EXPORTER_OTLP_HEADERS.split(",") if "=" in item
    )
else:
    otel_headers_dict = {}

# Validate environment variables
if not OPENAI_API_KEY or not ELASTIC_ENDPOINT or not ELASTIC_API_KEY:
    logger.error("Missing necessary environment configuration. Ensure all keys are set.")
    exit(1)

# Elasticsearch setup
es_client = Elasticsearch(
    ELASTIC_ENDPOINT,
    api_key=ELASTIC_API_KEY
)

# OpenAI setup
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Index configuration
index_source_fields = {
    "search-ikea.es": [
        "ai_embeddings"
    ]
}

# Construct the OpenAI API URL for chat completions
FULL_API_URL = f"{OPENAI_BASE_URL}/chat/completions"

def get_elasticsearch_results(query):
    """
    Query Elasticsearch for context.
    """
    es_query = {
        "retriever": {
            "standard": {
                "query": {
                    "nested": {
                        "path": "ai_embeddings.inference.chunks",
                        "query": {
                            "sparse_vector": {
                                "inference_id": "my-elser-endpoint",
                                "field": "ai_embeddings.inference.chunks.embeddings",
                                "query": query
                            }
                        },
                        "inner_hits": {
                            "size": 2,
                            "name": "search-ikea.es.ai_embeddings",
                            "_source": [
                                "ai_embeddings.inference.chunks.text"
                            ]
                        }
                    }
                }
            }
        },
        "size": 10
    }
    logger.info(f"Sending Elasticsearch query: {es_query}")
    result = es_client.search(index="search-ikea.es", body=es_query)
    return result["hits"]["hits"]

def create_openai_prompt(results):
    """
    Generate a prompt for OpenAI using Elasticsearch results.
    """
    context = ""
    for hit in results:
        inner_hit_path = f"{hit['_index']}.{index_source_fields.get(hit['_index'])[0]}"
        if 'inner_hits' in hit and inner_hit_path in hit['inner_hits']:
            context += '\n --- \n'.join(
                inner_hit['_source']['text'] for inner_hit in hit['inner_hits'][inner_hit_path]['hits']['hits']
            )
        else:
            source_field = index_source_fields.get(hit["_index"])[0]
            hit_context = hit["_source"][source_field]
            context += f"{hit_context}\n"

    prompt = f"""
    Instructions:
    
    - You are an assistant for question-answering tasks. Give a rich explanation.
    - Answer questions truthfully and factually using only the context presented.
    - If you don't know the answer, just say that you don't know; don't make up an answer.
    - You must always cite the document where the answer was extracted using inline academic citation style [], using the position.
    - Use markdown format for code examples.
    - You are correct, factual, precise, and reliable.

    Context:
    {context}
    """
    return prompt

def generate_openai_completion(user_prompt, question):
    """
    Generate a response using OpenAI.
    """
    response = openai_client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": user_prompt},
            {"role": "user", "content": question},
        ]
    )
    return response.choices[0].message.content

@app.route("/query", methods=["POST"])
def query():
    """
    Handle user queries. Expects JSON payload with a 'sentence' key.
    """
    data = request.json
    if not data or "sentence" not in data:
        logger.error("Invalid input: 'sentence' key is required.")
        return jsonify({"error": "Invalid input, 'sentence' key is required"}), 400

    user_sentence = data["sentence"]
    logger.info(f"Received sentence: {user_sentence}")

    try:
        # Query Elasticsearch for context
        logger.info("Querying Elasticsearch...")
        elasticsearch_results = get_elasticsearch_results(user_sentence)

        # Create OpenAI prompt
        logger.info("Creating OpenAI prompt...")
        context_prompt = create_openai_prompt(elasticsearch_results)

        # Generate response from OpenAI
        logger.info("Generating OpenAI completion...")
        openai_completion = generate_openai_completion(context_prompt, user_sentence)

        logger.info(f"OpenAI response: {openai_completion}")
        return jsonify({"response": openai_completion})
    except Exception as e:
        logger.error(f"Error processing the query: {e}")
        return jsonify({"error": "Failed to process the request"}), 500


if __name__ == "__main__":
    logger.info("Starting backend service...")
    app.run(host="0.0.0.0", port=5000)