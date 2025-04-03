import pandas as pd
import numpy as np
from sklearn.datasets import make_classification

def generate_sample_data():
    # Generate synthetic data
    X, y = make_classification(
        n_samples=1000,
        n_features=20,
        n_informative=15,
        n_redundant=5,
        random_state=42
    )
    
    # Create feature names
    feature_names = [f'feature_{i}' for i in range(X.shape[1])]
    
    # Create DataFrame
    df = pd.DataFrame(X, columns=feature_names)
    df['target'] = y
    
    # Add some metadata
    df['timestamp'] = pd.date_range(start='2023-01-01', periods=len(df), freq='H')
    df['version'] = '1.0'
    
    # Save to CSV
    df.to_csv('data/raw/sample_data.csv', index=False)
    print(f"Generated sample data with {len(df)} rows and {len(df.columns)} columns")

if __name__ == "__main__":
    generate_sample_data() 