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

Before deploying, create the dedicated namespace (if not using ArgoCD):

```bash
kubectl create namespace mdviewer
```

Then, deploy the application and service to your cluster:

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
  namespace: mdviewer
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
  namespace: mdviewer
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

* **`replicas: 1`**: Tells Kubernetes to ensure exactly one instance of your app is running at all times.
* **`selector`**: Defines how the Deployment finds the Pods it manages. It looks for Pods with the label `app: mdviewer`.
* **`template`**: This is the blueprint for the Pods. The `labels` here must match the `selector` above.
* **`containerPort: 8080`**: Tells Kubernetes that the application inside the container is listening on port 8080.

***

##### ⚡ Resource Management: Requests vs. Limits

The `resources` section is critical for cluster stability and ensuring your app has what it needs to perform.

###### **1. `requests` — Guaranteed Resources**

* This is the **minimum amount** of resources Kubernetes guarantees to the container.
* The scheduler uses this value to decide which node to place the Pod on.
* In your YAML:
    * `cpu: "200m"`: Requests 200 "millicores" (0.2 of a CPU core).
    * `memory: "256Mi"`: Requests 256 Mebibytes of RAM.

###### **2. `limits` — Maximum Allowed Resources**

* This is the **hard ceiling**. The container cannot consume more than this amount.
* **CPU Limit**: If reached, the container is throttled (slowed down) but usually not killed.
* **Memory Limit**: If reached, the container is **OOM Killed** (Out of Memory) and restarted by Kubernetes.
* In your YAML:
    * `cpu: "500m"`: Limits the container to 500 millicores (0.5 of a CPU core).
    * `memory: "512Mi"`: Limits the container to 512 Mebibytes of RAM.

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

#### Explanation of mdviewer-app.yaml

An **Argo CD Application** is a Custom Resource Definition (CRD) that tells Argo CD how to manage a set of Kubernetes resources as a single unit. It bridges the gap between your Git repository (the source of truth) and your cluster.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: mdviewer-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/nebupm/mdviewer.git
    targetRevision: HEAD
    path: k8s
  destination:
    server: https://kubernetes.default.svc
    namespace: mdviewer
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
```

***

##### 🔍 Key Sections

###### **1. `source` — Where the code lives**

* **`repoURL`**: The URL of the Git repository containing your manifests.
* **`path`**: The directory inside the repository where the Kubernetes YAML files are stored (in this case, the `k8s/` folder).
* **`targetRevision`**: Specifies which branch, tag, or commit to track (e.g., `HEAD` tracks the default branch).

###### **2. `destination` — Where the app goes**

* **`server`**: The API address of the target Kubernetes cluster (`https://kubernetes.default.svc` refers to the same cluster Argo CD is running on).
* **`namespace`**: The namespace where the application resources will be deployed (`mdviewer`).

###### **3. `syncPolicy` — Automation & GitOps**

* **`automated`**: Enables Argo CD to automatically sync changes when it detects a difference between Git and the cluster.
    * **`prune`**: Automatically deletes resources in the cluster that are no longer present in Git.
    * **`selfHeal`**: Automatically overwrites manual changes made in the cluster to ensure it matches Git.
* **`syncOptions: [CreateNamespace=true]`**: Tells Argo CD to create the target namespace if it doesn't already exist.

***

##### 🧠 Summary Table

| Section | Purpose | Key Benefit |
| :--- | :--- | :--- |
| **Source** | Connects to Git | Single source of truth |
| **Destination** | Targets the cluster | Deployment target management |
| **Sync Policy** | Automates deployment | Eliminates manual intervention & prevents drift |

***

## Verification Commands

Use these commands to check if the application is installed and running correctly:

### Check Pod Status

Verify that the pod is `Running`:

```bash
kubectl get pods -n mdviewer -l app=mdviewer
```

### Check Service Status

Verify the service is created and check the NodePort:

```bash
kubectl get service mdviewer-svc -n mdviewer
```

### Describe Deployment

Check for any errors in the deployment process:

```bash
kubectl describe deployment mdviewer -n mdviewer
```

### View Logs

Check the application logs for any startup errors:

```bash
kubectl logs -l app=mdviewer -n mdviewer
```

## Accessing the Application

Once the application is deployed and the pods are running, you can access the web interface using one of the following methods:

### Method 1: Using Minikube Service (Recommended)

This is the easiest way to get a clickable URL that automatically handles the network mapping for you.

```bash
minikube service mdviewer-svc -n mdviewer --url
```

### Method 2: Kubernetes Port Forwarding

If the service URL is not reachable or you prefer a stable localhost address, use port-forwarding to map the service directly to your machine.

```bash
# This maps your local port 8080 to the Service port 80
kubectl port-forward svc/mdviewer-svc -n mdviewer 8080:80
```

Then visit: **<http://localhost:8080>** in your browser.

### Method 3: Direct NodePort Access (macOS/Docker Limitations)

On macOS/Windows using the `docker` driver, the NodePort is exposed on the Minikube node (container) but is **not directly routable** from your host machine.

To make it work, you must start a tunnel in a separate terminal:

```bash
# This exposes the NodePort to your host
minikube tunnel
```

Once the tunnel is running, you can access the app at: **http://$(minikube ip):30080**

## Troubleshooting

### Issue: "Failed to load live state: namespace 'mdviewer' for Deployment 'mdviewer' is not managed"

This error occurs when Argo CD is configured to only manage specific namespaces on a cluster, and the target namespace (in this case, `mdviewer`) is not in that permitted list.

#### 🔍 Diagnosis (Root Cause Analysis)

1. **Check Application Status**:

    ```bash
    kubectl get application -n argocd mdviewer-app -o yaml
    ```

    Confirm the error message is present in the `status.conditions` block.

2. **Check Cluster Management Scope**:
    Verify if the cluster is restricted to specific namespaces using the Argo CD CLI:

    ```bash
    argocd cluster list
    ```

    If you see `(1 namespaces)` next to the server URL (e.g., `https://kubernetes.default.svc`), it means management is restricted.

3. **Inspect Cluster Secret**:
    Find the secret that stores the cluster configuration:

    ```bash
    kubectl get secrets -n argocd -l argocd.argoproj.io/secret-type=cluster
    ```

    If you inspect the YAML, a `namespaces` field under `data` indicates that restricted management is active.

#### 🛠️ Remedial Action

To allow Argo CD to manage all namespaces on the cluster (including `mdviewer`), remove the restriction from the cluster secret:

1. **Patch the Cluster Secret**:
    Replace `<SECRET_NAME>` with the name found in the previous step:

    ```bash
    kubectl patch secret <SECRET_NAME> -n argocd --type='json' -p='[{"op": "remove", "path": "/data/namespaces"}]'
    ```

2. **Verify the Change**:
    Ensure the namespace count is no longer shown in the cluster list:

    ```bash
    argocd cluster list
    ```

3. **Trigger a Hard Refresh**:
    Force Argo CD to reconcile the application with the new permissions:

    ```bash
    kubectl patch application mdviewer-app -n argocd --type merge -p '{"metadata": {"annotations": {"argocd.argoproj.io/refresh": "hard"}}}'
    ```
