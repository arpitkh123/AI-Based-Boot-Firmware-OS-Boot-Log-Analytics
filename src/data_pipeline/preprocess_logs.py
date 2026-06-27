import logging
from datetime import datetime

from pathlib import Path

import pandas as pd

from src.parsers.uart_parser import UARTParser
from src.parsers.kernel_parser import KernelParser
from src.parsers.boot_parser import BootParser

from src.feature_engineering.template_extraction import (
    TemplateExtractor
)

from src.feature_engineering.feature_builder import (
    FeatureBuilder
)


logger = logging.getLogger(__name__)


class DatasetPreprocessor:

    """
    Generates feature dataset from
    Raspberry Pi boot logs.
    """

    def __init__(self):

        self.uart_parser = UARTParser()

        self.kernel_parser = KernelParser()

        self.boot_parser = BootParser()

        self.template_extractor = (
            TemplateExtractor()
        )

        self.feature_builder = (
            FeatureBuilder()
        )

    def process_log(
        self,
        file_path: Path,
        label: str
    ):
        parsed_logs = (
            self.uart_parser.parse_file(
                file_path
            )
        )

        classified_logs = (
            self.kernel_parser.classify_logs(
                parsed_logs
            )
        )

        boot_analysis = (
            self.boot_parser.analyze_boot(
                classified_logs
            )
        )

        templates = (
            self.template_extractor.extract_templates(
                classified_logs
            )
        )

        feature_vector = (
            self.feature_builder.build_features(
                classified_logs,
                boot_analysis,
                templates,
                label
            )
        )

        return feature_vector
    




    def generate_dataset(
        self,
        normal_logs_path: Path,
        error_logs_path: Path
    ):

        dataset = []

        # -------------------------------
        # Process Normal Boot Logs
        # -------------------------------

        for file in sorted(
            normal_logs_path.glob("*.txt")
        ):

            logger.info(
                f"Processing {file.name}"
            )

            feature_vector = self.process_log(
                file,
                "normal"
            )

            feature_vector["file_name"] = file.name

            dataset.append(
                feature_vector
            )

        # -------------------------------
        # Process Error Boot Logs
        # -------------------------------

        for file in sorted(
            error_logs_path.glob("*.txt")
        ):

            logger.info(
                f"Processing {file.name}"
            )

            feature_vector = self.process_log(
                file,
                "error"
            )

            feature_vector["file_name"] = file.name

            dataset.append(
                feature_vector
            )

        # -------------------------------
        # Create DataFrame
        # -------------------------------

        dataframe = pd.DataFrame(
            dataset
        )

        logger.info(
            f"Dataset created with "
            f"{len(dataframe)} samples."
        )

        return dataframe
    


    # def generate_dataset(
    #     self,
    #     normal_logs_path: Path,
    #     error_logs_path: Path
    # ):
    #     dataset = []

    #     for file in sorted(
    #         normal_logs_path.glob("*.txt")
    #     ):

    #         logger.info(
    #             f"Processing {file.name}"
    #         )

    #         dataset.append(

    #             self.process_log(

    #                 file,

    #                 "normal"
    #             )
    #         )

    #     for file in sorted(
    #         error_logs_path.glob("*.txt")
    #     ):

    #         logger.info(
    #             f"Processing {file.name}"
    #         )

    #         dataset.append(

    #             self.process_log(

    #                 file,

    #                 "error"
    #             )
    #         )


    #         return pd.DataFrame(
    #             dataset
    #         )
        


    def save_dataset(
        self,
        dataframe,
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

            f"Dataset saved at "

            f"{output_path}"
        )


def main():

    processor = DatasetPreprocessor()

    dataframe = (

        processor.generate_dataset(

            Path(
                "src/dataset/normal_boot_logs"
            ),

            Path(
                "src/dataset/error_boot_logs"
            )
        )
    )


    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    output_path = Path(

        "data/processed"

    ) / (

        f"feature_dataset_{timestamp}.csv"
    )

    processor.save_dataset(

        dataframe,

        output_path
    )

    # processor.save_dataset(

    #     dataframe,

    #     Path(
    #         "data/processed/feature_dataset.csv"
    #     )
    # )

    # print()

    # print(dataframe.head())

    # print()

    # print(dataframe.shape)

    print()

    print(
        f"Dataset Shape : "
        f"{dataframe.shape}"
    )

    print()

    print(
        f"Dataset Saved : "
        f"{output_path}"
    )


if __name__ == "__main__":

    main()