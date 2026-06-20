# tests/test_kernel_parser.py

import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from src.parsers.uart_parser import UARTParser
from src.parsers.kernel_parser import KernelParser


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

        print(f"\nTesting File: {log_file.name}")

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

        print("\n" + "=" * 60)
        print("KERNEL PARSER TEST")
        print("=" * 60)

        print(
            f"\nTotal Classified Logs : "
            f"{len(classified_logs)}"
        )

        print("\nFirst 10 Classified Logs:\n")

        for log in classified_logs[:10]:

            print(
                f"[{log['severity']}] "
                f"[{log['subsystem']}] "
                f"{log['message']}"
            )

        severity_counts = {}

        subsystem_counts = {}

        for log in classified_logs:

            severity = log["severity"]
            subsystem = log["subsystem"]

            severity_counts[severity] = (
                severity_counts.get(
                    severity,
                    0
                ) + 1
            )

            subsystem_counts[subsystem] = (
                subsystem_counts.get(
                    subsystem,
                    0
                ) + 1
            )

        print("\nSeverity Summary:\n")

        for severity, count in sorted(
            severity_counts.items()
        ):
            print(
                f"{severity:<10} : {count}"
            )

        print("\nSubsystem Summary:\n")

        for subsystem, count in sorted(
            subsystem_counts.items()
        ):
            print(
                f"{subsystem:<12} : {count}"
            )

        print(
            "\nKernel Parser Test "
            "Completed Successfully"
        )

    except Exception as error:

        print("\nTest Failed")
        print(f"Error: {error}")


if __name__ == "__main__":
    main()