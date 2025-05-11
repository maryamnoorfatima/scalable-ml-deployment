import os
import subprocess
from dotenv import load_dotenv

def start_mlflow_server():
    load_dotenv()
    
    # Use the same port as your PostgreSQL connection
    mlflow_cmd = [
        "mlflow", "server",
        "--host", "0.0.0.0",
        "--port", "5000",
        "--backend-store-uri", "postgresql://mlflow:mlflow@localhost:5433/mlflow_db",
        "--default-artifact-root", "./mlruns"
    ]
    
    try:
        subprocess.run(mlflow_cmd)
    except KeyboardInterrupt:
        print("\nMLflow server stopped")

if __name__ == "__main__":
    start_mlflow_server() 