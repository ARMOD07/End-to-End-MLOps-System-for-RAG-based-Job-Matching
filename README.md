# End-to-End MLOps System for RAG-based Job Matching

title: Job Matching MLOps
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8000

# 🔍 Job Matching MLOps

> CV ↔ job offer matching system with online serving, batch pipeline, drift monitoring, and MLflow experiment tracking — deployed on Hugging Face Spaces.

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=flat-square&logo=fastapi&logoColor=white)
![MLflow](https://img.shields.io/badge/MLflow-tracking-0194E2?style=flat-square&logo=mlflow&logoColor=white)
![HF Spaces](https://img.shields.io/badge/HuggingFace-Spaces-FFD21E?style=flat-square&logo=huggingface&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## Table of Contents

- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Running Tests](#running-tests)
- [Deployment](#deployment)
- [Monitoring](#monitoring)
- [License](#license)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              USER INTERFACE                              │
│                         Streamlit (Hugging Face Spaces)                  │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           API GATEWAY / FastAPI                          │
│                    (Load Balancer, Auth, Rate Limiting)                  │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              ▼                       ▼                       ▼
┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐
│   Online Serving    │   │  Streaming Layer    │   │   Batch Pipeline    │
│   (FastAPI + LLM)   │   │  (Kinesis + Lambda) │   │   (Airflow/Prefect) │
└─────────────────────┘   └─────────────────────┘   └─────────────────────┘
              │                       │                       │
              └───────────────────────┼───────────────────────┘
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          VECTOR DATABASE (FAISS)                         │
│                         + PostgreSQL (Metadata)                          │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         MLflow Tracking Server                           │
│                    (Experiments, Registry, Metrics)                      │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    MONITORING STACK (Prometheus + Grafana)               │
│                         + Evidently AI (Drift Detection)                 │
└─────────────────────────────────────────────────────────────────────────┘
```

### Components

| Component | Description |
|---|---|
| **Online Serving** | FastAPI + LLM router for real-time inference. CV/JD requests → matching score + explanation |
| **Streaming Layer** | Kinesis producer + Lambda mock for continuous job offer ingestion |
| **Batch Pipeline** | Airflow/Prefect DAGs to periodically re-index the vector store |
| **Monitoring** | Prometheus + Grafana for operational metrics, Evidently AI for semantic drift detection |

---

## Tech Stack

| Category | Tools |
|---|---|
| **Embeddings & Retrieval** | `sentence-transformers`, `FAISS`, `pgvector` |
| **LLM & Orchestration** | `LangChain`, `OpenAI API`, `Pydantic` |
| **MLOps** | `MLflow`, `Airflow`, `Evidently AI` |
| **API & Serving** | `FastAPI`, `Uvicorn`, `Pydantic` |
| **Infrastructure** | `Docker`, `Docker Compose`, `Terraform` |
| **CI/CD** | `GitHub Actions`, `pre-commit` |
| **Observability** | `Prometheus`, `Grafana` |
| **Frontend** | `Streamlit`, `Hugging Face Spaces` |

---

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Git

### 1. Clone & install

```bash
git clone https://github.com/ARMOD07/End-to-End-MLOps-System-for-RAG-based-Job-Matching 
cd End-to-End-MLOps-System-for-RAG-based-Job-Matching 

python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt

# Dev tools (pre-commit, pytest, flake8)
pip install -r requirements-dev.txt
```

### 2. Configure environment variables

```bash
cp .env.example .env
# Edit .env and fill in required keys (see Environment Variables section)
```

### 3. Start with Docker Compose

```bash
docker-compose up --build
```

Services will be available at:

| Service | URL |
|---|---|
| FastAPI | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| MLflow | http://localhost:5000 |
| Grafana | http://localhost:3000 |
| Prometheus | http://localhost:9090 |

### 4. Seed data & launch Streamlit

```bash
# Inject sample job offers into FAISS
python scripts/seed_data.py

# Open the user interface
streamlit run frontend/streamlit_app.py
```

---

## Environment Variables

Copy `.env.example` to `.env` and configure the following:

| Variable | Required | Description |
|---|---|---|
| `OPENAI_API_KEY` | ✅ Required | OpenAI key for the LLM router |
| `DATABASE_URL` | ✅ Required | PostgreSQL URI for metadata storage |
| `FAISS_INDEX_PATH` | ✅ Required | Path to the persisted FAISS index |
| `MLFLOW_TRACKING_URI` | Optional | Defaults to `http://localhost:5000` |
| `AWS_KINESIS_STREAM` | Optional | Required only for real Kinesis streaming |
| `AWS_REGION` | Optional | AWS region (default: `us-east-1`) |
| `HF_TOKEN` | Optional | Hugging Face token for automated deployment |
| `SECRET_KEY` | Optional | API auth secret key |

---

## API Endpoints

### Matching

```
POST /api/v1/match
```

Request body:
```json
{
  "cv_text": "string",
  "job_description": "string",
  "top_k": 5
}
```

Response:
```json
{
  "match_score": 0.87,
  "explanation": "string",
  "similar_jobs": [...],
  "processing_time_ms": 142
}
```

### Other endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/health` | Service health check |
| `POST` | `/api/v1/admin/reindex` | Force FAISS re-indexing |
| `GET` | `/api/v1/admin/stats` | Index statistics |
| `GET` | `/metrics` | Prometheus metrics scrape endpoint |

Full interactive documentation available at `/docs` (Swagger UI) and `/redoc`.

---

## Project Structure

```
job-matching-mlops/
├── .github/workflows/          # CI/CD pipelines
│   ├── ci.yml                  # Lint, test, build
│   └── deploy.yml              # Auto-deploy to HF Spaces
├── src/
│   ├── api/                    # FastAPI app, routes, schemas
│   ├── core/                   # Embeddings, FAISS, LLM router, matcher
│   ├── models/                 # CV & job description processors
│   ├── pipelines/              # Training, inference, batch pipelines
│   ├── monitoring/             # Prometheus metrics, Evidently drift
│   ├── streaming/              # Kinesis producer, Lambda mock
│   └── utils/                  # MLflow utils, validators
├── tests/
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests (requires Docker)
│   └── fixtures/               # Sample CV & job PDF fixtures
├── airflow/dags/               # Airflow DAGs for batch & monitoring
├── mlflow/                     # MLflow tracking artifacts
├── dashboards/                 # Grafana & Prometheus configs
├── terraform/                  # Infrastructure as code
├── frontend/                   # Streamlit app & pages
├── scripts/                    # Setup, deploy, seed scripts
├── docker-compose.yml
├── Dockerfile
└── pyproject.toml
```

---

## Running Tests

```bash
# Unit tests
pytest tests/unit/ -v

# Integration tests (requires running Docker services)
pytest tests/integration/ -v

# Full coverage report
pytest --cov=src --cov-report=html
open htmlcov/index.html

# Pre-commit hooks (lint + format)
pre-commit run --all-files
```

---

## Deployment

### Hugging Face Spaces (automatic)

The `.github/workflows/deploy.yml` workflow automatically pushes to HF Spaces on every merge to `main`.

> **Setup:** Add `HF_TOKEN` as a GitHub repository secret before enabling the workflow.

### Manual deployment

```bash
bash scripts/deploy_hf_space.sh
```

### Terraform (cloud infrastructure)

```bash
cd terraform/
terraform init
terraform plan
terraform apply
```

---

## Monitoring

### Drift detection

Evidently AI reports are generated automatically by the `monitoring_dag.py` Airflow DAG. Reports are saved to `mlflow/mlruns/` and linked to the corresponding MLflow run.

### Grafana dashboards

Pre-built dashboards are in `dashboards/grafana/dashboards.yaml`. Import them via the Grafana UI or mount them as a provisioned datasource.

Key metrics tracked:

- Embedding cosine similarity distribution over time
- API latency (p50, p95, p99)
- Match score distribution drift
- Request volume and error rate

### MLflow experiment tracking

```bash
# Start MLflow UI
python mlflow/mlflow_server.py

# Or via CLI
mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
```

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Commit using conventional commits: `git commit -m "feat: add X"`
4. Open a pull request against `main`

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

*Built by [Amira](https://github.com/ARMOD07) · ML Engineer & Data Scientist*
