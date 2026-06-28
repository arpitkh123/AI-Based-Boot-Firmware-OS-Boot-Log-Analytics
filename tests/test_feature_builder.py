import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from src.parsers.uart_parser import UARTParser
from src.parsers.kernel_parser import KernelParser
from src.parsers.boot_parser import BootParser
from src.feature_engineering.template_extraction import (
    TemplateExtractor
)
from src.feature_engineering.feature_builder import (
    FeatureBuilder
)


def get_first_log_file():

    dataset_path = Path(
        "src/dataset/error_boot_logs"
    )

    log_files = sorted(
        dataset_path.glob("*")
    )

    if not log_files:

        raise FileNotFoundError(
            f"No log files found in {dataset_path}"
        )

    return log_files[0]



def get_all_log_files():

    dataset_root = Path(
        "src/dataset"
    )

    log_files = []

    for folder in sorted(
        dataset_root.iterdir()
    ):

        if folder.is_dir():

            log_files.extend(
                sorted(
                    folder.glob("*")
                )
            )

    if not log_files:

        raise FileNotFoundError(
            "No log files found inside dataset."
        )

    return log_files


def main():

    try:

        print("\n" + "=" * 90)
        print("FEATURE BUILDER TEST")
        print("=" * 90)

        log_files = get_all_log_files()

        for index, log_file in enumerate(
            log_files,
            start=1
        ):
            print(
                f"\n[{index}/{len(log_files)}]"
                # f"\nTesting File : {log_file.name}"
            )

            print(
                f"Testing File : {log_file.name}"
            )

            uart_parser = UARTParser()

            parsed_logs = uart_parser.parse_file(
                log_file
            )

            kernel_parser = KernelParser()

            classified_logs = (
                kernel_parser.classify_logs(
                    parsed_logs
                )
            )

            boot_parser = BootParser()

            boot_analysis = (
                boot_parser.analyze_boot(
                    classified_logs
                )
            )

            template_extractor = (
                TemplateExtractor()
            )

            templates = (
                template_extractor.extract_templates(
                    classified_logs
                )
            )

            feature_builder = (
                FeatureBuilder()
            )

            feature_vector = (
                feature_builder.build_features(
                    classified_logs=classified_logs,
                    boot_analysis=boot_analysis,
                    templates=templates,
                    # label="error"
                    label=log_file.parent.name
                )
            )

            # print("\n" + "=" * 70)
            # print("FEATURE VECTOR")
            # print("=" * 70)

            # for key, value in feature_vector.items():

            #     print(
            #         f"{key:<35}: {value}"
            #     )


            print(
            f"Boot Success : "
            f"{feature_vector['boot_successful']}"
            )

            print(
                f"Errors       : "
                f"{feature_vector['error_count']}"
            )

            print(
                f"Warnings     : "
                f"{feature_vector['warning_count']}"
            )

            print(
                f"Templates    : "
                f"{feature_vector['unique_templates']}"
            )

            print(
                f"Label        : "
                f"{feature_vector['label']}"
            )

            print(
                "\nFeature Builder Test Completed Successfully"
            )

    except Exception as error:

        print("\nTest Failed")

        print(error)


if __name__ == "__main__":
    main()