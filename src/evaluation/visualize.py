import logging
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
import joblib

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Visualizer:
    def __init__(self):
        self.output_dir = Path("visualizations")
        self.output_dir.mkdir(exist_ok=True)

    def load_latest_dataset(self, data_dir: Path) -> pd.DataFrame:
        dataset_files = sorted(data_dir.glob("feature_dataset_*.csv"), key=lambda f: f.stat().st_mtime, reverse=True)
        if not dataset_files:
            raise FileNotFoundError("No dataset found in data/processed/")
        return pd.read_csv(dataset_files[0])
        
    def load_model(self, model_path: Path):
        return joblib.load(model_path)

    def plot_pca_clusters(self, df: pd.DataFrame, model_data: dict):
        logger.info("Generating PCA scatter plot...")
        features = model_data["features"]
        X = df[features].copy()
        
        # Reduce to 2 dimensions
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X)
        
        plt.figure(figsize=(10, 7))
        # Plot Normal
        plt.scatter(X_pca[df['label'] == 'normal', 0], X_pca[df['label'] == 'normal', 1], 
                    color='green', label='Normal Boot', alpha=0.7)
        # Plot Anomaly
        plt.scatter(X_pca[df['label'] == 'anomaly', 0], X_pca[df['label'] == 'anomaly', 1], 
                    color='red', label='Error Boot', alpha=0.7)
                    
        # If your labels are 'error' instead of 'anomaly'
        plt.scatter(X_pca[df['label'] == 'error', 0], X_pca[df['label'] == 'error', 1], 
                    color='red', label='Error Boot', alpha=0.7)

        plt.title("PCA Cluster Visualization of Boot Logs")
        plt.xlabel("Principal Component 1")
        plt.ylabel("Principal Component 2")
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        output_file = self.output_dir / "pca_clusters.png"
        plt.savefig(output_file)
        plt.close()
        logger.info(f"Saved PCA plot to {output_file}")

    def plot_anomaly_distribution(self, df: pd.DataFrame, model_data: dict):
        logger.info("Generating Anomaly Score Distribution Histogram...")
        model = model_data["model"]
        features = model_data["features"]
        X = df[features].copy()
        
        # Calculate scores
        scores = model.decision_function(X)
        df['anomaly_score'] = scores
        
        plt.figure(figsize=(10, 6))
        
        # Support both 'error' and 'anomaly' labels
        normal_scores = df[df['label'] == 'normal']['anomaly_score']
        error_scores = df[df['label'].isin(['error', 'anomaly'])]['anomaly_score']
        
        sns.histplot(normal_scores, color='green', label='Normal Boot', kde=True, bins=20, alpha=0.5)
        sns.histplot(error_scores, color='red', label='Error Boot', kde=True, bins=20, alpha=0.5)
        
        # The isolation forest boundary is usually at score 0
        plt.axvline(x=0, color='black', linestyle='--', label='Decision Boundary')
        
        plt.title("Isolation Forest Decision Score Distribution")
        plt.xlabel("Anomaly Score (Negative = Anomalous)")
        plt.ylabel("Frequency")
        plt.legend()
        
        output_file = self.output_dir / "score_distribution.png"
        plt.savefig(output_file)
        plt.close()
        logger.info(f"Saved distribution plot to {output_file}")

    def plot_confusion_matrix(self, metrics: dict):
        if "confusion_matrix" not in metrics:
            return
        logger.info("Generating Confusion Matrix plot...")
        cm = metrics["confusion_matrix"]
        
        cm_array = [
            [cm["true_negative"], cm["false_positive"]],
            [cm["false_negative"], cm["true_positive"]]
        ]
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm_array, annot=True, fmt='d', cmap='Blues', 
                    xticklabels=['Predicted Normal', 'Predicted Error'],
                    yticklabels=['Actual Normal', 'Actual Error'])
        
        plt.title(f"Confusion Matrix\nPrecision: {metrics.get('precision', 0)} | Recall: {metrics.get('recall', 0)} | F1: {metrics.get('f1_score', 0)}")
        
        output_file = self.output_dir / "confusion_matrix.png"
        plt.savefig(output_file)
        plt.close()
        logger.info(f"Saved Confusion Matrix plot to {output_file}")

def main():
    vis = Visualizer()
    df = vis.load_latest_dataset(Path("data/processed"))
    
    try:
        model_data = vis.load_model(Path("models/trained/iforest.pkl"))
        vis.plot_pca_clusters(df, model_data)
        vis.plot_anomaly_distribution(df, model_data)
        logger.info("All visualizations generated successfully.")
    except Exception as e:
        logger.error(f"Failed to generate visualizations. Ensure tuner.py was run first. Error: {e}")

if __name__ == "__main__":
    main()
