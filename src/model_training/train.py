import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import mlflow
import mlflow.sklearn
from datetime import datetime

def train_model():
    # Set MLflow tracking URI
    mlflow.set_tracking_uri("http://localhost:5000")
    
    # Read processed data
    df = pd.read_csv('data/processed/processed_data.csv')
    
    # Prepare features and target
    X = df.drop(['target', 'timestamp'], axis=1)
    y = df['target']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Start MLflow run
    with mlflow.start_run(run_name=f"model_training_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
        # Log parameters
        params = {
            'n_estimators': 100,
            'max_depth': 10,
            'random_state': 42
        }
        mlflow.log_params(params)
        
        # Train model
        model = RandomForestClassifier(**params)
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1': f1_score(y_test, y_pred)
        }
        
        # Log metrics
        mlflow.log_metrics(metrics)
        
        # Log feature importance plot
        feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        feature_importance.to_csv('models/feature_importance.csv', index=False)
        mlflow.log_artifact('models/feature_importance.csv')
        
        # Log model
        mlflow.sklearn.log_model(model, "model")
        
        print("Model training completed:")
        print("Metrics:")
        for metric, value in metrics.items():
            print(f"- {metric}: {value:.4f}")
        print(f"Model and artifacts logged to MLflow run: {mlflow.active_run().info.run_id}")

if __name__ == "__main__":
    train_model() 