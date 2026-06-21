# tests/test_boot_parser.py

import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from src.parsers.uart_parser import UARTParser
from src.parsers.kernel_parser import KernelParser
from src.parsers.boot_parser import BootParser


def get_first_log_file():

    dataset_path = Path(
        "src/dataset/normal_boot_logs"
    )

    log_files = list(dataset_path.glob("*"))

    if not log_files:
        raise FileNotFoundError(
            f"No log files found in {dataset_path}"
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

        boot_parser = BootParser()

        boot_analysis = (
            boot_parser.analyze_boot(
                classified_logs
            )
        )

        print("\n" + "=" * 60)
        print("BOOT PARSER TEST")
        print("=" * 60)

        print("\nBoot Analysis Results:\n")

        for key, value in (
            boot_analysis.items()
        ):

            print(
                f"{key:<35} "
                f": {value}"
            )

        print(
            "\nBoot Parser Test "
            "Completed Successfully"
        )

    except Exception as error:

        print("\nTest Failed")
        print(
            f"Error: {error}"
        )


if __name__ == "__main__":
    main()