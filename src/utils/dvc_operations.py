import os
import subprocess
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def run_command(command):
    """Run a shell command and log output"""
    logger = setup_logging()
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        logger.info(f"Command '{command}' executed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing command '{command}': {e.stderr}")
        raise

def track_data():
    """Track data files with DVC"""
    logger = setup_logging()
    
    try:
        # Add raw data to DVC
        if os.path.exists('data/raw/customer_transactions.csv'):
            run_command('dvc add data/raw/customer_transactions.csv')
            logger.info("Raw data tracked with DVC")
        
        # Add processed data to DVC
        if os.path.exists('data/processed/processed_transactions.csv'):
            run_command('dvc add data/processed/processed_transactions.csv')
            logger.info("Processed data tracked with DVC")
        
        # Commit changes to Git
        run_command('git add .gitignore data/.gitignore data/raw/.gitignore data/processed/.gitignore *.dvc')
        run_command('git commit -m "Update data tracking"')
        
        logger.info("Data tracking completed successfully")
        
    except Exception as e:
        logger.error(f"Error tracking data: {str(e)}")
        raise

def push_data():
    """Push data to remote storage"""
    logger = setup_logging()
    try:
        run_command('dvc push')
        logger.info("Data pushed to remote storage")
    except Exception as e:
        logger.error(f"Error pushing data: {str(e)}")
        raise

def pull_data():
    """Pull data from remote storage"""
    logger = setup_logging()
    try:
        run_command('dvc pull')
        logger.info("Data pulled from remote storage")
    except Exception as e:
        logger.error(f"Error pulling data: {str(e)}")
        raise

if __name__ == "__main__":
    # Test DVC operations
    track_data()
    push_data() 