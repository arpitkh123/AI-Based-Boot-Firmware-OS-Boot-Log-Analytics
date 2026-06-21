import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.parsers.uart_parser import UARTParser



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

    parser = UARTParser()

    try:

        log_file = get_first_log_file()

        print(f"\nTesting File: {log_file.name}")

        logs = parser.parse_file(log_file)

        print("\n" + "=" * 60)
        print("UART PARSER TEST")
        print("=" * 60)

        print(f"\nTotal Parsed Logs : {len(logs)}")

        print("\nFirst 5 Log Entries:\n")

        for log in logs[:5]:
            print(log)

        print("\nStatistics:\n")

        stats = parser.get_basic_statistics(logs)

        for key, value in stats.items():
            print(f"{key}: {value}")

        print("\nTest Completed Successfully")

    except Exception as error:

        print("\nTest Failed")
        print(f"Error: {error}")


if __name__ == "__main__":
    main()