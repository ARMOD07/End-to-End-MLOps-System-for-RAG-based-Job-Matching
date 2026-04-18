from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # API Settings
    api_version: str = "v1"
    debug: bool = False
    
    # Model Settings
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dim: int = 384
    llm_model: str = "gpt-3.5-turbo"  # or "meta-llama/Llama-2-7b"
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # Vector Store
    faiss_index_path: str = "data/faiss_index"
    metadata_db_path: str = "data/metadata.db"
    
    # MLflow
    mlflow_tracking_uri: str = "http://localhost:5000"
    mlflow_experiment_name: str = "job_matching"
    
    # Monitoring
    prometheus_port: int = 8001
    enable_drift_detection: bool = True
    
    # AWS (Optional)
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    kinesis_stream_name: str = "job-matching-stream"
    
    class Config:
        env_file = ".env"

settings = Settings()