from pathlib import Path
import pandas as pd
import sys

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from src.evaluation.model_evaluator import (
    ModelEvaluator
)

from src.models.iforest import (
    IsolationForestModel
)


from sklearn.metrics import (

    confusion_matrix,

    classification_report,

    accuracy_score,

    precision_score,

    recall_score,

    f1_score

)



def main():

    detector = IsolationForestModel()

    evaluator = ModelEvaluator()


    latest_dataset = detector.get_latest_dataset(

        Path(
            "data/processed"
        )

    )

    print(

        f"\nEvaluating Dataset : "

        f"{latest_dataset.name}"

    )

    dataframe = detector.load_dataset(
        latest_dataset
    )


    X = detector.prepare_features(
        dataframe
    )

    detector.train(
        X
    )


    predictions, scores = detector.predict(
        dataframe
    )

    dataframe[
        "anomaly_prediction"
    ] = predictions




    # ------------------------------------
    # Convert predictions to labels
    # ------------------------------------

    dataframe["predicted_label"] = (

        dataframe["anomaly_prediction"]

        .map(

            {

                -1: "error",

                1: "normal"

            }

        )

    )





    dataframe[
        "anomaly_score"
    ] = scores

    dataframe[
        "anomaly_strength"
    ] = (

        dataframe[
            "anomaly_score"
        ]

        .abs()

        * 100

    ).round(2)



    dataset_summary = (

        evaluator.dataset_summary(
            dataframe
        )

    )

    print("\nDataset Summary")
    print("-" * 60)

    for key, value in dataset_summary.items():

        print(

            f"{key:<25}: {value}"

        )



    prediction_summary = (

        evaluator.prediction_summary(
            dataframe
        )

    )

    print("\nPrediction Summary")
    print("-" * 60)

    for key, value in prediction_summary.items():

        print(

            f"{key:<25}: {value}"

        )




    statistics = (

        evaluator.anomaly_statistics(
            dataframe
        )

    )

    print("\nAnomaly Statistics")
    print("-" * 60)

    for key, value in statistics.items():

        print(

            f"{key:<25}: {value}"

        )

    

    print("\nTop Anomalies")
    print("-" * 60)

    top_anomalies = (

        evaluator.top_anomalies(
            dataframe
        )

    )

    print(
        top_anomalies
    )




    print("\nTop Normal Samples")
    print("-" * 60)

    top_normal = (

        evaluator.top_normal_samples(
            dataframe
        )

    )

    print(
        top_normal
    )

    print("\nFeature Statistics")
    print("-" * 60)

    feature_statistics = (

        evaluator.feature_statistics(
            dataframe
        )

    )

    print(

        feature_statistics.head()

    )

    print("\nLabel Distribution")
    print("-" * 60)

    label_distribution = (

        evaluator.label_distribution(
            dataframe
        )

    )

    print(
        label_distribution
    )

    print("\nPrediction Distribution")
    print("-" * 60)

    prediction_distribution = (

        evaluator.prediction_distribution(
            dataframe
        )

    )

    print(
        prediction_distribution
    )





    print("\nConfusion Matrix")
    print("-" * 60)

    actual = dataframe["label"]

    predicted = dataframe["predicted_label"]

    cm = confusion_matrix(

        actual,

        predicted,

        labels=[

            "normal",

            "error"

        ]

    )

    cm_df = pd.DataFrame(

        cm,

        index=[

            "Actual Normal",

            "Actual Error"

        ],

        columns=[

            "Predicted Normal",

            "Predicted Error"

        ]

    )

    print(cm_df)




    print("\nClassification Metrics")
    print("-" * 60)

    print(

        f"Accuracy  : "

        f"{accuracy_score(actual, predicted):.3f}"

    )

    print(

        f"Precision : "

        f"{precision_score(actual, predicted, pos_label='error'):.3f}"

    )

    print(

        f"Recall    : "

        f"{recall_score(actual, predicted, pos_label='error'):.3f}"

    )

    print(

        f"F1 Score  : "

        f"{f1_score(actual, predicted, pos_label='error'):.3f}"

    )    



    print("\nDetailed Classification Report")
    print("-" * 60)

    print(

        classification_report(

            actual,

            predicted,

            digits=3

        )

    )




    print("\nFalse Positives")
    print("-" * 60)

    false_positives = dataframe[

        (dataframe["label"] == "normal")

        &

        (dataframe["predicted_label"] == "error")

    ]

    print(

        false_positives[

            [

                "file_name",

                "anomaly_score"

            ]

        ]

    )


    print("\nFalse Negatives")
    print("-" * 60)

    false_negatives = dataframe[

        (dataframe["label"] == "error")

        &

        (dataframe["predicted_label"] == "normal")

    ]

    print(

        false_negatives[

            [

                "file_name",

                "anomaly_score"

            ]

        ]

    )





    output_directory = Path(
        # "evaluation"
        "data/reports"
    )


    evaluator.save_dataframe(

        cm_df,

        output_directory /

        "confusion_matrix.csv"

    )




    evaluator.save_report(

        dataset_summary,

        output_directory /

        "dataset_summary.csv"

    )

    evaluator.save_report(

        prediction_summary,

        output_directory /

        "prediction_summary.csv"

    )

    evaluator.save_report(

        statistics,

        output_directory /

        "anomaly_statistics.csv"

    )

    evaluator.save_dataframe(

        top_anomalies,

        output_directory /

        "top_anomalies.csv"

    )

    evaluator.save_dataframe(

        top_normal,

        output_directory /

        "top_normal.csv"

    )

    evaluator.save_dataframe(

        # evaluator.feature_statistics(
        #     dataframe
        # ),

        feature_statistics,

        output_directory /

        "feature_statistics.csv"

    )

    evaluator.save_dataframe(

        # evaluator.label_distribution(
        #     dataframe
        # ),

        label_distribution,

        output_directory /

        "label_distribution.csv"

    )

    evaluator.save_dataframe(

        # evaluator.prediction_distribution(
        #     dataframe
        # ),

        prediction_distribution,

        output_directory /

        "prediction_distribution.csv"

    )


    print(

        "\nEvaluation Completed Successfully."

    )


if __name__ == "__main__":

    main()    