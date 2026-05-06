from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import pandas as pd
from pathlib import Path

default_args = {
    'owner': 'mlops',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

def ingest_data(**context):
    """Ingest job offers from source"""
    # In production: read from S3, database, or API
    import json
    sample_data = [
        {"job_id": 1, "title": "ML Engineer", "description": "..."},
        {"job_id": 2, "title": "Data Scientist", "description": "..."}
    ]
    
    # Save to shared location
    with open('/tmp/job_data.json', 'w') as f:
        json.dump(sample_data, f)
    
    return {'num_jobs': len(sample_data)}

def preprocess_data(**context):
    """Clean and preprocess job descriptions"""
    import json
    import re
    
    with open('/tmp/job_data.json', 'r') as f:
        data = json.load(f)
    
    for job in data:
        # Clean text
        job['cleaned_description'] = re.sub(r'[^\w\s]', '', job['description'])
    
    with open('/tmp/processed_jobs.json', 'w') as f:
        json.dump(data, f)
    
    return {'processed_count': len(data)}

def generate_embeddings(**context):
    """Generate embeddings for job descriptions"""
    import json
    from sentence_transformers import SentenceTransformer
    
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    with open('/tmp/processed_jobs.json', 'r') as f:
        data = json.load(f)
    
    embeddings = []
    for job in data:
        embedding = model.encode(job['cleaned_description'])
        embeddings.append(embedding.tolist())
        job['embedding'] = embedding.tolist()
    
    with open('/tmp/embedded_jobs.json', 'w') as f:
        json.dump(data, f)
    
    return {'embeddings_generated': len(embeddings)}

def store_in_faiss(**context):
    """Store embeddings in FAISS index"""
    import json
    import faiss
    import numpy as np
    
    with open('/tmp/embedded_jobs.json', 'r') as f:
        data = json.load(f)
    
    embeddings = np.array([job['embedding'] for job in data])
    dimension = embeddings.shape[1]
    
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    
    faiss.write_index(index, '/tmp/job_index.faiss')
    
    return {'index_size': index.ntotal}

def evaluate_pipeline(**context):
    """Evaluate pipeline performance and log to MLflow"""
    import mlflow
    
    with mlflow.start_run(run_name="airflow_pipeline"):
        mlflow.log_param("num_jobs", context['task_instance'].xcom_pull(task_ids='ingest_data')['num_jobs'])
        mlflow.log_metric("index_size", context['task_instance'].xcom_pull(task_ids='store_in_faiss')['index_size'])

# Define DAG
dag = DAG(
    'job_matching_pipeline',
    default_args=default_args,
    description='End-to-end job matching pipeline',
    schedule_interval='@daily',
    catchup=False,
    tags=['mlops', 'job_matching']
)

# Define tasks
ingest_task = PythonOperator(
    task_id='ingest_data',
    python_callable=ingest_data,
    dag=dag
)

preprocess_task = PythonOperator(
    task_id='preprocess_data',
    python_callable=preprocess_data,
    dag=dag
)

embedding_task = PythonOperator(
    task_id='generate_embeddings',
    python_callable=generate_embeddings,
    dag=dag
)

store_task = PythonOperator(
    task_id='store_in_faiss',
    python_callable=store_in_faiss,
    dag=dag
)

evaluate_task = PythonOperator(
    task_id='evaluate_pipeline',
    python_callable=evaluate_pipeline,
    dag=dag
)

# Set dependencies
ingest_task >> preprocess_task >> embedding_task >> store_task >> evaluate_task