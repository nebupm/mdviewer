# mdviewer

This is a simple app to view markdown files.

## Key Features

- **Global Search:** Search across all markdown files in the library from a central search bar in the sidebar.
- **Contextual Highlights:** View search results with text snippets and highlighted keywords for quick identification.
- **Match Counter:** Automatically calculates how many unique content pages (folders) contain your search term.
- **Deep Linking:** Clicking a search result takes you directly to the specific file within its folder using automatic anchor points.
- **Return to Search:** A smart navigation bar appears when viewing content from a search result, allowing you to return to your exact search position with one click.
- **GitOps Ready:** Fully integrated with GitHub Actions and Argo CD for automated builds and deployments.

## Project Structure

```
mdviewer/
├── app/                        # Application source code
│   ├── app.py
│   ├── content/                # Markdown content files
│   ├── static/                 # CSS and images
│   └── templates/              # HTML templates
├── deploy/                     # All deployment artifacts
│   ├── argocd/
│   │   └── application.yaml    # ArgoCD Application definition
│   ├── helm/
│   │   └── mdviewer/           # Helm chart (primary K8s deployment method)
│   │       ├── Chart.yaml
│   │       ├── values.yaml         # Base defaults
│   │       ├── values-dev.yaml     # Dev environment overrides
│   │       ├── values-prod.yaml    # Prod environment overrides
│   │       └── templates/
│   └── k8s/
│       ├── base/               # Raw manifests (Kustomize base)
│       └── overlays/           # Environment-specific overlays
│           ├── dev/
│           └── prod/
├── .github/
│   └── workflows/
│       └── ci.yml              # CI — build image, push to Docker Hub, update Helm values
├── Dockerfile
├── compose.yaml
└── requirements.txt
```

---

## Local Development & Testing

### Option 1: Python Virtual Environment (Recommended for development)

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask application:

   ```bash
   python app/app.py
   ```

   The application will be available at: http://localhost:8080

### Option 2: Docker Compose

1. Build and start the container:

   ```bash
   docker compose up --build -d
   ```

2. Access the application at: http://localhost:5001

3. Stop the container:

   ```bash
   docker compose down
   ```

---

## Deploying to Kubernetes

There are two ways to deploy the application to a cluster. ArgoCD is the recommended approach for any persistent environment; the manual method is for cases where ArgoCD is not available.

---

### Option 1: GitOps with ArgoCD (Recommended)

ArgoCD watches the Helm chart in this repository and automatically applies changes to the cluster whenever `deploy/helm/mdviewer/values.yaml` is updated — which the CI pipeline does on every successful build. No manual intervention is required once ArgoCD is set up.

The ArgoCD Application manifest lives at `deploy/argocd/application.yaml`. Apply it once to the cluster where ArgoCD is running:

```bash
kubectl apply -f deploy/argocd/application.yaml
```

### Application Manifest

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: mdviewer-app-multipass
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/nebupm/mdviewer.git
    targetRevision: HEAD
    path: deploy/helm/mdviewer
    helm:
      valueFiles:
        - values.yaml
  destination:
    name: k8slab
    namespace: mdviewer
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
      - ApplyOutOfSyncOnly=true
      - Adopt=true
```

### Key Sections

| Section | Purpose |
| :--- | :--- |
| `source.path` | Directory in the repo containing the Helm chart |
| `source.helm.valueFiles` | Values files ArgoCD passes to Helm at render time |
| `destination.name` | The registered cluster name in ArgoCD |
| `syncPolicy.automated` | Enables auto-sync on Git changes |
| `syncPolicy.automated.prune` | Deletes cluster resources removed from Git |
| `syncPolicy.automated.selfHeal` | Reverts manual cluster changes to match Git |

---

### Option 2: Manual Deployment with Helm

Use this when ArgoCD is not available. After CI runs and updates `values.yaml`, pull the latest changes and run Helm directly against your cluster.

#### Install or Upgrade (default values)

```bash
git pull
helm upgrade --install mdviewer deploy/helm/mdviewer \
  --namespace mdviewer \
  --create-namespace
```

#### Environment-Specific Deployments

```bash
# Dev
helm upgrade --install mdviewer deploy/helm/mdviewer \
  --namespace mdviewer \
  --create-namespace \
  --values deploy/helm/mdviewer/values-dev.yaml

