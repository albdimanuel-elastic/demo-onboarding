



# Demo Installation Automation with Ansible

This repository contains an Ansible playbook to automate the installation and setup of a Kubernetes-based demo environment. The steps include creating necessary Kubernetes secrets, installing Cert-Manager and OpenTelemetry Operator, building and deploying application images, and configuring annotations for instrumentation.

---

## Prerequisites

Before running the playbook, ensure the following tools are installed and configured:

- **Kubernetes Cluster**: A running Kubernetes cluster with `kubectl` configured.
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
4. **Build Application Images**:
   - Executes the `build-images.sh` script to build Docker images.
5. **Deploy Applications**:
   - Executes the `deploy-k8s.sh` script to deploy applications to Kubernetes.
6. **Add Annotations**:
   - Patches the backend deployment to add OpenTelemetry instrumentation annotations.

---

## Usage

### 1. Clone the Repository

```bash
git clone https://github.com/<your-repo-url>.git
cd <repository-folder>

```
---


### 2. Update Variables

Edit the `demo_installation.yml` file to customize the variables in the `vars` section:

```yaml
azure_openai_endpoint: "<Your Azure OpenAI Endpoint>"
azure_openai_api_key: "<Your Azure OpenAI API Key>"
azure_openai_deployment_name: "<Your Deployment Name>"
azure_openai_api_version: "<API Version>"
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
1.	Create Kubernetes secrets required by the backend application.
2.	Install Cert-Manager and apply the necessary CRDs.
3.	Install the OpenTelemetry Operator using Helm.
4.	Build Docker images for the applications.
5.	Deploy the applications to your Kubernetes cluster.
6.	Add OpenTelemetry instrumentation annotations to the backend deployment.

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
  kubectl get pods
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



**Troubleshooting**

​	•	**Cert-Manager Issues**:

​	•	If you encounter errors with Cert-Manager, ensure its CRDs are installed:


```
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.crds.yaml
```



​	•	**Helm Repository Errors**:

​	•	If Helm fails to add or update repositories, ensure you have internet access and correct repository URLs.

​	•	**Playbook Execution Fails**:

​	•	Review the playbook output to identify the error.

​	•	Ensure all required tools (kubectl, helm, ansible) are installed and correctly configured.

​	•	**OpenTelemetry Operator Installation Issues**:

​	•	Ensure dependencies like Cert-Manager are installed and verify the Helm chart values.
