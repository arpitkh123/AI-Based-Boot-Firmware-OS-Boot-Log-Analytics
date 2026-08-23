import logging
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
import numpy as np

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LearningCurveVisualizer:
    def __init__(self):
        self.output_dir = Path("visualizations")
        self.output_dir.mkdir(exist_ok=True)

    def load_latest_dataset(self, data_dir: Path) -> pd.DataFrame:
        dataset_files = sorted(data_dir.glob("feature_dataset_*.csv"), key=lambda f: f.stat().st_mtime, reverse=True)
        if not dataset_files:
            raise FileNotFoundError("No dataset found in data/processed/")
        return pd.read_csv(dataset_files[0])

    def plot_estimators_curve(self, df: pd.DataFrame):
        """Plots the F1 validation score as the number of trees (n_estimators) increases."""
        logger.info("Generating learning curve (n_estimators vs F1-score)...")
        
        df['y'] = df['label'].apply(lambda x: 1 if x == 'normal' else -1)
        normal_data = df[df['y'] == 1].copy()
        anomaly_data = df[df['y'] == -1].copy()
        
        train_normal, test_normal = train_test_split(normal_data, test_size=0.2, random_state=42)
        test_df = pd.concat([test_normal, anomaly_data])
        
        feature_columns = [col for col in df.select_dtypes(include=["number"]).columns if col not in ['y']]
        
        X_train = train_normal[feature_columns]
        X_test = test_df[feature_columns]
        y_test = test_df['y']
        
        estimators_range = range(10, 301, 20)
        f1_scores = []
        
        for n_est in estimators_range:
            model = IsolationForest(n_estimators=n_est, contamination=0.05, random_state=42)
            model.fit(X_train)
            preds = model.predict(X_test)
            score = f1_score(y_test, preds, pos_label=-1)
            f1_scores.append(score)
            
        plt.figure(figsize=(10, 6))
        plt.plot(estimators_range, f1_scores, marker='o', linestyle='-', color='b', linewidth=2)
        plt.title("Isolation Forest: Validation F1-Score vs Number of Trees")
        plt.xlabel("Number of Estimators (Trees)")
        plt.ylabel("F1-Score (Anomaly Detection)")
        plt.grid(True, linestyle='--', alpha=0.7)
        
        output_file = self.output_dir / "learning_curve_estimators.png"
        plt.savefig(output_file)
        plt.close()
        logger.info(f"Saved estimators learning curve to {output_file}")
        
    def plot_data_size_curve(self, df: pd.DataFrame):
        """Plots the F1 validation score as the amount of training data increases."""
        logger.info("Generating learning curve (training size vs F1-score)...")
        
        df['y'] = df['label'].apply(lambda x: 1 if x == 'normal' else -1)
        normal_data = df[df['y'] == 1].copy()
        anomaly_data = df[df['y'] == -1].copy()
        
        # We need a fixed test set
        train_normal_full, test_normal = train_test_split(normal_data, test_size=0.2, random_state=42)
        test_df = pd.concat([test_normal, anomaly_data])
        
        feature_columns = [col for col in df.select_dtypes(include=["number"]).columns if col not in ['y']]
        
        X_test = test_df[feature_columns]
        y_test = test_df['y']
        
        # Vary training sizes
        train_sizes = np.linspace(0.2, 1.0, 5)
        f1_scores = []
        
        for size in train_sizes:
            # Subsample the training data
            n_samples = max(int(len(train_normal_full) * size), 2) # At least 2 samples
            X_train = train_normal_full[feature_columns].sample(n=n_samples, random_state=42)
            
            model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
            model.fit(X_train)
            preds = model.predict(X_test)
            score = f1_score(y_test, preds, pos_label=-1)
            f1_scores.append(score)
            
        # Convert proportions back to actual sample counts for the x-axis
        sample_counts = [int(len(train_normal_full) * s) for s in train_sizes]
            
        plt.figure(figsize=(10, 6))
        plt.plot(sample_counts, f1_scores, marker='s', linestyle='-', color='g', linewidth=2)
        plt.title("Isolation Forest: Validation F1-Score vs Training Data Size")
        plt.xlabel("Number of Normal Training Samples")
        plt.ylabel("F1-Score (Anomaly Detection)")
        plt.grid(True, linestyle='--', alpha=0.7)
        
        output_file = self.output_dir / "learning_curve_data_size.png"
        plt.savefig(output_file)
        plt.close()
        logger.info(f"Saved data size learning curve to {output_file}")

def main():
    vis = LearningCurveVisualizer()
    df = vis.load_latest_dataset(Path("data/processed"))
    vis.plot_estimators_curve(df)
    vis.plot_data_size_curve(df)
    logger.info("Learning curves generated successfully.")

if __name__ == "__main__":
    main()
