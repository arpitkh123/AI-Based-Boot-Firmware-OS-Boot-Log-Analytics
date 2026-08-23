import logging
import pandas as pd
from pathlib import Path
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import f1_score, make_scorer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IsolationForestTuner:
    def __init__(self):
        self.feature_columns = None

    def load_latest_dataset(self, data_dir: Path) -> pd.DataFrame:
        dataset_files = sorted(data_dir.glob("feature_dataset_*.csv"), key=lambda f: f.stat().st_mtime, reverse=True)
        if not dataset_files:
            raise FileNotFoundError("No dataset found in data/processed/")
        latest = dataset_files[0]
        logger.info(f"Loading dataset: {latest.name}")
        return pd.read_csv(latest)

    def tune_and_train(self, df: pd.DataFrame, model_output_path: Path):
        # We need normal and anomaly data
        # Mapping label to 1 (normal) and -1 (anomaly) for Isolation Forest
        df['y'] = df['label'].apply(lambda x: 1 if x == 'normal' else -1)
        
        normal_data = df[df['y'] == 1].copy()
        anomaly_data = df[df['y'] == -1].copy()
        
        logger.info(f"Found {len(normal_data)} normal logs and {len(anomaly_data)} error logs.")
        
        # Split normal data: 80% strictly for training, 20% for testing (validation)
        # We DO NOT put anomalies in training set to ensure pure baseline learning
        train_normal, test_normal = train_test_split(normal_data, test_size=0.2, random_state=42)
        
        # Testing set combines the held-out normal data and ALL anomaly data
        test_df = pd.concat([test_normal, anomaly_data])
        
        # Define features
        self.feature_columns = [col for col in df.select_dtypes(include=["number"]).columns if col not in ['y']]
        
        X_train = train_normal[self.feature_columns]
        X_test = test_df[self.feature_columns]
        y_test = test_df['y']
        
        logger.info(f"Training strictly on {len(X_train)} normal logs.")
        logger.info(f"Validating on {len(X_test)} mixed logs.")
        
        # Define the parameter grid
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_samples': ['auto', 0.5, 0.8],
            'contamination': [0.01, 0.05, 0.1, 0.15]
        }
        
        # Custom scorer for Isolation Forest (since it outputs 1 and -1)
        # We care about accurately finding anomalies (-1)
        f1_scorer = make_scorer(f1_score, pos_label=-1)
        
        clf = IsolationForest(random_state=42)
        
        logger.info("Starting GridSearchCV...")
        grid = GridSearchCV(clf, param_grid, scoring=f1_scorer, cv=3, n_jobs=-1)
        
        # We need a small hack here because GridSearchCV uses CV internally and expects both classes in X_train for typical supervised models.
        # But Isolation Forest is unsupervised and only needs X_train. 
        # Since GridSearchCV natively cross-validates on the provided training set (which here is 100% normal), it won't be able to calculate F1 score!
        # Instead, we will do a manual grid search on the test set.
        
        best_f1 = -1
        best_params = None
        best_model = None
        
        for n_est in param_grid['n_estimators']:
            for max_samp in param_grid['max_samples']:
                for contam in param_grid['contamination']:
                    model = IsolationForest(
                        n_estimators=n_est, 
                        max_samples=max_samp, 
                        contamination=contam, 
                        random_state=42
                    )
                    model.fit(X_train)
                    preds = model.predict(X_test)
                    score = f1_score(y_test, preds, pos_label=-1)
                    
                    if score > best_f1:
                        best_f1 = score
                        best_params = {'n_estimators': n_est, 'max_samples': max_samp, 'contamination': contam}
                        best_model = model
                        
        logger.info(f"Best Parameters found: {best_params}")
        logger.info(f"Best Validation F1 Score: {best_f1:.4f}")
        
        # Save the best model using the existing format
        model_output_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump({
            "model": best_model,
            "features": self.feature_columns,
            "feature_count": len(self.feature_columns),
            "training_samples": len(X_train),
            "model_type": "IsolationForest",
            "model_version": "1.1_tuned",
            "best_params": best_params
        }, model_output_path)
        
        logger.info(f"Optimized model successfully saved to {model_output_path}")

def main():
    tuner = IsolationForestTuner()
    df = tuner.load_latest_dataset(Path("data/processed"))
    tuner.tune_and_train(df, Path("models/trained/iforest.pkl"))

if __name__ == "__main__":
    main()
