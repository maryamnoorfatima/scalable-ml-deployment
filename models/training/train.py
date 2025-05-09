import mlflow
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
from src.utils.mlflow_utils import setup_mlflow_tracking, log_model_metrics

def train_model():
    # Set up MLflow tracking
    setup_mlflow_tracking("innovate_analytics_experiment")
    
    # Load processed data
    data = pd.read_csv('data/processed/training_data.csv')
    X = data.drop('target', axis=1)
    y = data['target']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, average='weighted'),
        'recall': recall_score(y_test, y_pred, average='weighted')
    }
    
    # Log metrics and model to MLflow
    log_model_metrics(metrics)
    
    return model, metrics

if __name__ == "__main__":
    train_model() 