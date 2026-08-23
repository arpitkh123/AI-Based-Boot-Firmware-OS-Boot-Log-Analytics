from pathlib import Path

from typing import Dict

import logging

import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    precision_recall_curve,
    auc,
    confusion_matrix
)


logger = logging.getLogger(__name__)


class ModelEvaluator:

    """
    Evaluate Isolation Forest
    predictions and generate
    statistics and reports.
    """

    def __init__(self):

        logger.info(

            "ModelEvaluator initialized."
        )


    def dataset_summary(
        self,
        dataframe: pd.DataFrame
    ) -> Dict:

        summary = {

            "total_samples":
                len(dataframe),

            "total_features":
                dataframe.shape[1],

            "normal_samples":
                len(
                    dataframe[
                        dataframe["label"] == "normal"
                    ]
                ),

            "error_samples":
                len(
                    dataframe[
                        dataframe["label"] == "error"
                    ]
                ),

            "missing_values":
                int(
                    dataframe
                    .isnull()
                    .sum()
                    .sum()
                ),

            "duplicate_rows":
                int(
                    dataframe
                    .duplicated()
                    .sum()
                )
        }

        return summary        




    def prediction_summary(
        self,
        dataframe: pd.DataFrame
    ) -> Dict:

        summary = {

            "predicted_anomalies":
                int(
                    (
                        dataframe[
                            "anomaly_prediction"
                        ] == -1
                    ).sum()
                ),

            "predicted_inliers":
                int(
                    (
                        dataframe[
                            "anomaly_prediction"
                        ] == 1
                    ).sum()
                ),

            "average_anomaly_score":
                round(

                    dataframe[
                        "anomaly_score"
                    ].mean(),

                    4
                ),

            "highest_anomaly_strength":
                round(

                    dataframe[
                        "anomaly_strength"
                    ].max(),

                    4
                )
        }

        return summary



    def evaluate_with_labels(
        self,
        dataframe: pd.DataFrame
    ) -> Dict:
        """
        Evaluate predictions using ground truth labels.
        Assumes 'label' column exists with 'error' or 'normal',
        and 'anomaly_prediction' column exists (-1 for anomaly, 1 for normal).
        """
        if "label" not in dataframe.columns or "anomaly_prediction" not in dataframe.columns:
            logger.warning("Missing 'label' or 'anomaly_prediction' column for supervised evaluation.")
            return {}

        # Map labels: error/anomaly = 1, normal/inlier = 0
        y_true = (dataframe["label"] == "error").astype(int)
        y_pred = (dataframe["anomaly_prediction"] == -1).astype(int)

        precision = precision_score(y_true, y_pred, zero_division=0)
        recall = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)

        # PR-AUC needs higher score = more anomalous. We use anomaly_strength if available.
        if "anomaly_strength" in dataframe.columns:
            y_scores = dataframe["anomaly_strength"]
            precision_curve, recall_curve, _ = precision_recall_curve(y_true, y_scores)
            pr_auc = auc(recall_curve, precision_curve)
        else:
            pr_auc = None

        cm = confusion_matrix(y_true, y_pred)
        # cm format: [[TN, FP], [FN, TP]]
        tn, fp, fn, tp = cm.ravel() if len(cm.ravel()) == 4 else (0, 0, 0, 0)

        return {
            "precision": round(float(precision), 4),
            "recall": round(float(recall), 4),
            "f1_score": round(float(f1), 4),
            "pr_auc": round(float(pr_auc), 4) if pr_auc is not None else None,
            "confusion_matrix": {
                "true_negative": int(tn),
                "false_positive": int(fp),
                "false_negative": int(fn),
                "true_positive": int(tp)
            }
        }



    def anomaly_statistics(
        self,
        dataframe: pd.DataFrame
    ) -> Dict:

        scores = dataframe[
            "anomaly_score"
        ]

        return {

            "minimum":
                round(
                    scores.min(),
                    4
                ),

            "maximum":
                round(
                    scores.max(),
                    4
                ),

            "mean":
                round(
                    scores.mean(),
                    4
                ),

            "median":
                round(
                    scores.median(),
                    4
                ),

            "std":
                round(
                    scores.std(),
                    4
                )
        }
    

    def top_anomalies(
        self,
        dataframe: pd.DataFrame,
        top_n: int = 5
    ) -> pd.DataFrame:

        return (

            dataframe

            .sort_values(

                by="anomaly_score",

                ascending=True

            )

            .head(top_n)[

                [

                    "file_name",

                    "label",

                    "anomaly_prediction",

                    "anomaly_score",

                    "anomaly_strength"

                ]

            ]

        )
    

    def top_normal_samples(
        self,
        dataframe: pd.DataFrame,
        top_n: int = 5
    ) -> pd.DataFrame:

        return (

            dataframe

            .sort_values(

                by="anomaly_score",

                ascending=False

            )

            .head(top_n)[

                [

                    "file_name",

                    "label",

                    "anomaly_prediction",

                    "anomaly_score",

                    "anomaly_strength"

                ]

            ]

        )



    def save_dataframe(
        self,
        dataframe: pd.DataFrame,
        output_path: Path
    ):

        output_path.parent.mkdir(

            parents=True,

            exist_ok=True

        )

        dataframe.to_csv(

            output_path,

            index=False

        )

        logger.info(

            f"Saved: {output_path}"

        )


    def feature_statistics(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:

        numeric_dataframe = dataframe.select_dtypes(

            include=["number"]

        )

        return numeric_dataframe.describe().T  




    def label_distribution(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:

        return (

            dataframe["label"]

            .value_counts()

            .rename_axis(

                "label"

            )

            .reset_index(

                name="count"

            )

        ) 
    


    def prediction_distribution(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:

        return (

            dataframe["anomaly_prediction"]

            .value_counts()

            .rename_axis(

                "prediction"

            )

            .reset_index(

                name="count"

            )

        )
    



    

    def save_report(
        self,
        report: Dict,
        output_path: Path
    ):

        output_path.parent.mkdir(

            parents=True,

            exist_ok=True
        )

        report_dataframe = pd.DataFrame(

            report.items(),

            columns=[
                "Metric",
                "Value"
            ]
        )

        report_dataframe.to_csv(

            output_path,

            index=False
        )

        logger.info(

            f"Evaluation report saved to "

            f"{output_path}"
        )