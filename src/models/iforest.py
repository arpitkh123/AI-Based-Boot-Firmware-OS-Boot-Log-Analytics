import logging
from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import IsolationForest

logger = logging.getLogger(__name__)


class IsolationForestModel:
    """
    Isolation Forest based anomaly detector.
    """

    def __init__(self):

        self.model = None

        self.feature_columns = None

    

    def load_dataset(
        self,
        dataset_path: Path
    ) -> pd.DataFrame:

        dataframe = pd.read_csv(
            dataset_path
        )

        logger.info(

            f"Loaded dataset with "

            f"{len(dataframe)} samples."
        )

        return dataframe
    



    def prepare_features(
        self,
        dataframe: pd.DataFrame
    ):

        X = dataframe.select_dtypes(
            include=["number"]
        ).copy()

        if "label" in X.columns:

            X.drop(
                columns=["label"],
                inplace=True
            )

        self.feature_columns = list(
            X.columns
        )

        logger.info(

            f"Training with "

            f"{len(self.feature_columns)} "

            f"features."

        )

        return X
    



    

    # def prepare_features(
    #     self,
    #     dataframe: pd.DataFrame
    # ):
    #     excluded_columns = [

    #         "label",

    #         "file_name"
    #     ]

    #     feature_columns = [

    #         column

    #         for column in dataframe.columns

    #         if column not in excluded_columns
    #     ]

    #     self.feature_columns = feature_columns

    #     X = dataframe[
    #         feature_columns
    #     ]

    #     return X
    


    # def train(
    #     self,
    #     X
    # ):
    #     self.model = IsolationForest(

    #         n_estimators=100,

    #         contamination="auto",

    #         random_state=42
    #     )

    #     self.model.fit(X)

    #     logger.info(

    #         "Isolation Forest trained successfully."
    #     )



    def train(
        self,
        X
    ):

        if X.isnull().values.any():

            raise ValueError(

                "Dataset contains missing values."

            )

        self.model = IsolationForest(

            n_estimators=100,

            contamination="auto",

            random_state=42
        )

        self.model.fit(
            X
        )

        logger.info(

            "Isolation Forest trained successfully."

        )


    def save_model(
        self,
        model_path: Path,
        X
    ):
        model_path.parent.mkdir(

            parents=True,

            exist_ok=True
        )

        # joblib.dump(

        #     {

        #         "model": self.model,

        #         "features": self.feature_columns,

        #         "feature_count": len(
        #             self.feature_columns
        #         ),

        #         "training_samples": len(
        #             X
        #         )
        #     },


        joblib.dump(

        {

            "model":

                self.model,

            "features":

                self.feature_columns,

            "feature_count":

                len(

                    self.feature_columns

                ),

            "training_samples":

                len(X),

            "model_type":

                "IsolationForest",

            "model_version":

                "1.0"

        },

        model_path

    )

        #     model_path
        # )

        logger.info(

            f"Model saved to "

            f"{model_path}"
        )

    
    def load_model(
        self,
        model_path: Path | None = None
    ):
        
        if model_path is None:

            model_path = self.get_latest_model(

                Path("models/trained")

            )

        saved = joblib.load(
            model_path
        )

        self.model = saved["model"]

        self.feature_columns = saved["features"]

        logger.info(

            "Model loaded successfully."
        )


    # def predict(
    #     self,
    #     dataframe: pd.DataFrame
    # ):
    #     X = dataframe[
    #         self.feature_columns
    #     ]

    #     predictions = self.model.predict(
    #         X
    #     )

    #     return predictions


    def predict(
        self,
        dataframe: pd.DataFrame
    ):

        missing_columns = [

            column

            for column in self.feature_columns

            if column not in dataframe.columns

        ]

        if missing_columns:

            raise ValueError(

                f"Missing feature columns: "

                f"{missing_columns}"

            )

        X = dataframe[
            self.feature_columns
        ]

        predictions = self.model.predict(
            X
        )

        # print(predictions)

        scores = self.model.decision_function(
            X
        )

        # print(scores)

        return predictions, scores


    def predict_feature_vector(
        self,
        feature_vector: dict
    ):
        """
        Predict anomaly for a
        single feature vector.
        """

        if self.model is None:

            raise ValueError(

                "Model has not been loaded."

            )

        missing_columns = [

            column

            for column in self.feature_columns

            if column not in feature_vector

        ]

        if missing_columns:

            raise ValueError(

                f"Missing feature columns: "

                f"{missing_columns}"

            )

        dataframe = pd.DataFrame(

            [

                {

                    column: feature_vector[column]

                    for column in self.feature_columns

                }

            ]

        )

        prediction = self.model.predict(

            dataframe

        )[0]

        anomaly_score = self.model.decision_function(

            dataframe

        )[0]

        anomaly_strength = round(

            abs(

                anomaly_score

            ) * 100,

            2

        )

        return {

            "prediction":

                "ANOMALY"

                if prediction == -1

                else "NORMAL",

            "prediction_code":

                int(

                    prediction

                ),

            "anomaly_score":

                float(

                    anomaly_score

                ),

            "anomaly_strength":

                anomaly_strength

        }


    def get_latest_dataset(
        self,
        processed_dir: Path
    ) -> Path:

        dataset_files = sorted(

            processed_dir.glob(
                "feature_dataset_*.csv"
            ),

            key=lambda file: file.stat().st_mtime,

            reverse=True
        )

        if not dataset_files:

            raise FileNotFoundError(

                "No processed feature dataset found."

            )

        latest_dataset = dataset_files[0]

        logger.info(

            f"Using latest dataset: "

            f"{latest_dataset.name}"

        )

        return latest_dataset




    def get_latest_model(
        self,
        model_dir: Path
    ) -> Path:

        model_files = sorted(

            model_dir.glob(

                "*.pkl"

            ),

            key=lambda file: file.stat().st_mtime,

            reverse=True

        )

        if not model_files:

            raise FileNotFoundError(

                "No trained model found."

            )

        latest_model = model_files[0]

        logger.info(

            f"Using latest model: "

            f"{latest_model.name}"

        )

        return latest_model
    



def main():

    detector = IsolationForestModel()

    # dataframe = detector.load_dataset(

    #     Path(
    #         "data/processed/feature_dataset.csv"
    #     ),
    # )

    latest_dataset = detector.get_latest_dataset(

        Path(
            "data/processed"
        )
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

    detector.save_model(

        Path(
            "models/trained/iforest.pkl"
        ),
        X
    )

    predictions = detector.predict(
        dataframe
    )

    dataframe["prediction"] = predictions

    print()

    print(

        dataframe[

            [

                "file_name",

                "label",

                "prediction"
            ]

        ]
    )


if __name__ == "__main__":

    main()