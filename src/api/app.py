from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
import uvicorn
from typing import Optional
import asyncio

app = FastAPI(title="Job Matching API", version="1.0.0")

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metrics
instrumentator = Instrumentator().instrument(app)

@app.on_event("startup")
async def startup_event():
    instrumentator.expose(app)
    # Initialize components
    from src.core.embeddings import EmbeddingGenerator
    from src.core.vector_store import VectorStore
    from src.core.matcher import JobMatcher
    
    app.state.embedding_gen = EmbeddingGenerator()
    app.state.vector_store = VectorStore()
    app.state.matcher = JobMatcher(app.state.embedding_gen, app.state.vector_store)

@app.post("/api/v1/match")
async def match_job(
    job_file: Optional[UploadFile] = File(None),
    cv_file: Optional[UploadFile] = File(None),
    job_text: Optional[str] = None,
    cv_text: Optional[str] = None
):
    """Match job offer with CV"""
    
    # Extract text from files
    if job_file:
        job_text = await job_file.read()
        job_text = job_text.decode()
    if cv_file:
        cv_text = await cv_file.read()
        cv_text = cv_text.decode()
    
    if not job_text or not cv_text:
        raise HTTPException(status_code=400, detail="Missing job or CV text")
    
    # Perform matching
    result = app.state.matcher.match(job_text, cv_text)
    
    return result

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)