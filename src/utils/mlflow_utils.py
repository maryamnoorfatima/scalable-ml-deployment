import mlflow
from mlflow.tracking import MlflowClient
from typing import Dict, Any

def setup_mlflow_tracking(experiment_name: str) -> None:
    """Initialize MLflow tracking"""
    mlflow.set_tracking_uri("http://localhost:5000")
    
    # Create experiment if it doesn't exist
    try:
        mlflow.create_experiment(experiment_name)
    except:
        pass
    mlflow.set_experiment(experiment_name)

def log_model_metrics(metrics: Dict[str, Any]) -> None:
    """Log metrics to MLflow"""
    with mlflow.start_run():
        for metric_name, value in metrics.items():
            mlflow.log_metric(metric_name, value)
        
        # Log model parameters from params.yaml
        mlflow.log_params(load_parameters())
        
        # Log the model
        mlflow.sklearn.log_model(model, "model") 