# Prod
helm upgrade --install mdviewer deploy/helm/mdviewer \
  --namespace mdviewer \
  --create-namespace \
  --values deploy/helm/mdviewer/values-prod.yaml
```

#### Deploy a Specific Image Tag

If you want to deploy a particular build without editing `values.yaml`:

```bash
helm upgrade --install mdviewer deploy/helm/mdviewer \
  --namespace mdviewer \
  --create-namespace \
  --set image.tag=<git-sha>
```

#### Dry Run (Inspect Rendered Manifests Before Applying)

```bash
helm template mdviewer deploy/helm/mdviewer
```

---

### Understanding `values.yaml`

| Field | Purpose |
| :--- | :--- |
| `replicaCount` | Number of Pod replicas Kubernetes maintains |
| `image.repository` | Docker image name |
| `image.tag` | Image version; updated automatically by CI on every build |
| `image.pullPolicy` | When to pull the image (`IfNotPresent`, `Always`) |
| `service.type` | Service exposure type (`NodePort`, `ClusterIP`, `LoadBalancer`) |
| `service.port` | Cluster-internal service port |
| `service.targetPort` | Port the container application listens on |
| `service.nodePort` | External port exposed on every node (NodePort only) |
| `resources.requests` | Minimum resources guaranteed to the container; used by the scheduler |
| `resources.limits` | Hard ceiling — CPU is throttled, memory excess causes OOM kill |

#### How Traffic Flows (NodePort)

```
User → NodeIP:30080 (nodePort) → Service mdviewer-svc:80 (port) → Pod container:8080 (targetPort)
```

---

## CI — Build and Push (GitHub Actions)

The pipeline at `.github/workflows/ci.yml` is a **pure CI workflow** — it builds the Docker image, publishes it, and records the new image tag in the Helm chart. It does not deploy to any cluster. Deployment is handled separately, either by ArgoCD (recommended) or by running Helm manually.

### What the Pipeline Does

1. **Trigger:** Runs when `app/**`, `Dockerfile`, or `requirements.txt` changes on `main`.
2. **Build & Push:** Builds a multi-platform Docker image tagged with the Git commit SHA and pushes it to Docker Hub.
3. **Update Helm values:** Writes the new SHA into `image.tag` in `deploy/helm/mdviewer/values.yaml` using `sed`.
4. **Commit back:** Pushes the updated `values.yaml` to the repo with `[skip ci]` to prevent the workflow re-triggering itself.

After step 4, `values.yaml` in the repo is the single source of truth for which image version should be running. ArgoCD picks this up automatically; without ArgoCD, a manual `helm upgrade` is required (see [Option 2](#option-2-manual-deployment-with-helm) above).

### Workflow (`.github/workflows/ci.yml`)

```yaml
name: CI — Build and Push

on:
  push:
    branches: [ "main" ]
    paths:
      - 'app/**'
      - 'Dockerfile'
      - 'requirements.txt'
      - '.github/workflows/ci.yml'

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}

      - uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - uses: docker/setup-qemu-action@v3
      - uses: docker/setup-buildx-action@v3

      - uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          platforms: linux/amd64,linux/arm64
          tags: |
            deneasta/mdviewer:${{ github.sha }}
            deneasta/mdviewer:latest

      - name: Update image tag in Helm values
        run: |
          sed -i 's|tag: ".*"|tag: "${{ github.sha }}"|' deploy/helm/mdviewer/values.yaml

      - name: Commit and push Helm values change
        run: |
          git config --global user.name 'github-actions[bot]'
          git config --global user.email 'github-actions[bot]@users.noreply.github.com'
          git add deploy/helm/mdviewer/values.yaml
          git commit -m "chore: update image tag to ${{ github.sha }} [skip ci]"
          git push
```

### Required Setup

#### GitHub Secrets

Go to **Settings > Secrets and variables > Actions** and add:

- `DOCKERHUB_USERNAME` — your Docker Hub username
- `DOCKERHUB_TOKEN` — a Docker Hub Personal Access Token

#### Workflow Permissions

The `GITHUB_TOKEN` needs write access to commit the manifest update back:

1. Go to **Settings > Actions > General**
2. Under **Workflow permissions**, select **Read and write permissions**
3. Click **Save**

---

## Updating & Managing the Application

### With ArgoCD

Push to `main`. The CI pipeline builds a new image and commits the updated `image.tag` into `deploy/helm/mdviewer/values.yaml`. ArgoCD detects the Git change and runs `helm upgrade` automatically — no manual steps required.

### Without ArgoCD (Manual)

Push to `main` to trigger CI, then once the CI commit lands, pull and run Helm:

```bash
git pull
helm upgrade mdviewer deploy/helm/mdviewer --namespace mdviewer
```

See [Option 2: Manual Deployment with Helm](#option-2-manual-deployment-with-helm) for environment-specific and tag-override commands.

### Other Management Commands

```bash
# Force a redeploy of the same image (e.g. to pick up ConfigMap changes)
kubectl rollout restart deployment/mdviewer -n mdviewer

# Roll back to the previous Helm release
helm rollback mdviewer -n mdviewer
```

---

## Verification & Health Checks

### 1. Check Deployment and Pod Status

```bash
kubectl get deployment,pods -n mdviewer
```

Pods should be `Running` and `1/1 Ready`.

### 2. Verify Service and Endpoints

```bash
kubectl get service,endpoints -n mdviewer
```

If `Endpoints` shows `<none>`, the service selector does not match the pod labels.

### 3. Inspect Events (for failing pods)

```bash
kubectl describe pod -l app=mdviewer -n mdviewer
```

### 4. HTTP Health Check

```bash
curl -I http://<Node-IP>:30080
```

### 5. View Live Logs

```bash
kubectl logs -l app=mdviewer -n mdviewer --tail 20
```

---

## Accessing the Application

### Minikube — Service URL

```bash
minikube service mdviewer-svc -n mdviewer --url
```

### Port Forwarding (any cluster)

```bash
kubectl port-forward svc/mdviewer-svc -n mdviewer 8080:80
```

Then visit: http://localhost:8080

### NodePort — Minikube with Docker driver (macOS)

Start a tunnel in a separate terminal, then access via the Minikube IP:

```bash
minikube tunnel
# then: http://$(minikube ip):30080
```

### NodePort — General K8s Cluster (Multipass)

Access from any node IP on port `30080`:

| Node | IP |
| :--- | :--- |
| k8s-m1 | 192.168.2.30 |
| k8s-m2 | 192.168.2.31 |
| k8s-m3 | 192.168.2.32 |
| k8s-w1 | 192.168.2.33 |
| k8s-w2 | 192.168.2.34 |

Example: http://192.168.2.30:30080

Traffic hits the `kube-proxy` on whichever node you target and is routed to the running pod, regardless of which node the pod is actually on.

---

## Troubleshooting

### "Failed to load live state: namespace 'mdviewer' is not managed"

ArgoCD is restricted to specific namespaces and `mdviewer` is not in that list.

1. Check if the cluster is namespace-restricted:

   ```bash
   argocd cluster list
   ```

   A `(1 namespaces)` annotation next to the server URL confirms the restriction.

2. Remove the restriction from the cluster secret:

   ```bash
   kubectl get secrets -n argocd -l argocd.argoproj.io/secret-type=cluster
   kubectl patch secret <SECRET_NAME> -n argocd \
     --type='json' \
     -p='[{"op": "remove", "path": "/data/namespaces"}]'
   ```

3. Force a hard refresh:

   ```bash
   kubectl patch application mdviewer-app-multipass -n argocd \
     --type merge \
     -p '{"metadata": {"annotations": {"argocd.argoproj.io/refresh": "hard"}}}'
   ```

### Application not syncing after a push

1. Check for sync errors:

   ```bash
   argocd app get mdviewer-app-multipass
   ```

2. Compare commit hashes:

   ```bash
   argocd app get mdviewer-app-multipass | grep "Sync Status"
   git ls-remote https://github.com/nebupm/mdviewer.git HEAD
   ```

   If they match but the cluster hasn't updated, the issue is likely in the rendered Helm chart (e.g. image tag not propagating).

3. Force an immediate refresh:

   ```bash
   argocd app get mdviewer-app-multipass --refresh
   ```

4. Inspect the diff:

   ```bash
   argocd app diff mdviewer-app-multipass
   ```
