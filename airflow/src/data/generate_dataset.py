import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_customer_data(n_samples=1000):
    """
    Generate a synthetic customer transaction dataset
    """
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Generate customer IDs
    customer_ids = [f'CUST_{i:04d}' for i in range(n_samples)]
    
    # Generate dates
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    dates = [start_date + timedelta(days=x) for x in range(n_samples)]
    np.random.shuffle(dates)
    
    # Generate features
    data = {
        'customer_id': customer_ids,
        'transaction_date': dates,
        'transaction_amount': np.random.normal(500, 200, n_samples),  # Mean $500, SD $200
        'age': np.random.randint(18, 80, n_samples),
        'income': np.random.normal(60000, 20000, n_samples),  # Mean $60k, SD $20k
        'credit_score': np.random.normal(700, 50, n_samples),  # Mean 700, SD 50
        'num_previous_transactions': np.random.poisson(10, n_samples),
        'account_age_years': np.random.uniform(0, 20, n_samples),
        'is_premium_customer': np.random.choice([0, 1], n_samples, p=[0.8, 0.2]),
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Add some derived features
    df['transaction_month'] = df['transaction_date'].dt.month
    df['transaction_day'] = df['transaction_date'].dt.day
    df['transaction_dayofweek'] = df['transaction_date'].dt.dayofweek
    
    # Add some missing values
    for column in ['income', 'credit_score']:
        mask = np.random.random(len(df)) < 0.1
        df.loc[mask, column] = np.nan
    
    # Generate target variable (fraud detection)
    # Higher probability of fraud for:
    # - Large transactions
    # - Low credit scores
    # - New accounts
    fraud_score = (
        (df['transaction_amount'] > 800).astype(int) * 2 +
        (df['credit_score'] < 600).astype(int) * 1.5 +
        (df['account_age_years'] < 1).astype(int) * 1
    )
    fraud_prob = 1 / (1 + np.exp(-fraud_score + 2))
    df['is_fraudulent'] = np.random.binomial(1, fraud_prob)
    
    # Clean up and format
    df['transaction_amount'] = df['transaction_amount'].round(2)
    df['income'] = df['income'].round(2)
    df['credit_score'] = df['credit_score'].round(0)
    df['account_age_years'] = df['account_age_years'].round(1)
    
    # Create directory if it doesn't exist
    os.makedirs('data/raw', exist_ok=True)
    
    # Save dataset
    output_path = 'data/raw/customer_transactions.csv'
    df.to_csv(output_path, index=False)
    
    # Print dataset information
    print(f"\nDataset generated and saved to {output_path}")
    print("\nDataset Information:")
    print(f"Number of samples: {len(df)}")
    print(f"Number of features: {len(df.columns)}")
    print("\nFeatures:")
    print(df.dtypes)
    print("\nMissing values:")
    print(df.isnull().sum())
    print("\nTarget distribution (Fraudulent Transactions):")
    print(df['is_fraudulent'].value_counts(normalize=True))
    print("\nSample of the data:")
    print(df.head())
    
    return df

if __name__ == "__main__":
    df = generate_customer_data() 