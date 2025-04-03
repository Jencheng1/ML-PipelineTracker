import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def generate_analysis_report():
    # Read processed data
    df = pd.read_csv('data/processed/processed_data.csv')
    
    # Create HTML report
    html_content = """
    <html>
    <head>
        <title>Data Analysis Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .section { margin: 20px 0; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h1>Data Analysis Report</h1>
        <p>Generated on: {}</p>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # Basic statistics
    html_content += """
        <div class="section">
            <h2>Basic Statistics</h2>
            <table>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
                <tr>
                    <td>Number of samples</td>
                    <td>{}</td>
                </tr>
                <tr>
                    <td>Number of features</td>
                    <td>{}</td>
                </tr>
                <tr>
                    <td>Class distribution</td>
                    <td>{}</td>
                </tr>
            </table>
        </div>
    """.format(
        len(df),
        len(df.columns) - 2,  # Excluding target and timestamp
        df['target'].value_counts().to_dict()
    )
    
    # Feature correlations
    corr_matrix = df.drop(['target', 'timestamp'], axis=1).corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('Feature Correlation Matrix')
    plt.tight_layout()
    plt.savefig('data/processed/correlation_matrix.png')
    
    html_content += """
        <div class="section">
            <h2>Feature Correlations</h2>
            <img src="correlation_matrix.png" alt="Correlation Matrix" style="width: 100%;">
        </div>
    """
    
    # Close HTML
    html_content += """
    </body>
    </html>
    """
    
    # Save report
    with open('data/processed/analysis_report.html', 'w') as f:
        f.write(html_content)
    
    print("Analysis report generated:")
    print("- Basic statistics included")
    print("- Correlation matrix generated")
    print("- Report saved to: data/processed/analysis_report.html")

if __name__ == "__main__":
    generate_analysis_report() 