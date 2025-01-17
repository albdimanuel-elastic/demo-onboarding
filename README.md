



#       DEMO GOAL

The purpose of this demo is to practice semantic search and build an end-to-end solution that involves web crawling, data indexing, microservices development, and auto-instrumentation using OpenTelemetry. Additionally, the demo will integrate OpenAI’s LLM (Large Language Model) to create a **Retrieval-Augmented Generation (RAG)** application.

![](https://github.com/albdimanuel-elastic/demo-onboarding/blob/main/images/demo-flowdiagram.png)

**Step-by-Step Overview**

​	1.	**Web Crawling with Ikea’s Product Pages**:

​	•	A web crawler will traverse the Ikea website to collect product data.

​	•	This data will include product names, descriptions, and other relevant metadata.

​	2.	**Data Storage in Elasticsearch**:

​	•	The collected data will be stored in an Elasticsearch index called search_ikeas.es.

​	•	The index settings will be customized to include semantic fields based on the content gathered from the Ikea website. These settings will enable advanced semantic search capabilities.

​	3.	**Integration with OpenAI’s LLM**:

​	•	The **backend service** will integrate with **OpenAI’s LLM** to process user queries.

​	•	The LLM will interact with the *search_ikeas.es* index in Elasticsearch to retrieve relevant documents.

​	•	This integration will form the foundation of a **Retrieval-Augmented Generation (RAG)** application, where the LLM combines its generative capabilities with the semantic data retrieved from Elasticsearch.

​	4.	**Microservices Development**:

​	•	Two microservices will be developed:

​	•	**Frontend Service**:

​		•	Built in **Node.js**, this service will provide a user-friendly web interface.

​		•	Users will interact with this interface to perform semantic searches and view RAG-based results.

​	•	**Backend Service**:

​		•	Built in **Python**, this service will handle:

​		•	Querying Elasticsearch for relevant documents.

​		•	Sending user queries and retrieved documents to OpenAI’s LLM.

​		•	Returning LLM-generated responses to the frontend.

​		•	This backend service will act as the core logic for integrating Elasticsearch and OpenAI’s LLM.

​	5.	**Auto-Instrumentation with OpenTelemetry**:

​	•	Both microservices will be auto-instrumented for observability:

​	•	OpenTelemetry instrumentation will be applied to the services to collect traces, metrics, and logs.

​	•	The OpenTelemetry **Kubernetes Operator** provided by Elastic will be used to simplify and manage the instrumentation process.

​	•	This will ensure end-to-end observability, allowing for monitoring and troubleshooting of the application.



# Web Crawler and mapping updates

The process begins with a web crawler navigating through Ikea’s website to collect detailed product information, including names, descriptions, and metadata. This data is then structured and prepared for storage in Elasticsearch.

To enable semantic search, the data is indexed into an Elasticsearch index named search_ikeas.es. The index mapping is updated to include a semantic field that leverages the ELSER (Elastic Learned Sparse Encoder Representations) model. This model generates vectorized representations of the product descriptions, allowing Elasticsearch to perform intent-based semantic searches.

By integrating web crawling with semantic mapping updates using ELSER, the system enables advanced search functionality that provides highly relevant and meaningful results based on user queries.



**Create an inference_api from the DevOps console:**

```bash
 PUT _inference/sparse_embedding/my-elser-endpoint
{
  "service": "elasticsearch",
  "service_settings": {
    "num_threads": 1,
    "num_allocations": 8,
    "model_id": ".elser_model_2"
  }
}
```



**Create the crawler**:

![](https://github.com/albdimanuel-elastic/demo-onboarding/blob/main/images/crawler.png)



**Update the index mapping adding a new field:**

![](https://github.com/albdimanuel-elastic/demo-onboarding/blob/main/images/mappings.png)


**Verify the field is populated correctly in the documents:**

![](https://github.com/albdimanuel-elastic/demo-onboarding/blob/main/images/embeddings.png)


# Application setup  with Ansible

This repository contains an Ansible playbook to automate the installation and setup of a Kubernetes-based demo environment. The steps include creating necessary Kubernetes secrets, installing Cert-Manager and OpenTelemetry Operator, building and deploying application images, and configuring annotations for instrumentation.



---

## Prerequisites

Before running the playbook, ensure the following tools are installed and configured:

- **Update the file demo-installation-playbook.yml** setting the vars sections pointing to the Elastic Deployment and the OpenAI API Key.

- **Kubernetes Cluster**: A running Kubernetes cluster with `kubectl` configured. For this demo a minikube k8s cluster has been used. (it's important to boot k8s with resources enough):

  ```
  minikube start --cpus=4 --memory 4096 --disk-size 32g
  ```

- **Elastic Deployment.**: XXXXXX

- **Helm**: Installed and available in your environment.

- **Ansible**: Installed on your local machine.

- **Scripts**: Ensure the following scripts are available in the repository:
  - `build-images.sh`: Builds the required application images.
  - `deploy-k8s.sh`: Deploys the applications to Kubernetes.

---

## Files

- **`demo_installation.yml`**: The main Ansible playbook for automating the demo setup.
- **`build-images.sh`**: A script to build application Docker images.
- **`deploy-k8s.sh`**: A script to deploy the applications to Kubernetes.

---

## Steps Automated by the Playbook

1. **Create Kubernetes Secrets**:
   - Generates secrets needed by the backend application.
2. **Install Cert-Manager**:
   - Adds the Helm repository, installs CRDs, and deploys Cert-Manager.
3. **Install OpenTelemetry Operator**:
   - Installs the OpenTelemetry Operator using Helm with the required configurations.
  
![](https://github.com/albdimanuel-elastic/demo-onboarding/blob/main/images/ansible-diagram.png)


1. **Build Application Images**:
   - Executes the `build-images.sh` script to build Docker images.
2. **Deploy Applications**:
   - Executes the `deploy-k8s.sh` script to deploy applications to Kubernetes.
3. **Add Annotations**:
   - Patches the backend deployment to add OpenTelemetry instrumentation annotations.

![]()


---

## Usage

### 1. Clone the Repository

```bash
git clone https://github.com/albdimanuel-elastic/demo-onboarding.git
cd demo-onboarding
```
---


### 2. Update Variables

Edit the `demo_installation.yml` file to customize the variables in the `vars` section:

```yaml

openai_api_key: "<Your OpenAI API Key>"
elastic_endpoint: "<Elastic Cloud Endpoint>"
otel_exporter_otlp_endpoint: "<OTEL Exporter Endpoint>"
otel_exporter_otlp_headers: "<OTEL Exporter Headers>"
elastic_api_key: "<Your Elastic API Key>"
```
---

### Run the Playbook

Execute the Ansible playbook to set up the demo environment:

```bash
ansible-playbook demo_installation.yml
```
This command will automate the following steps:
1.	**Create Kubernetes secrets** required by the backend application.
2.	Install Cert-Manager and apply the necessary CRDs.
3.	**Install the OpenTelemetry Operator** using Helm.
4.	**Build Docker images** for the applications.
5.	**Deploy the applications to your Kubernetes** cluster.
6.	**Add OpenTelemetry instrumentation annotations** to the backend deployment.

Ensure all prerequisites are met before running the playbook, such as having kubectl, helm, and ansible properly installed and configured.



## Testing the Setup

### 3. Verify Kubernetes Resources

Use the following commands to confirm that Kubernetes resources are created and running correctly:

- **Check Kubernetes Secrets**:
  Run the following command to list all secrets in the Kubernetes cluster and verify that the `backend-config` secret is present:
  
  ```bash
  kubectl get secrets 
  ```
- **Verify Cert-Manager Installation**:
  Cert-Manager should be installed in the cert-manager namespace. Use this command to check the status of Cert-Manager pods:
  
  ```bash
  kubectl get pods -n cert-manager
  ```
- **Verify OpenTelemetry Operator Installation**:
  Confirm that the OpenTelemetry Operator pods are deployed and running in the default namespace::
  
  ```bash
  kubectl get pods -n opentelemetry-operator-system
  ```

### 4. Access the Frontend Application
#### Using NodePort:

To verify that the frontend application is running, you can use one of the following methods:
1. Retrieve the NodePort and the external IP of the frontend service:
   ```
   kubectl get svc frontend-service
   ```
   Example output:

   ```
   NAME              TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
   frontend-service  NodePort   10.109.137.45    <none>        80:30080/TCP     5m
   
   ```

2. Access the frontend using the node’s IP address and NodePort:

•	Replace <node-ip> with the external IP of your node.
•	Replace <node-port> with the NodePort value (e.g., 30080 in the example above).
•	Open your browser and navigate to:

```
http://<node-ip>:<node-port>
```

#### Using Port forwarding:


1.	Forward port 8080 on your local machine to the service’s port 80 in the cluster:

```
kubectl port-forward svc/frontend-service 8080:80
```

2.	Open your browser and navigate to:

```
http://localhost:8080
```



### 5. Test the frontend and check the backend

To verify that the frontend successfully connects to the backend and that the backend is integrated with the LLM, follow these steps:



**Step 1: Access the Frontend**

​	1.	Open your browser and navigate to the frontend:

​	•	**NodePort**: http://<node-ip>:<node-port>

​	•	**Port Forwarding**: http://localhost:8080

​	2.	Enter a test query in the frontend’s input form and submit it. The query will be sent to the backend for processing.



**Step 2: Verify Backend Response**

​	1.	If the backend is correctly integrated with the LLM:

​	•	The LLM will process the query and return a generated response.

​	•	This response will be displayed on the frontend.

​	2.	If there is an issue, the frontend might display an error message or incomplete results.



**Step 3: Invoke the Backend Directly**

​	1.	Use a curl command to test the backend directly:

```
curl -X POST http://<backend-service>:5000/query \
 -H "Content-Type: application/json" \
 -d '{"query": "This is a test query"}'
```



If the LLM is integrated correctly, the backend will return a response generated by the model.


![](https://github.com/albdimanuel-elastic/demo-onboarding/blob/main/images/frontend-home.png)



**Step 4: Check Backend Logs**

​	1.	Inspect the backend logs to confirm LLM interaction:

```
kubectl logs <backend-pod-name>
```



​	2.	Look for entries indicating:

​	•	The receipt of the request from the frontend.

​	•	The query sent to the LLM.

​	•	The response received and processed by the backend.


![](https://github.com/albdimanuel-elastic/demo-onboarding/blob/main/images/backend-logs.png)



**Expected Outcome**

​	•	If the integration is successful:

​	•	The frontend displays a response generated by the LLM.

​	•	Backend logs confirm the query processing and interaction with the LLM.



### 6. Run Semantic Searches. Demo in action

**Testing a RAG Application in Action**

Get ready to see a **Retrieval-Augmented Generation (RAG) application** in action! In this demo, we’re taking the power of an LLM and integrating it with **private data**—specifically, a retailer’s product catalog stored in an Elasticsearch index.

We’re pushing the limits of **semantic search** by leveraging **ELSER** and **sparse vectors** to deliver relevant, intent-based results.

**The Real-World Scenario**

Imagine this: we want to explore office chairs. Not just any chairs—we’re looking for ones that:

​	•	Are **highly rated by users**,

​	•	Provide **great comfort**, and

​	•	**Look stylish** while doing it.

This isn’t a simple keyword search. This is where **semantic search** and the LLM come into play.

**How It Works**

​	1.	**Semantic Search with ELSER**:

​	•	The query is sent to Elasticsearch, where ELSER transforms it into a sparse vector.

​	•	Elasticsearch performs a similarity search across the index to retrieve the most relevant products based on user intent.

​	2.	**LLM-Enhanced Results**:

​	•	The retrieved data is enriched by the LLM.

​	•	The LLM uses its generative capabilities to provide a **human-like response** that combines the catalog data with user preferences.

​	3.	**The RAG Workflow**:

​	•	Query → Elasticsearch (via semantic search) → Relevant results → LLM → Final response.

We’ll ask the system:

​	“Show me office chairs that are highly rated by users, very comfortable, and maintain great style.”

​	•	The **semantic search** will dig into the product catalog for the best matches based on user reviews and product descriptions.

​	•	The **LLM** will enhance these results, explaining why these chairs are the best fit for your query.

![](https://github.com/albdimanuel-elastic/demo-onboarding/blob/main/images/llm-diagram.png)

**Why This Matters**



This demo showcases the future of intelligent search:

​	•	Integrating **private, domain-specific data** with the creativity of an LLM.

​	•	Using **advanced search techniques** like ELSER and sparse vectors to truly understand user intent.

​	•	Delivering insights that are not only accurate but also engaging and meaningful.


![](https://github.com/albdimanuel-elastic/demo-onboarding/blob/main/images/frontend-action.png)


![](https://github.com/albdimanuel-elastic/demo-onboarding/blob/main/images/backend-llm-logs.png)




### 7. Check Elastic APM - Observability



**Observability with Elastic: Seamless End-to-End Visibility**



In this demo, we’ve integrated observability into the **frontend** and **backend** services using **OpenTelemetry** and Elastic. The process was straightforward, thanks to the **Elastic Kubernetes Operator**, which simplifies the instrumentation process and ensures full visibility into our application. The  observability was seamlessly integrated into the **frontend** and **backend** services using **OpenTelemetry** and Elastic. The process was simplified by adding **annotations** to the Kubernetes deployment files, making it both flexible and efficient.

For the **frontend** retail the deployment manifest has been updated:

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
      annotations:
        instrumentation.opentelemetry.io/inject-nodejs: "opentelemetry-operator-system/elastic-instrumentation"
    spec:
      containers:
      - name: frontend
        image: albertodimanuel275/frontend-demo-onboarding:latest
        ports:
        - containerPort: 3000
```

For the **backend service the annotations are made using kubectl dynamically:**

```
 kubectl patch deployment backend --type=json -p='[{"op": "add", "path": "/spec/template/metadata/annotations", "value": {"instrumentation.opentelemetry.io/inject-python": "opentelemetry-operator-system/elastic-instrumentation"}}]'
```



**This approach eliminated the need for manual instrumentation in the application code**, allowing us to focus on building the application while ensuring robust observability.



**Effortless Auto-Instrumentation with OpenTelemetry**



Instrumenting the services was remarkably easy:

​	1.	The **Elastic Kubernetes Operator** automatically injected OpenTelemetry configurations into the **frontend** (Node.js) and **backend** (Python) services.

​	2.	With minimal setup, we collected **traces**, **logs**, and **metrics** directly in Elastic, all in context, without requiring significant code changes.



This streamlined process enabled both services to emit observability data, giving us insights into how they interact and perform in real time.



**Comprehensive Observability with Elastic**



Elastic provides **end-to-end visibility** across the entire stack:

​	•	**Traces**: Automatically capture the flow of requests across the **frontend** and **backend**, including interactions with Elasticsearch and OpenAI’s LLM.

​	•	**Logs**: View logs in context with traces to quickly troubleshoot errors or performance issues.

​	•	**Metrics**: Monitor resource utilization and application performance metrics to ensure optimal health.


![](https://github.com/albdimanuel-elastic/demo-onboarding/blob/main/images/frontend-overview.png)


![](https://github.com/albdimanuel-elastic/demo-onboarding/blob/main/images/trace-logs.png)



**Kubernetes Cluster Insights**



The **Elastic Kubernetes Operator** goes a step further by collecting detailed information about the **Kubernetes cluster** and its workloads:

​	•	**Cluster Health**: Automatically gathers metrics such as node utilization, pod status, and resource availability.

​	•	**Workload Observability**: Provides visibility into deployments, services, and other Kubernetes resources, giving a complete picture of how the workloads interact within the cluster.

![](https://github.com/albdimanuel-elastic/demo-onboarding/blob/main/images/k8scluster-overview.png)

![](https://github.com/albdimanuel-elastic/demo-onboarding/blob/main/images/host-overview.png)

![](https://github.com/albdimanuel-elastic/demo-onboarding/blob/main/images/workloads-k8.png)


**The Result: True End-to-End Visibility**



With Elastic, we have a **single pane of glass** for monitoring and debugging:

​	•	We can follow a **user request** from the **frontend**, through the **backend**, into **Elasticsearch**, and even through **OpenAI’s LLM**, all within a unified interface.

​	•	Traces, logs, and metrics are **automatically correlated**, enabling faster troubleshooting and deeper insights into the application’s behavior.

![](https://github.com/albdimanuel-elastic/demo-onboarding/blob/main/images/service-map.png)




**Why This Matters**



This level of observability ensures:

​	•	**Faster Troubleshooting**: Quickly identify and resolve performance bottlenecks or errors.

​	•	**Proactive Monitoring**: Gain real-time insights into the health of the application and Kubernetes cluster.

​	•	**Enhanced User Experience**: Deliver a reliable and performant application by addressing issues before they impact users.



Elastic and OpenTelemetry together make observability **powerful yet simple**, enabling developers and operators to focus on innovation rather than configuration.



### **Troubleshooting**

​	•	**Cert-Manager Issues**: If you encounter errors with Cert-Manager, ensure its CRDs are installed:


```
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.crds.yaml
```

​	•	**Helm Repository Errors**: if Helm fails to add or update repositories, ensure you have internet access and correct repository URLs.

​	•	**Playbook Execution Fails**: 

​			- Review the playbook output to identify the error.

​			- Ensure all required tools (kubectl, helm, ansible) are installed and correctly configured.

​	•	**OpenTelemetry Operator Installation Issues**:  Ensure dependencies like Cert-Manager are installed and verify the Helm chart values.



If find any problem or just want to discuss the demo openly, don't hesitate to contacto me: alberto.dimanuel@elastio.co

