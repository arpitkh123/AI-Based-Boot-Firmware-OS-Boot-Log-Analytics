import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.parsers.uart_parser import UARTParser

from collections import Counter



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

    
    parser = UARTParser()
    total_files = 0

    total_logs = 0

    passed_files = 0

    failed_files = 0

    try:

        log_files = get_all_log_files()

        print(
            f"\nFound {len(log_files)} log files.\n"
        )

        for log_file in log_files:

            print("=" * 80)

            print(
                f"Testing File : {log_file.name}"
            )

            print("=" * 80)

            logs = parser.parse_file(
                log_file
            )

            total_files += 1

            passed_files += 1

            total_logs += len(logs)

        # log_file = get_first_log_file()

        # print(f"\nTesting File: {log_file.name}")

        # logs = parser.parse_file(log_file)

            print("\n" + "=" * 60)
            print("UART PARSER TEST")
            print("=" * 60)

            print(f"\nTotal Parsed Logs : {len(logs)}")

        # print("\nFirst 5 Log Entries:\n")

        # for log in logs[:5]:
        #     print(log)

            print("\nFirst 5 Parsed Entries:\n")

            for log in logs[:5]:

                print(
                    f"Line      : {log['line_number']}"
                )

                print(
                    f"Timestamp : {log['timestamp']}"
                )

                # print(
                #     f"Stage     : {log['stage']}"
                # )

                # Use .get() so it doesn't crash if 'stage' is missing
                print(f"Stage     : {log.get('stage', 'N/A')}")

                print(
                    f"Message   : {log['message']}"
                )

                print("-" * 60)

            print("\nStatistics:\n")

            stats = parser.get_basic_statistics(logs)

            for key, value in stats.items():
                print(f"{key}: {value}")

            print("\nTest Completed Successfully")

            stage_counter = Counter()

            for log in logs:

                # Again, use .get() to catch missing keys
                stage_name = log.get("stage", "UNKNOWN")
                stage_counter[stage_name] += 1

                # stage_counter[log["stage"]] += 1

            print("\nStage Summary\n")

            for stage, count in stage_counter.items():

                print(f"{stage:<10}: {count}")

            print("\n")

        print("\n" + "=" * 70)

        print("UART PARSER SUMMARY")

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
            f"Total Parsed Logs : {total_logs}"
        )

        print(
            f"Average Logs/File : "
            f"{round(total_logs / total_files, 2)}"
        )

        print("=" * 70)

    except Exception as error:

        print("\nTest Failed")
        print(f"Error: {error}")


if __name__ == "__main__":
    main()