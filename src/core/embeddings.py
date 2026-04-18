import mlflow
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List
import logging

logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    def __init__(self, model_name: str = settings.embedding_model):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.dimension = settings.embedding_dim
        
    @mlflow.trace(name="generate_embeddings")
    def generate(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for a list of texts"""
        with mlflow.start_span(name="embedding_generation"):
            embeddings = self.model.encode(texts, show_progress_bar=False)
            
            # Log metadata
            mlflow.log_params({
                "model_name": self.model_name,
                "num_texts": len(texts),
                "embedding_dim": embeddings.shape[1]
            })
            
        return embeddings
    
    def generate_single(self, text: str) -> np.ndarray:
        return self.generate([text])[0]