import faiss
import pickle
import numpy as np
from typing import List, Tuple, Dict
import sqlite3
from pathlib import Path

class VectorStore:
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.metadata_db = settings.metadata_db_path
        self._init_db()
        
    def _init_db(self):
        conn = sqlite3.connect(self.metadata_db)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY,
                vector_id INTEGER,
                content TEXT,
                doc_type TEXT,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
    
    def add_documents(self, vectors: np.ndarray, documents: List[Dict]):
        """Add documents to FAISS index with metadata"""
        start_id = self.index.ntotal
        self.index.add(vectors)
        
        conn = sqlite3.connect(self.metadata_db)
        cursor = conn.cursor()
        
        for i, doc in enumerate(documents):
            cursor.execute("""
                INSERT INTO documents (vector_id, content, doc_type, metadata)
                VALUES (?, ?, ?, ?)
            """, (start_id + i, doc['content'], doc['type'], str(doc['meta'])))
        
        conn.commit()
        conn.close()
    
    def search(self, query_vector: np.ndarray, k: int = 5) -> List[Tuple[float, Dict]]:
        """Search similar documents"""
        distances, indices = self.index.search(query_vector.reshape(1, -1), k)
        
        conn = sqlite3.connect(self.metadata_db)
        cursor = conn.cursor()
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            cursor.execute("SELECT content, doc_type, metadata FROM documents WHERE vector_id = ?", (int(idx),))
            row = cursor.fetchone()
            if row:
                results.append((float(dist), {
                    'content': row[0],
                    'type': row[1],
                    'metadata': eval(row[2]) if row[2] else {}
                }))
        
        conn.close()
        return results
    
    def save(self, path: str):
        """Save FAISS index"""
        faiss.write_index(self.index, f"{path}.faiss")
        with open(f"{path}.pkl", 'wb') as f:
            pickle.dump({'dimension': self.dimension}, f)
    
    def load(self, path: str):
        """Load FAISS index"""
        self.index = faiss.read_index(f"{path}.faiss")