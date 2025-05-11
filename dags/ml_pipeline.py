from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import sys
from pathlib import Path

# Add absolute path to Python path
sys.path.append('/opt/airflow')

def _import_and_generate_data():
    """Import and run data generation"""
    from src.data.generate_dataset import generate_customer_data
    return generate_customer_data()

def _import_and_process_data():
    """Import and run data processing"""
    from src.data.preprocessing import preprocess_data
    input_path = 'data/raw/customer_transactions.csv'
    output_path = 'data/processed/processed_transactions.csv'
    return preprocess_data(input_path, output_path)

def _import_and_train():
    """Import and run model training"""
    import matplotlib
    matplotlib.use('Agg')  # Set non-interactive backend
    from src.models.train import train_model
    return train_model()

with DAG(
    'fraud_detection_pipeline',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'start_date': datetime(2024, 1, 1),
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    description='Fraud Detection ML Pipeline',
    schedule_interval=timedelta(days=1),
    catchup=False
) as dag:

    # Create necessary directories
    os.makedirs('/opt/airflow/data/raw', exist_ok=True)
    os.makedirs('/opt/airflow/data/processed', exist_ok=True)
    os.makedirs('/opt/airflow/models', exist_ok=True)

    generate_data_task = PythonOperator(
        task_id='generate_data',
        python_callable=_import_and_generate_data,
        dag=dag,
    )

    preprocess_task = PythonOperator(
        task_id='preprocess_data',
        python_callable=_import_and_process_data,
        dag=dag,
    )

    train_task = PythonOperator(
        task_id='train_model',
        python_callable=_import_and_train,
        dag=dag,
    )

    # Set task dependencies
    generate_data_task >> preprocess_task >> train_task 