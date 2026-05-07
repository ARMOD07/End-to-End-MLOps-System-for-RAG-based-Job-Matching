# End-to-End MLOps System for RAG-based Job Matching

title: Job Matching MLOps
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8000


job-matching-mlops/
├── .github/
│   └── workflows/
│       ├── ci.yml                 # CI/CD pipeline
│       └── deploy.yml             # Deployment to HF Spaces
├── .pre-commit-config.yaml
├── .flake8
├── .gitignore
├── pyproject.toml
├── README.md
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
├── docker-compose.yml
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── src/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── app.py                 # FastAPI main app
│   │   ├── routes/
│   │   │   ├── match.py
│   │   │   ├── health.py
│   │   │   └── admin.py
│   │   └── schemas/
│   │       ├── request.py
│   │       └── response.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py              # Configuration management
│   │   ├── embeddings.py          # Embedding generation
│   │   ├── vector_store.py        # FAISS operations
│   │   ├── llm_router.py          # LLM reasoning
│   │   ├── matcher.py             # Matching logic
│   │   └── preprocessing.py       # Text preprocessing
│   ├── models/
│   │   ├── __init__.py
│   │   ├── cv_processor.py
│   │   └── job_processor.py
│   ├── pipelines/
│   │   ├── __init__.py
│   │   ├── training_pipeline.py   # Model training
│   │   ├── inference_pipeline.py  # Online inference
│   │   └── batch_pipeline.py      # Batch processing
│   ├── monitoring/
│   │   ├── __init__.py
│   │   ├── metrics.py             # Prometheus metrics
│   │   ├── drift_detector.py      # Evidently AI
│   │   └── logger.py              # Prediction logging
│   ├── streaming/
│   │   ├── __init__.py
│   │   ├── kinesis_producer.py
│   │   └── lambda_function.py     # AWS Lambda mock
│   └── utils/
│       ├── __init__.py
│       ├── mlflow_utils.py        # MLflow integration
│       └── validators.py
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── test_embeddings.py
│   │   ├── test_matcher.py
│   │   └── test_preprocessing.py
│   ├── integration/
│   │   ├── test_api.py
│   │   └── test_vector_store.py
│   └── fixtures/
│       ├── sample_cv.pdf
│       └── sample_job.pdf
├── notebooks/
│   └── experiment_tracking_demo.ipynb
├── airflow/
│   ├── dags/
│   │   ├── job_matching_dag.py
│   │   └── monitoring_dag.py
│   └── plugins/
├── mlflow/
│   ├── mlruns/                    # MLflow artifacts
│   └── mlflow_server.py
├── dashboards/
│   ├── grafana/
│   │   └── dashboards.yaml
│   └── prometheus/
│       └── prometheus.yml
├── scripts/
│   ├── setup.sh
│   ├── deploy_hf_space.sh
│   └── seed_data.py
└── frontend/
    ├── streamlit_app.py
    ├── pages/
    │   ├── 1_Match_Job.py
    │   ├── 2_Monitoring.py
    │   └── 3_Experiments.py
    └── components/

    🔍 Job Matching MLOps
Système de matching CV ↔ offre d'emploi avec serving en ligne, pipeline batch, monitoring de drift et traçabilité via MLflow — déployé sur Hugging Face Spaces.
Python 3.11
FastAPI
FAISS + PostgreSQL
MLflow
HF Spaces
Evidently AI
Docker
Architecture système
Serving en ligne
FastAPI + LLM router pour l'inférence temps-réel. Requêtes CV/JD → score de matching + explication via src/api/routes/match.py.
Streaming layer
Kinesis producer + Lambda mock pour l'ingestion continue de nouvelles offres. Voir src/streaming/.
Pipeline batch
Airflow/Prefect DAGs pour réindexer la base vectorielle périodiquement. DAGs dans airflow/dags/.
Monitoring
Prometheus + Grafana pour les métriques opérationnelles. Evidently AI pour la détection de drift sémantique.
Stack technique
Embeddings & retrieval
sentence-transformers
FAISS
pgvector
LLM & orchestration
LangChain
OpenAI API
Pydantic
MLOps
MLflow
Airflow
Evidently
Infrastructure
Docker
Terraform
GitHub Actions
Observabilité
Prometheus
Grafana
Frontend
Streamlit
HF Spaces
Installation rapide
1
Cloner & installer
Cloner le dépôt et installer les dépendances dans un environnement virtuel.
git clone https://github.com/ARMOD07/job-matching-mlops
cd job-matching-mlops
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# Dev tools (pre-commit, pytest, flake8)
pip install -r requirements-dev.txt
2
Configurer les variables d'environnement
Copier .env.example → .env et renseigner les clés.
cp .env.example .env
3
Lancer avec Docker Compose
Lance l'API FastAPI, le serveur MLflow, Prometheus et Grafana en une commande.
docker-compose up --build
# API     → http://localhost:8000
# MLflow  → http://localhost:5000
# Grafana → http://localhost:3000
4
Seeder les données & démarrer Streamlit
Injecter des offres exemples dans FAISS puis ouvrir l'interface utilisateur.
python scripts/seed_data.py
streamlit run frontend/streamlit_app.py
Variables d'environnement
OPENAI_API_KEYrequis
Clé OpenAI pour le LLM router
DATABASE_URLrequis
URI PostgreSQL (metadata)
FAISS_INDEX_PATHrequis
Chemin vers l'index FAISS persisté
MLFLOW_TRACKING_URIoptionnel
Par défaut http://localhost:5000
AWS_KINESIS_STREAMoptionnel
Requis uniquement pour le streaming réel
HF_TOKENoptionnel
Déploiement automatique sur HF Spaces
Endpoints API
POST
/api/v1/match
Matching CV ↔ offre d'emploi
GET
/api/v1/health
Santé du service
POST
/api/v1/admin/reindex
Forcer la réindexation FAISS
GET
/metrics
Métriques Prometheus
Tests
# Tests unitaires
pytest tests/unit/ -v
# Tests d'intégration (nécessite Docker)
pytest tests/integration/ -v
# Couverture complète
pytest --cov=src --cov-report=html
Déploiement HF Spaces
CI/CD automatique — le workflow .github/workflows/deploy.yml pousse sur HF Spaces à chaque merge sur main. Vérifier que HF_TOKEN est bien configuré en secret GitHub.
# Déploiement manuel
bash scripts/deploy_hf_space.sh
Modules principaux
src/core/
Embeddings, FAISS, LLM router, matching logic et preprocessing. Cœur du système.
src/pipelines/
Training pipeline, inference pipeline et batch processing (Airflow-compatible).
src/monitoring/
Métriques Prometheus, détection de drift Evidently AI et logging des prédictions.
src/streaming/
Kinesis producer + Lambda mock pour simuler l'ingestion d'offres en temps réel.
Amira — github.com/ARMOD07
