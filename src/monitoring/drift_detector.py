from evidently.model_monitoring import ModelMonitoring
from evidently.metrics import DataDriftTable, ColumnDriftMetric
import pandas as pd
from datetime import datetime

class DriftDetector:
    def __init__(self):
        self.monitoring = ModelMonitoring(
            metrics=[
                DataDriftTable(),
                ColumnDriftMetric(column_name='match_score'),
                ColumnDriftMetric(column_name='embedding_norm')
            ],
            options={
                'calculate_metrics': True,
                'reference_data': None
            }
        )
    
    def set_reference(self, reference_data: pd.DataFrame):
        """Set reference dataset for drift detection"""
        self.monitoring.options['reference_data'] = reference_data
    
    def detect_drift(self, current_data: pd.DataFrame):
        """Detect drift in current predictions"""
        results = self.monitoring.calculate(current_data)
        
        drift_report = {
            'timestamp': datetime.now(),
            'data_drift_detected': results['data_drift'].drift_detected,
            'drifted_columns': results['data_drift'].drifted_columns,
            'match_score_drift': results['column_drift_match_score'].drift_detected
        }
        
        # Log drift metrics
        if drift_report['data_drift_detected']:
            logging.warning(f"Data drift detected: {drift_report['drifted_columns']}")
        
        return drift_report
    
    def save_drift_report(self, report, path: str):
        """Save drift report to file"""
        import json
        with open(f"{path}/drift_report_{datetime.now().strftime('%Y%m%d')}.json", 'w') as f:
            json.dump(report, f, default=str)