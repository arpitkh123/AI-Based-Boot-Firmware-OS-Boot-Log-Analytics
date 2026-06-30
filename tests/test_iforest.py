from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models.iforest import IsolationForestModel


def main():

    detector = IsolationForestModel()

    # dataset_path = Path(
    #     "data/processed/feature_dataset.csv"
    # )

    # dataframe = detector.load_dataset(
    #     dataset_path
    # )


    latest_dataset = detector.get_latest_dataset(

        Path(
            "data/processed"
        )
    )

    print(

        f"\nTraining Dataset : "

        f"{latest_dataset.name}"

    )

    dataframe = detector.load_dataset(
        latest_dataset
    )

    print("\nDataset Loaded")
    print("-" * 60)
    print(dataframe.head())

    X = detector.prepare_features(
        dataframe
    )

    print("\nFeature Matrix Shape")
    print("-" * 60)
    print(X.shape)

    print("\nMissing Values")
    print("-" * 60)

    missing = X.isnull().sum()

    missing = missing[
        missing > 0
    ]

    if missing.empty:

        print("No missing values found.")

    else:

        print(missing)

    if not missing.empty:

        print("\nRows containing missing values")
        print("-" * 60)

        print(

            dataframe[
                X.isnull().any(axis=1)
            ]

        )

    detector.train(X)

    # detector.save_model(
    #     Path(
    #         "models/trained/iforest.pkl"
    #     )
    # )

    detector.save_model(

        Path(
            "models/trained/iforest.pkl"
        ),

        X
    )

    # predictions = detector.predict(
    #     dataframe
    # )

    # dataframe["prediction"] = predictions


    predictions, scores = detector.predict(
        dataframe
    )

    dataframe["prediction"] = predictions

    dataframe["prediction_label"] = (

        dataframe["prediction"]

        .map({

            1: "NORMAL_PATTERN",

            -1: "ANOMALOUS_PATTERN"

        })

    )

    dataframe["anomaly_score"] = scores

    # dataframe["confidence"] = (
    dataframe["anomaly_strength"] = (

        dataframe["anomaly_score"]

        .abs()

        * 100

    ).round(2)

    output_path = Path(
        "data/predictions"
    )

    output_path.mkdir(

        parents=True,

        exist_ok=True
    )

    prediction_file = (

        output_path /

        "prediction_results.csv"

    )

    dataframe.to_csv(

        prediction_file,

        index=False
    )

    print(

        f"\nPrediction results saved to: "

        f"{prediction_file}"

    )

    print("\nPrediction Results")
    print("-" * 60)

    # print(
    #     dataframe[
    #         [
    #             "file_name",
    #             "label",
    #             "prediction"
    #         ]
    #     ]
    # )


    print(

        dataframe[
            [
                "file_name",
                "label",
                "prediction",
                "anomaly_score",
                "anomaly_strength"
                # "confidence"
                
            ]
        ]
    )


if __name__ == "__main__":
    main()