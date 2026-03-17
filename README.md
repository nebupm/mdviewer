# mdviewer

This is a simple app to view markdown files.

## Kubernetes Deployment (Minikube)

To deploy this application in a Minikube cluster, follow these steps:

### 1. Build and Push the Image

Since Minikube needs access to the container image, build it and push it to your registry:

You can either build it from local or build from github repo.

```bash
docker build -t deneasta/mdviewer:latest .
or 
docker build -t deneasta/mdviewer:latest https://github.com/nebupm/mdviewer.git
```

Once its successfully build on your local setup, push this to the docker hub.

```bash
docker push deneasta/mdviewer:latest
```

### 2. Apply Manifests

Deploy the application and service to your cluster:

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```
#### Explanation of k8s/service.yaml

##### 🧩 Understanding the `ports` Section in a Kubernetes Service (NodePort)

When defining a **Service** in Kubernetes — especially of type `NodePort` — the `ports` section controls **how traffic flows** from outside the cluster to your application running inside a Pod.

Here is the Service YAML for reference:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mdviewer-svc
spec:
  selector:
    app: mdviewer
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
      nodePort: 30080
  type: NodePort
```

***

##### 🔍 What Each Port Field Means

###### **1. `port` — The Service Port**

* This is the **port exposed by the Service inside the cluster**.
* Other pods or cluster‑internal clients communicate with the service using this port.
* In your YAML:

```yaml
port: 80
```

    → The Service is accessible internally at **mdviewer-svc:80**.

***

###### **2. `targetPort` — The Pod Container Port**

* This is the **port your application listens on inside the container**.
* It maps the Service port → to the actual container port.
* In your YAML:

```yaml
targetPort: 8080
```

    → Means incoming traffic on port 80 gets forwarded to **port 8080** in the Pod.

This allows your container to listen on any port, while the service presents a stable API.

***

###### **3. `nodePort` — The External Port on the Node**

* This is the port exposed **on every Kubernetes node**, enabling external access.
* Only used because Service type is:

```yaml
type: NodePort
```

* In your YAML:

```yaml
nodePort: 30080
```

    → Users can access your app via:
        http://<NodeIP>:30080

Example for Minikube: `http://$(minikube ip):30080`

***

###### 🔁 How Traffic Flows (End‑to‑End)

    User → NodeIP:30080 (nodePort) → Service mdviewer-svc:80 (port) → Pod container:8080 (targetPort)

This three‑layer port mapping provides:

* Port stability
* Port translation
* External access control
* Flexible internal routing

***

##### 🧠 Summary Table

| Field          | Description                                               | Your Value |
| -------------- | --------------------------------------------------------- | ---------- |
| **nodePort**   | Port exposed on each Kubernetes node for external traffic | `30080`    |
| **port**       | Cluster‑internal Service port                             | `80`       |
| **targetPort** | Pod container application port                            | `8080`     |

***

#### Explanation of k8s/deployment.yaml

A **Deployment** is a Kubernetes resource that manages a set of identical Pods. It handles scaling, updates, and self-healing (restarting pods if they fail).

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mdviewer
  labels:
    app: mdviewer
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mdviewer
  template:
    metadata:
      labels:
        app: mdviewer
    spec:
      containers:
      - name: mdviewer
        image: deneasta/mdviewer:latest
        ports:
        - containerPort: 8080
        resources:
          limits:
            cpu: "500m"
            memory: "512Mi"
          requests:
            cpu: "200m"
            memory: "256Mi"
```

***

##### 🔍 Core Components

*   **`replicas: 1`**: Tells Kubernetes to ensure exactly one instance of your app is running at all times.
*   **`selector`**: Defines how the Deployment finds the Pods it manages. It looks for Pods with the label `app: mdviewer`.
*   **`template`**: This is the blueprint for the Pods. The `labels` here must match the `selector` above.
*   **`containerPort: 8080`**: Tells Kubernetes that the application inside the container is listening on port 8080.

***

##### ⚡ Resource Management: Requests vs. Limits

The `resources` section is critical for cluster stability and ensuring your app has what it needs to perform.

###### **1. `requests` — Guaranteed Resources**
*   This is the **minimum amount** of resources Kubernetes guarantees to the container.
*   The scheduler uses this value to decide which node to place the Pod on.
*   In your YAML:
    *   `cpu: "200m"`: Requests 200 "millicores" (0.2 of a CPU core).
    *   `memory: "256Mi"`: Requests 256 Mebibytes of RAM.

###### **2. `limits` — Maximum Allowed Resources**
*   This is the **hard ceiling**. The container cannot consume more than this amount.
*   **CPU Limit**: If reached, the container is throttled (slowed down) but usually not killed.
*   **Memory Limit**: If reached, the container is **OOM Killed** (Out of Memory) and restarted by Kubernetes.
*   In your YAML:
    *   `cpu: "500m"`: Limits the container to 500 millicores (0.5 of a CPU core).
    *   `memory: "512Mi"`: Limits the container to 512 Mebibytes of RAM.

***

##### 🧠 Summary Table

| Field | Purpose | Units |
| :--- | :--- | :--- |
| **Requests** | Minimum guaranteed; used for scheduling | `m` (1/1000th core), `Mi` (Mebibytes) |
| **Limits** | Maximum allowed; prevents resource hogging | `m`, `Mi` |

***

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
 
