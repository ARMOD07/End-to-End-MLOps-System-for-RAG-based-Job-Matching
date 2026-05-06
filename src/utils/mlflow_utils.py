import mlflow
from mlflow.tracking import MlflowClient
from mlflow.entities import ViewType
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class MLflowManager:
    def __init__(self):
        mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
        self.client = MlflowClient()
        
    def create_experiment(self, experiment_name: str):
        """Create or get experiment"""
        try:
            experiment_id = mlflow.create_experiment(experiment_name)
        except:
            experiment_id = mlflow.get_experiment_by_name(experiment_name).experiment_id
        
        mlflow.set_experiment(experiment_name)
        return experiment_id
    
    def log_match_evaluation(self, 
                            run_name: str,
                            params: Dict[str, Any],
                            metrics: Dict[str, float],
                            artifacts: Dict[str, str] = None):
        """Log matching evaluation to MLflow"""
        with mlflow.start_run(run_name=run_name):
            # Log parameters
            for key, value in params.items():
                mlflow.log_param(key, value)
            
            # Log metrics
            for key, value in metrics.items():
                mlflow.log_metric(key, value)
            
            # Log artifacts
            if artifacts:
                for name, path in artifacts.items():
                    mlflow.log_artifact(path, artifact_path=name)
            
            # Register model if metrics meet threshold
            if metrics.get('match_accuracy', 0) > 0.8:
                model_uri = f"runs:/{mlflow.active_run().info.run_id}/model"
                mlflow.register_model(model_uri, "JobMatchingModel")
    
    def get_best_model(self, metric: str = "match_accuracy"):
        """Get best model from registry"""
        best_model = self.client.get_latest_versions("JobMatchingModel", stages=["Production"])
        if best_model:
            return best_model[0]
        return None
    
    def transition_model_stage(self, model_name: str, version: int, stage: str):
        """Transition model to different stage"""
        self.client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage=stage
        )