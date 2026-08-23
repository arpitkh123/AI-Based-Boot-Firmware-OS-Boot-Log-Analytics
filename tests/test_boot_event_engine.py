import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.append(
    str(PROJECT_ROOT)
)


from pathlib import Path

from src.parsers.uart_parser import UARTParser
from src.parsers.kernel_parser import KernelParser
from src.boot_engine.boot_event_engine import (
    BootEventEngine
)


DATASET = Path(
    "src/dataset/error_boot_logs"
)


uart_parser = UARTParser()

kernel_parser = KernelParser()

engine = BootEventEngine()


for file in sorted(DATASET.glob("*.txt")):

    print("\n" + "=" * 80)

# file = DATASET / "logs3_5june(uboot + some kernel).txt"

    print(file.name)

    parsed_logs = uart_parser.parse_file(file)

    classified_logs = (
        kernel_parser.classify_logs(
            parsed_logs
        )
    )

    events = engine.extract_events(
        classified_logs
    )

    print()

    for event in events:

        print(

            f"{event['event']:<20}"

            f"{event['stage']:<12}"

            f"{event['timestamp']}"

        )