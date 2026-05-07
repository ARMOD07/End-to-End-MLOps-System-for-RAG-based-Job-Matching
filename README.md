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
