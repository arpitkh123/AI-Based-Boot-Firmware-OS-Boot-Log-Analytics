import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from src.parsers.uart_parser import UARTParser
from src.parsers.kernel_parser import KernelParser
from src.feature_engineering.template_extraction import (
    TemplateExtractor
)


def get_first_log_file():

    dataset_path = Path(
        "src/dataset/normal_boot_logs"
    )

    log_files = list(
        dataset_path.glob("*")
    )

    if not log_files:

        raise FileNotFoundError(
            f"No log files found in "
            f"{dataset_path}"
        )

    return log_files[0]


def main():

    try:

        log_file = get_first_log_file()

        print(
            f"\nTesting File: "
            f"{log_file.name}"
        )

        uart_parser = UARTParser()

        parsed_logs = (
            uart_parser.parse_file(
                log_file
            )
        )

        kernel_parser = KernelParser()

        classified_logs = (
            kernel_parser.classify_logs(
                parsed_logs
            )
        )

        extractor = (
            TemplateExtractor()
        )

        templates = (
            extractor.extract_templates(
                classified_logs
            )
        )

        stats = (
            extractor.get_template_statistics(
                templates
            )
        )

        print("\n" + "=" * 70)
        print("TEMPLATE EXTRACTION TEST")
        print("=" * 70)

        print(
            f"\nTotal Templates : "
            f"{stats['total_templates']}"
        )

        print(
            f"Total Occurrences : "
            f"{stats['total_occurrences']}"
        )

        print(
            "\nTop Templates:\n"
        )

        templates = sorted(
            templates,
            key=lambda x: x["count"],
            reverse=True
        )

        for template in templates[:20]:

            print(
                f"\nCluster ID : "
                f"{template['cluster_id']}"
            )

            print(
                f"Count      : "
                f"{template['count']}"
            )

            print(
                f"Template   : "
                f"{template['template']}"
            )

            print("-" * 70)

        print(
            "\nTemplate Extraction "
            "Test Completed Successfully"
        )

    except Exception as error:

        print(
            "\nTest Failed"
        )

        print(
            f"Error: {error}"
        )


if __name__ == "__main__":
    main()