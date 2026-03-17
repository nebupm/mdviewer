# mdviewer

This is a simple app to view markdown files.

## Kubernetes Deployment (Minikube)

To deploy this application in a Minikube cluster, follow these steps:

### 1. Build and Push the Image

Since Minikube needs access to the container image, build it and push it to your registry:

```bash
docker build -t deneasta/mdviewer:latest .
docker push deneasta/mdviewer:latest
```

### 2. Apply Manifests

Deploy the application and service to your cluster:

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### 3. Deploy via ArgoCD (Optional)

If you have ArgoCD installed and want to manage the app via GitOps:

```bash
kubectl apply -f mdviewer-app.yaml
```

## Verification Commands

Use these commands to check if the application is installed and running correctly:

### Check Pod Status

Verify that the pod is `Running`:

```bash
kubectl get pods -l app=mdviewer
```

### Check Service Status

Verify the service is created and check the NodePort:

```bash
kubectl get service mdviewer-svc
```

### Describe Deployment

Check for any errors in the deployment process:

```bash
kubectl describe deployment mdviewer
```

### View Logs

Check the application logs for any startup errors:

```bash
kubectl logs -l app=mdviewer
```

### Access the Application

Get the URL to access the app in your browser:

```bash
minikube service mdviewer-svc --url
```

Alternatively, use the NodePort directly (defined as `30080`):

```bash
# Get Minikube IP
minikube ip
# Visit http://<minikube-ip>:30080
```
 
