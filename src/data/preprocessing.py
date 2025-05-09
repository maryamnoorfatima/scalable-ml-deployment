import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
import logging
import os
from datetime import datetime

def setup_logging():
    """Configure logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def load_data(file_path):
    """Load data from raw source"""
    logger = setup_logging()
    logger.info(f"Loading data from {file_path}")
    
    # Read CSV file
    df = pd.read_csv(file_path)
    
    # Convert transaction_date to datetime
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    
    return df

def handle_missing_values(df):
    """Handle missing values in the dataset"""
    logger = setup_logging()
    logger.info("Handling missing values")
    
    # Create imputer for numeric columns
    numeric_imputer = SimpleImputer(strategy='mean')
    
    # Columns to impute
    numeric_columns = ['income', 'credit_score']
    
    # Impute missing values
    df[numeric_columns] = numeric_imputer.fit_transform(df[numeric_columns])
    
    return df

def create_features(df):
    """Create new features from existing data"""
    logger = setup_logging()
    logger.info("Creating new features")
    
    # Transaction time features
    df['transaction_hour'] = df['transaction_date'].dt.hour
    df['transaction_day'] = df['transaction_date'].dt.day
    df['transaction_month'] = df['transaction_date'].dt.month
    df['is_weekend'] = df['transaction_date'].dt.dayofweek.isin([5, 6]).astype(int)
    
    # Amount-based features
    df['amount_per_previous_transaction'] = df['transaction_amount'] / (df['num_previous_transactions'] + 1)
    
    # Risk score based on multiple factors
    df['risk_score'] = (
        (df['transaction_amount'] > df['transaction_amount'].mean()).astype(int) * 0.3 +
        (df['credit_score'] < df['credit_score'].mean()).astype(int) * 0.3 +
        (df['account_age_years'] < 1).astype(int) * 0.4
    )
    
    return df

def scale_features(df):
    """Scale numeric features"""
    logger = setup_logging()
    logger.info("Scaling features")
    
    # Columns to scale
    columns_to_scale = [
        'transaction_amount', 'age', 'income', 'credit_score',
        'num_previous_transactions', 'account_age_years',
        'amount_per_previous_transaction', 'risk_score'
    ]
    
    # Initialize scaler
    scaler = StandardScaler()
    
    # Scale features
    df[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])
    
    return df

def encode_categorical(df):
    """Encode categorical variables"""
    logger = setup_logging()
    logger.info("Encoding categorical variables")
    
    # Encode binary variables
    binary_columns = ['is_premium_customer', 'is_weekend']
    df[binary_columns] = df[binary_columns].astype(int)
    
    # Encode customer_id if needed
    le = LabelEncoder()
    df['customer_id_encoded'] = le.fit_transform(df['customer_id'])
    
    return df

def select_features(df):
    """Select features for model training"""
    logger = setup_logging()
    logger.info("Selecting features")
    
    features_to_drop = ['transaction_date', 'customer_id']
    df = df.drop(columns=features_to_drop)
    
    return df

def preprocess_data(input_path, output_path):
    """Main preprocessing function"""
    logger = setup_logging()
    logger.info("Starting preprocessing pipeline")
    
    try:
        # Load data
        df = load_data(input_path)
        
        # Handle missing values
        df = handle_missing_values(df)
        
        # Create new features
        df = create_features(df)
        
        # Scale features
        df = scale_features(df)
        
        # Encode categorical variables
        df = encode_categorical(df)
        
        # Select final features
        df = select_features(df)
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save processed data
        df.to_csv(output_path, index=False)
        logger.info(f"Preprocessed data saved to {output_path}")
        
        # Log preprocessing summary
        logger.info(f"Final dataset shape: {df.shape}")
        logger.info(f"Features: {', '.join(df.columns)}")
        
        return df
        
    except Exception as e:
        logger.error(f"Error in preprocessing pipeline: {str(e)}")
        raise

if __name__ == "__main__":
    # Test preprocessing pipeline
    input_path = "data/raw/customer_transactions.csv"
    output_path = "data/processed/processed_transactions.csv"
    
    df = preprocess_data(input_path, output_path) 