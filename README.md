# 🛒 ShopWave — Python Ecommerce App on Kubernetes

![CI/CD](https://github.com/rkdasari77/python-argocd-kubernetes/actions/workflows/ci-cd.yml/badge.svg)
![Docker](https://img.shields.io/badge/Docker-Hub-2496ED?logo=docker)
![Kubernetes](https://img.shields.io/badge/Kubernetes-AKS-326CE5?logo=kubernetes)
![ArgoCD](https://img.shields.io/badge/GitOps-ArgoCD-EF7B4D?logo=argo)
![Azure](https://img.shields.io/badge/Cloud-Azure-0078D4?logo=microsoftazure)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python)

> A production-grade GitOps CI/CD pipeline that automatically tests, builds, and deploys a Python ecommerce app to Azure Kubernetes Service on every code push — zero manual steps.

---

## 📸 Architecture

![ShopWave GitOps Architecture](shopwave_arch_linkedin_v3.png)

---

## 🏗️ Pipeline Flow

```
Developer (git push)
        │
        ▼
GitHub (App Repo)
        │  webhook trigger
        ▼
GitHub Actions
  ├── Job 1: Run pytest tests
  ├── Job 2: Build & push Docker image → Docker Hub
  └── Job 3: Update image tag in k8s/deployment.yaml
                        │
                        │  ArgoCD polls every 3 min
                        ▼
                     ArgoCD
                        │  rolling deploy (zero downtime)
                        ▼
              Azure AKS Cluster
              ├── Pod 1 (shopwave)
              ├── Pod 2 (shopwave)
              └── Azure LoadBalancer → Public IP
```

---

## 🔧 Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Application | Python 3.12 + Flask | Ecommerce web application |
| Web Server | Gunicorn | Production WSGI server |
| Containerization | Docker | App packaging |
| Image Registry | Docker Hub | Versioned image storage |
| CI Pipeline | GitHub Actions | Test, build, push |
| CD / GitOps | ArgoCD | Kubernetes continuous delivery |
| Orchestration | Kubernetes | Container management |
| Cloud Platform | Azure AKS | Managed Kubernetes cluster |

---

## 📁 Project Structure

```
python-argocd-kubernetes/
│
├── app/                        # All Python source files
│   ├── app.py                  # Flask ecommerce application
│   ├── requirements.txt        # Python dependencies
│   ├── test_app.py             # Pytest test suite
│   └── templates/
│       ├── index.html          # Product listing page
│       └── cart.html           # Shopping cart page
│
├── Dockerfile                  # Container definition
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml           # GitHub Actions 3-job pipeline
│
├── k8s/                        # Kubernetes manifests
│   ├── namespace.yaml
│   ├── deployment.yaml         # Auto-updated by pipeline
│   └── service.yaml            # Azure LoadBalancer
│
└── argocd/
    └── application.yaml        # ArgoCD Application definition
```

---

## 🌐 Application

A lightweight Python Flask ecommerce site with the following pages:

| Route | Description |
|---|---|
| `/` | Product listing with category filter |
| `/cart` | Shopping cart with item management |
| `/add/<id>` | Add product to cart |
| `/remove/<id>` | Remove product from cart |
| `/health` | Health check — used by Kubernetes probes |

---

## ⚙️ CI/CD Pipeline — GitHub Actions

The pipeline has 3 jobs that run sequentially on every push to `main`:

**Job 1 — Run Tests**
- Sets up Python 3.12
- Installs dependencies
- Runs `pytest` against `app/test_app.py`
- Pipeline stops here if any test fails

**Job 2 — Build & Push Docker Image**
- Builds Docker image from `Dockerfile`
- Tags with both `:latest` and `:sha-xxxxxxx` (commit SHA)
- Pushes both tags to Docker Hub

**Job 3 — Update K8s Manifest**
- Updates the `image:` field in `k8s/deployment.yaml` with the new SHA tag
- Commits the change back to the repository via `github-actions[bot]`
- This commit is what triggers ArgoCD to redeploy

---

## 🔄 GitOps with ArgoCD

ArgoCD watches the `k8s/` folder in this repository and automatically syncs the cluster state with Git.

**Key behaviours:**

| Feature | Description |
|---|---|
| Auto-sync | Detects manifest changes and deploys automatically |
| Self-heal | Reverts any manual `kubectl` changes back to Git state |
| Prune | Removes Kubernetes resources deleted from Git |
| Zero downtime | `maxUnavailable: 0` keeps pods running during updates |

**Why SHA tags instead of `latest`?**
ArgoCD detects changes by comparing the Git manifest with the cluster state. If the image tag never changes (e.g. always `latest`), ArgoCD sees no diff and does not redeploy. Using a unique SHA tag per commit ensures every push triggers a fresh deployment.

---

## ☸️ Kubernetes Resources

**Namespace:** `shopwave`

**Deployment**
- 2 replicas for high availability
- Rolling update strategy with `maxUnavailable: 0`
- Liveness probe — restarts unhealthy pods automatically
- Readiness probe — only routes traffic to ready pods
- Resource limits defined (CPU + memory)

**Service**
- Type: `LoadBalancer`
- Azure automatically provisions a public IP
- Routes external traffic on port 80 to pods on port 5000

---

## 🧪 Test Coverage

```
test_app.py::test_health            ✅
test_app.py::test_homepage          ✅
test_app.py::test_products_listed   ✅
test_app.py::test_cart_empty        ✅
test_app.py::test_add_to_cart       ✅
test_app.py::test_remove_from_cart  ✅

6 passed
```

---

## 📊 Pipeline Duration

| Stage | Duration |
|---|---|
| Job 1 — Tests | ~30 seconds |
| Job 2 — Build & Push | ~2 minutes |
| Job 3 — Update Manifest | ~15 seconds |
| ArgoCD Sync | ~1–3 minutes |
| **Total: push → live** | **~5–7 minutes** |

---

## 🔐 Security Practices

- Container runs as a **non-root user**
- No secrets hardcoded — managed via GitHub Secrets and Kubernetes Secrets
- Image pinned to **SHA tag** — prevents silent image changes
- Health probes ensure only healthy pods receive traffic

---

## 💡 Key Learnings

- GitOps pattern — Git as the single source of truth for cluster state
- Pull-based CD is more secure than push-based (ArgoCD pulls vs pipeline pushing)
- SHA image tags are essential for GitOps to detect and trigger redeployments
- ArgoCD self-heal protects against configuration drift in production
- Rolling updates with `maxUnavailable: 0` guarantee zero-downtime deployments
- Azure LoadBalancer public IPs are limited on free subscriptions — plan service types accordingly

---

## 📬 Author

**Raj Kumar Dasari**
- GitHub: [@rkdasari77](https://github.com/rkdasari77)

---

> ⭐ If this project helped you, give it a star!
