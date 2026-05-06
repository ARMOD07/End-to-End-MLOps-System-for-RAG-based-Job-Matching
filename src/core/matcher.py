import numpy as np
from typing import Dict, Tuple
from sklearn.metrics.pairwise import cosine_similarity
import mlflow

class JobMatcher:
    def __init__(self, embedding_generator, vector_store):
        self.embedding_generator = embedding_generator
        self.vector_store = vector_store
        
    @mlflow.trace(name="job_matching")
    def match(self, job_text: str, cv_text: str) -> Dict[str, any]:
        """Compute match score between job and CV"""
        
        # Generate embeddings
        job_embedding = self.embedding_generator.generate_single(job_text)
        cv_embedding = self.embedding_generator.generate_single(cv_text)
        
        # Compute similarity
        similarity = cosine_similarity(
            job_embedding.reshape(1, -1),
            cv_embedding.reshape(1, -1)
        )[0][0]
        
        # Convert to percentage
        match_score = float(similarity * 100)
        
        # Find relevant skills match (keyword-based)
        job_keywords = self._extract_keywords(job_text)
        cv_keywords = self._extract_keywords(cv_text)
        
        matched_keywords = set(job_keywords) & set(cv_keywords)
        missing_keywords = set(job_keywords) - set(cv_keywords)
        
        skills_match_score = (len(matched_keywords) / len(job_keywords)) * 100 if job_keywords else 0
        
        # Final weighted score
        final_score = (match_score * 0.6 + skills_match_score * 0.4)
        
        # Decision logic
        if final_score >= 80:
            decision = "Strongly Recommended"
        elif final_score >= 60:
            decision = "Recommended"
        elif final_score >= 40:
            decision = "Consider with Improvements"
        else:
            decision = "Not Recommended"
        
        # Log to MLflow
        mlflow.log_metrics({
            "similarity_score": match_score,
            "skills_match_score": skills_match_score,
            "final_match_score": final_score
        })
        
        return {
            "match_score": round(final_score, 2),
            "similarity_score": round(match_score, 2),
            "skills_match_score": round(skills_match_score, 2),
            "decision": decision,
            "strengths": list(matched_keywords)[:5],
            "gaps": list(missing_keywords)[:5],
            "improvement_suggestions": self._generate_suggestions(missing_keywords)
        }
    
    def _extract_keywords(self, text: str) -> set:
        """Extract keywords from text (simplified)"""
        # In production, use NLP libraries like spaCy
        common_skills = ["python", "java", "sql", "aws", "docker", "kubernetes", 
                        "machine learning", "data science", "react", "nodejs"]
        text_lower = text.lower()
        return {skill for skill in common_skills if skill in text_lower}
    
    def _generate_suggestions(self, missing_keywords: set) -> list:
        """Generate improvement suggestions"""
        return [f"Consider learning or highlighting experience with {kw}" 
                for kw in missing_keywords] 
        
        