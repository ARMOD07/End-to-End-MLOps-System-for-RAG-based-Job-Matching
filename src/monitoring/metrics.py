from prometheus_client import Counter, Histogram, Gauge, generate_latest
import time
from functools import wraps
import logging

# Define metrics
MATCH_REQUESTS = Counter('match_requests_total', 'Total match requests', ['status'])
MATCH_DURATION = Histogram('match_duration_seconds', 'Match processing duration')
MATCH_SCORE = Gauge('match_score_percentage', 'Match score percentage')
EMBEDDING_QUALITY = Gauge('embedding_quality_score', 'Embedding quality metric')
ACTIVE_MODEL = Gauge('active_model_version', 'Currently active model version')

def monitor_performance(func):
    """Decorator to monitor function performance"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            MATCH_REQUESTS.labels(status='success').inc()
            return result
        except Exception as e:
            MATCH_REQUESTS.labels(status='error').inc()
            raise e
        finally:
            duration = time.time() - start_time
            MATCH_DURATION.observe(duration)
    return wrapper

class MonitoringManager:
    def __init__(self):
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/monitoring.log'),
                logging.StreamHandler()
            ]
        )
    
    def update_match_metrics(self, score: float):
        MATCH_SCORE.set(score)
    
    def update_model_version(self, version: int):
        ACTIVE_MODEL.set(version)