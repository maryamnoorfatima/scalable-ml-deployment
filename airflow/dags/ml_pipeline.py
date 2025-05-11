from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Import our functions
from src.data.generate_dataset import generate_customer_data
from src.data.preprocessing import preprocess_data
from src.models.train import train_model

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'fraud_detection_pipeline',
    default_args=default_args,
    description='Fraud Detection ML Pipeline',
    schedule_interval=timedelta(days=1),
    catchup=False
)

def generate_data():
    """Generate synthetic dataset"""
    generate_customer_data()

def process_data():
    """Preprocess the data"""
    input_path = 'data/raw/customer_transactions.csv'
    output_path = 'data/processed/processed_transactions.csv'
    preprocess_data(input_path, output_path)

def train():
    """Train the model"""
    train_model()

def _import_and_process_data():
    """Import and run data processing"""
    # First import sklearn to ensure it's available
    import sklearn
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    
    # Then import our preprocessing module
    from src.data.preprocessing import preprocess_data
    return preprocess_data()

# Define tasks
generate_data_task = PythonOperator(
    task_id='generate_data',
    python_callable=generate_data,
    dag=dag,
)

preprocess_task = PythonOperator(
    task_id='preprocess_data',
    python_callable=process_data,
    dag=dag,
)

train_task = PythonOperator(
    task_id='train_model',
    python_callable=train,
    dag=dag,
)

# Set task dependencies
generate_data_task >> preprocess_task >> train_task
