import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import mlflow
import joblib
import json
import os

def train_model():
    # Load processed data
    df = pd.read_csv('data/processed/processed_transactions.csv')
    
    # Separate features and target
    X = df.drop('is_fraudulent', axis=1)
    y = df['is_fraudulent']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Calculate metrics
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    # Save metrics
    metrics = {
        'train_accuracy': train_score,
        'test_accuracy': test_score
    }
    
    with open('metrics.json', 'w') as f:
        json.dump(metrics, f)
    
    # Save model
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/model.pkl')

if __name__ == "__main__":
    train_model()