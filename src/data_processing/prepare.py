import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
import matplotlib.pyplot as plt

def prepare_data():
    # Read raw data
    df = pd.read_csv('data/raw/sample_data.csv')
    
    # Basic preprocessing
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Feature selection
    X = df.drop(['target', 'timestamp', 'version'], axis=1)
    y = df['target']
    
    # Select top 10 features
    selector = SelectKBest(score_func=f_classif, k=10)
    X_selected = selector.fit_transform(X, y)
    
    # Get selected feature names
    selected_features = X.columns[selector.get_support()].tolist()
    
    # Create processed dataset
    processed_df = pd.DataFrame(X_selected, columns=selected_features)
    processed_df['target'] = y
    processed_df['timestamp'] = df['timestamp']
    
    # Save processed data
    processed_df.to_csv('data/processed/processed_data.csv', index=False)
    
    # Create feature importance plot
    feature_scores = pd.DataFrame({
        'Feature': X.columns,
        'Score': selector.scores_
    })
    feature_scores = feature_scores.sort_values('Score', ascending=False)
    
    plt.figure(figsize=(10, 6))
    plt.bar(feature_scores['Feature'][:10], feature_scores['Score'][:10])
    plt.xticks(rotation=45)
    plt.title('Top 10 Feature Importance Scores')
    plt.tight_layout()
    plt.savefig('data/processed/feature_importance.png')
    
    print("Data preparation completed:")
    print(f"- Original features: {len(X.columns)}")
    print(f"- Selected features: {len(selected_features)}")
    print(f"- Processed data saved to: data/processed/processed_data.csv")
    print(f"- Feature importance plot saved to: data/processed/feature_importance.png")

if __name__ == "__main__":
    prepare_data() 