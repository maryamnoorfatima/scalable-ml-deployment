from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.data.preprocessing import preprocess_data, load_data, save_processed_data
from src.models.train import main as train_main

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
    'ml_training_pipeline',
    default_args=default_args,
    description='ML model training pipeline',
    schedule_interval=timedelta(days=1),
)

def run_preprocessing():
    """Run data preprocessing"""
    df = load_data('data/raw/dataset.csv')
    processed_df = preprocess_data(df)
    save_processed_data(processed_df, 'data/processed/processed_dataset.csv')

def run_training():
    """Run model training"""
    train_main()

preprocess_task = PythonOperator(
    task_id='preprocess_data',
    python_callable=run_preprocessing,
    dag=dag,
)

train_task = PythonOperator(
    task_id='train_model',
    python_callable=run_training,
    dag=dag,
)

preprocess_task >> train_task
