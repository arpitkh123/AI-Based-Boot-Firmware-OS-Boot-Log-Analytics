# tests/test_kernel_parser.py

import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from src.parsers.uart_parser import UARTParser
from src.parsers.kernel_parser import KernelParser


# def get_first_log_file():

#     dataset_path = Path(
#         "src/dataset/normal_boot_logs"
#     )

#     log_files = list(dataset_path.glob("*"))

#     if not log_files:
#         raise FileNotFoundError(
#             f"No log files found in {dataset_path}"
#         )

#     return log_files[0]


def get_all_log_files():

    dataset_paths = [

        Path(
            "src/dataset/normal_boot_logs"
        ),

        Path(
            "src/dataset/error_boot_logs"
        )
    ]

    log_files = []

    for folder in dataset_paths:

        if folder.exists():

            log_files.extend(

                sorted(
                    folder.glob("*.txt")
                )

            )

    if not log_files:

        raise FileNotFoundError(
            "No log files found."
        )

    return log_files


def main():

    try:

        # log_file = get_first_log_file()

        # print(f"\nTesting File: {log_file.name}")

        log_files = get_all_log_files()

        print(
            f"\nFound {len(log_files)} log files.\n"
        )

        uart_parser = UARTParser()

        # parsed_logs = uart_parser.parse_file(
        #     log_file
        # )

        kernel_parser = KernelParser()

        total_files = 0
        passed_files = 0
        failed_files = 0
        total_classified_logs = 0

        # classified_logs = (
        #     kernel_parser.classify_logs(
        #         parsed_logs
        #     )
        # )


        for log_file in log_files:

            print("\n" + "=" * 80)

            print(
                f"Category : {log_file.parent.name}"
            )

            print(
                f"Testing File : {log_file.name}"
            )

            print("=" * 80)

            try:

                parsed_logs = uart_parser.parse_file(
                    log_file
                )

                classified_logs = (

                    kernel_parser.classify_logs(

                        parsed_logs

                    )

                )

                total_files += 1
                passed_files += 1
                total_classified_logs += len(
                    classified_logs
                )

                print(
                    "Status : PASS"
                )




                print("\n" + "=" * 60)
                print("KERNEL PARSER TEST")
                print("=" * 60)

                print(
                    f"\nTotal Classified Logs : "
                    f"{len(classified_logs)}"
                )

                print("\nFirst 5 Classified Logs:\n")

                for log in classified_logs[:5]:

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
                failed_files += 1
                total_files += 1
                print(
                    "Status : FAIL"
                )
                print(error)

        print("\n" + "=" * 70)

        print("KERNEL PARSER SUMMARY")

        print("=" * 70)

        print(
            f"Files Tested : {total_files}"
        )

        print(
            f"Files Passed : {passed_files}"
        )

        print(
            f"Files Failed : {failed_files}"
        )

        print(
            f"Total Classified Logs : "
            f"{total_classified_logs}"
        )

        print(
            f"Average Logs/File : "
            f"{round(total_classified_logs / total_files, 2)}"
        )

        print("=" * 70)

    except Exception as error:

        print("\nTest Failed")
        print(f"Error: {error}")


if __name__ == "__main__":
    main()