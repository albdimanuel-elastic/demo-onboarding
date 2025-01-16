FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create the /var/log directory
RUN mkdir -p /var/log

EXPOSE 5000

CMD ["python", "app.py"]