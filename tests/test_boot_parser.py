import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from pathlib import Path

from src.parsers.uart_parser import UARTParser
from src.parsers.kernel_parser import KernelParser
from src.parsers.boot_parser import BootParser


# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------

DATASET_PATH = Path("src/dataset/error_boot_logs")


# ---------------------------------------------------------------------
# Initialize Parsers
# ---------------------------------------------------------------------

uart_parser = UARTParser()
kernel_parser = KernelParser()
boot_parser = BootParser()


# ---------------------------------------------------------------------
# Collect Log Files
# ---------------------------------------------------------------------

log_files = sorted(DATASET_PATH.glob("*.txt"))

if not log_files:
    raise FileNotFoundError(
        f"No log files found in {DATASET_PATH}"
    )


print("\n" + "=" * 90)
print("BOOT PARSER TEST")
print("=" * 90)


# ---------------------------------------------------------------------
# Test Every Log File
# ---------------------------------------------------------------------

for index, log_file in enumerate(log_files, start=1):

    print(f"\n[{index}/{len(log_files)}]")
    print(f"Testing File : {log_file.name}")

    try:

        # -------------------------------------------------------------
        # UART Parsing
        # -------------------------------------------------------------

        parsed_logs = uart_parser.parse_file(log_file)

        # -------------------------------------------------------------
        # Kernel Classification
        # -------------------------------------------------------------

        classified_logs = kernel_parser.classify_logs(
            parsed_logs
        )

        # -------------------------------------------------------------
        # Boot Analysis
        # -------------------------------------------------------------

        result = boot_parser.analyze_boot(
            classified_logs
        )

        print("-" * 70)

        print(
            f"Boot Successful : "
            f"{result['boot_successful']}"
        )

        print(
            f"Boot Stage      : "
            f"{result['boot_stage_reached']}"
        )

        print(
            f"Failure Type    : "
            f"{result['failure_type']}"
        )

        print(
            f"Failure Reason  : "
            f"{result['failure_reason']}"
        )

        print(
            f"Boot Duration   : "
            f"{result['boot_duration']}"
        )

        print(
            f"Kernel Panic    : "
            f"{result['kernel_panic_detected']}"
        )

        print(
            f"IRQ Failure     : "
            f"{boot_parser.detect_irq_failure(classified_logs)}"
        )

        print(
            f"DMA Failure     : "
            f"{boot_parser.detect_dma_failure(classified_logs)}"
        )

        print(
            f"RootFS Failure  : "
            f"{boot_parser.detect_rootfs_failure(classified_logs)}"
        )

        print(
            f"DTB Failure     : "
            f"{boot_parser.detect_dtb_failure(classified_logs)}"
        )

        print(
            f"OOM Detected    : "
            f"{boot_parser.detect_oom(classified_logs)}"
        )

        print(
            f"CPU Failure     : "
            f"{boot_parser.detect_cpu_failure(classified_logs)}"
        )

        print(
            f"Filesystem Fail : "
            f"{boot_parser.detect_filesystem_failure(classified_logs)}"
        )

        print(
            f"Init Failure    : "
            f"{boot_parser.detect_init_failure(classified_logs)}"
        )

        print(
            f"Errors          : "
            f"{result['error_count']}"
        )

        print(
            f"Warnings        : "
            f"{result['warning_count']}"
        )

    except Exception as error:

        print("\nTest Failed")
        print(error)

        break


print("\n" + "=" * 90)
print("Boot Parser Test Completed Successfully")
print("=" * 90)






# # tests/test_boot_parser.py

# import sys
# from pathlib import Path

# sys.path.insert(
#     0,
#     str(Path(__file__).resolve().parent.parent)
# )

# from src.parsers.uart_parser import UARTParser
# from src.parsers.kernel_parser import KernelParser
# from src.parsers.boot_parser import BootParser


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


# def main():

#     try:

#         log_file = get_first_log_file()

#         print(
#             f"\nTesting File: "
#             f"{log_file.name}"
#         )

#         uart_parser = UARTParser()

#         parsed_logs = (
#             uart_parser.parse_file(
#                 log_file
#             )
#         )

#         kernel_parser = KernelParser()

#         classified_logs = (
#             kernel_parser.classify_logs(
#                 parsed_logs
#             )
#         )

#         boot_parser = BootParser()

#         boot_analysis = (
#             boot_parser.analyze_boot(
#                 classified_logs
#             )
#         )

#         print("\n" + "=" * 60)
#         print("BOOT PARSER TEST")
#         print("=" * 60)

#         print("\nBoot Analysis Results:\n")

#         for key, value in (
#             boot_analysis.items()
#         ):

#             print(
#                 f"{key:<35} "
#                 f": {value}"
#             )

#         print(
#             "\nBoot Parser Test "
#             "Completed Successfully"
#         )

#     except Exception as error:

#         print("\nTest Failed")
#         print(
#             f"Error: {error}"
#         )


# if __name__ == "__main__":
#     main()