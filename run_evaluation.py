import sys
from pathlib import Path
import pandas as pd
import json

from src.models.iforest import IsolationForestModel
from src.evaluation.model_evaluator import ModelEvaluator
from src.evaluation.visualize import Visualizer

def main():
    print("Initializing Isolation Forest Model...")
    detector = IsolationForestModel()
    
    # Try to load latest dataset
    try:
        dataset_path = Path("data/processed")
        latest_dataset = detector.get_latest_dataset(dataset_path)
        print(f"Loading dataset: {latest_dataset}")
        df = detector.load_dataset(latest_dataset)
    except FileNotFoundError:
        print("No dataset found in data/processed/. Please ensure the data pipeline has been run.")
        sys.exit(1)
        
    # Attempt to load model
    try:
        detector.load_model()
        print("Successfully loaded trained model.")
    except Exception:
        print("No trained model found. Training a new model on the loaded dataset...")
        X = detector.prepare_features(df)
        detector.train(X)
        detector.save_model(Path("models/trained/iforest.pkl"), X)

    # Generate predictions
    print("Generating predictions on the dataset...")
    try:
        # predict() returns (predictions, scores)
        predictions, scores = detector.predict(df)
        df["anomaly_prediction"] = predictions
        df["anomaly_score"] = scores
        df["anomaly_strength"] = abs(scores) * 100
    except Exception as e:
        print(f"Error making predictions: {e}")
        sys.exit(1)

    evaluator = ModelEvaluator()
    
    if "label" not in df.columns:
        print("\nNotice: The dataset does not contain a 'label' column.")
        print("Supervised evaluation metrics (Precision, Recall) cannot be computed.")
        print("\n--- Prediction Summary ---")
        summary = evaluator.prediction_summary(df)
        print(json.dumps(summary, indent=4))
        sys.exit(0)
        
    print("\n--- Model Evaluation Metrics (Labeled Data) ---")
    results = evaluator.evaluate_with_labels(df)
    
    if results:
        print(json.dumps(results, indent=4))
        
        # Save results to visualization folder
        vis = Visualizer()
        output_json = vis.output_dir / "evaluation_metrics.json"
        with open(output_json, "w") as f:
            json.dump(results, f, indent=4)
        print(f"\nSaved numerical metrics to {output_json}")
        
        # Plot confusion matrix
        vis.plot_confusion_matrix(results)
    else:
        print("Evaluation failed. Please check the dataset columns.")

if __name__ == "__main__":
    main()
