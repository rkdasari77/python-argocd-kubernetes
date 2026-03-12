# 🛒 ShopWave — Python Ecommerce App on Kubernetes
## GitOps Pipeline: GitHub Actions + ArgoCD

---

## 🏗️ Architecture Overview

```
Developer → GitHub (Push) → GitHub Actions → Docker Hub
                                   ↓
                        Update K8s Manifest (Git commit)
                                   ↓
                              ArgoCD (watches Git)
                                   ↓
                         Kubernetes Cluster → Pods
```

### Pipeline Flow

| Step | Tool | Action |
|------|------|--------|
| 1 | Developer | Commits code to GitHub |
| 2 | GitHub Actions | Runs tests |
| 3 | GitHub Actions | Builds & pushes Docker image |
| 4 | GitHub Actions | Updates image tag in `k8s/deployment.yaml` |
| 5 | ArgoCD | Detects manifest change, syncs cluster |
| 6 | Kubernetes | Performs rolling update with zero downtime |

---

## 📁 Project Structure

```
ecommerce-gitops/
├── app/
│   ├── app.py                  # Flask ecommerce application
│   ├── requirements.txt        # Python dependencies
│   └── templates/
│       ├── index.html          # Product listing page
│       └── cart.html           # Shopping cart page
├── Dockerfile                  # Container definition
├── .github/
│   └── workflows/
│       └── ci-cd.yml           # GitHub Actions pipeline
├── k8s/                        # Kubernetes manifests (GitOps source of truth)
│   ├── namespace.yaml
│   ├── deployment.yaml         # ← Image tag updated by pipeline
│   ├── service.yaml
│   ├── ingress.yaml
│   └── secret.yaml
└── argocd/
    └── application.yaml        # ArgoCD Application definition
```

---

## 🚀 Setup Guide

### Prerequisites
- Kubernetes cluster (minikube, EKS, GKE, AKS, etc.)
- `kubectl` configured
- ArgoCD installed on the cluster
- Docker Hub account
- GitHub repository

---

### Step 1: Set GitHub Secrets

In your GitHub repo → Settings → Secrets → Actions:

| Secret | Value |
|--------|-------|
| `DOCKERHUB_USERNAME` | Your Docker Hub username |
| `DOCKERHUB_TOKEN` | Docker Hub access token |

---

### Step 2: Install ArgoCD

```bash
# Create namespace and install ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for pods to be ready
kubectl wait --for=condition=Ready pods --all -n argocd --timeout=120s

# Access the ArgoCD UI
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Get initial admin password
kubectl get secret argocd-initial-admin-secret -n argocd \
  -o jsonpath="{.data.password}" | base64 -d && echo
```

Visit: https://localhost:8080 (admin / <password above>)

---

### Step 3: Apply K8s Manifests

```bash
# Update k8s/secret.yaml with real values first!
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secret.yaml
```

---

### Step 4: Register App with ArgoCD

```bash
# Update argocd/application.yaml with your GitHub repo URL first!
kubectl apply -f argocd/application.yaml -n argocd
```

ArgoCD will now automatically sync your cluster with the `k8s/` directory.

---

### Step 5: Push Code — Trigger the Pipeline

```bash
git add .
git commit -m "feat: initial ecommerce app"
git push origin main
```

GitHub Actions will:
1. Run tests
2. Build and push Docker image
3. Commit updated image tag to `k8s/deployment.yaml`
4. ArgoCD detects the change and deploys automatically ✅

---

## 🔍 Verify Deployment

```bash
# Check pods
kubectl get pods -n ecommerce

# Check service
kubectl get svc -n ecommerce

# Port-forward for local testing
kubectl port-forward svc/ecommerce-svc 8080:80 -n ecommerce
# Visit: http://localhost:8080
```

---

## 🌐 App Endpoints

| Route | Description |
|-------|-------------|
| `/` | Product listing (with search & filter) |
| `/cart` | Shopping cart |
| `/add/<id>` | Add item to cart |
| `/remove/<id>` | Remove item from cart |
| `/health` | Health check (used by K8s probes) |

---

## 🔄 GitOps Flow (ArgoCD)

ArgoCD continuously reconciles the cluster state with Git:

- **Auto-sync**: Detects new commits in `k8s/` within ~3 minutes
- **Self-heal**: Reverts manual `kubectl` changes automatically
- **Prune**: Removes K8s resources deleted from Git

To view sync status:
```bash
# Using ArgoCD CLI
argocd app get ecommerce-app
argocd app sync ecommerce-app   # Manual sync if needed
```

---

## 🔧 Key Design Decisions

| Decision | Reason |
|----------|--------|
| **GitHub Actions over Jenkins** | No server to maintain, native GitHub integration |
| **ArgoCD for CD** | GitOps pattern — Git is the single source of truth |
| **Separate CI and CD** | Security: pipeline writes to Git, ArgoCD pulls (no cluster credentials in CI) |
| **Rolling Updates** | Zero-downtime deployments (`maxUnavailable: 0`) |
| **Non-root container** | Security best practice |
| **Gunicorn** | Production-grade WSGI server (not Flask dev server) |
