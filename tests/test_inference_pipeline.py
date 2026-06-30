import sys
from pathlib import Path

sys.path.insert(
    0,
    str(
        Path(__file__).resolve().parent.parent
    )
)

from src.inference.inference_pipeline import (
    InferencePipeline
)


def get_first_log_file():

    dataset_paths = [

        Path(
            "src/dataset/normal_boot_logs"
        ),

        Path(
            "src/dataset/error_boot_logs"
        )

    ]

    for folder in dataset_paths:

        if folder.exists():

            log_files = sorted(

                folder.glob("*.txt")

            )

            if log_files:

                return log_files[0]

    raise FileNotFoundError(

        "No log files found."

    )


def main():

    print("\n" + "=" * 80)

    print(
        "COMPLETE AI INFERENCE PIPELINE TEST"
    )

    print("=" * 80)

    log_file = get_first_log_file()

    print(

        f"\nTesting File : "

        f"{log_file.name}"

    )

    pipeline = InferencePipeline()

    report = pipeline.run(

        log_file

    )

    print("\n")

    print("=" * 80)

    print("FINAL AI REPORT")

    print("=" * 80)

    print("\nMetadata")

    print("-" * 80)

    print(

        report["metadata"]

    )

    print("\nBoot Analysis")

    print("-" * 80)

    for key, value in report[

        "boot_analysis"

    ].items():

        print(

            f"{key:<30}: {value}"

        )

    print("\nAnomaly Result")

    print("-" * 80)

    for key, value in report[

        "anomaly_result"

    ].items():

        print(

            f"{key:<30}: {value}"

        )

    print("\nFeature Vector")

    print("-" * 80)

    for key, value in report[

        "feature_vector"

    ].items():

        print(

            f"{key:<30}: {value}"

        )

    print("\nLLM Explanation")

    print("-" * 80)

    print(

        report["llm_explanation"]

    )

    print("\n")

    print("=" * 80)

    print(

        "END-TO-END PIPELINE EXECUTED SUCCESSFULLY"

    )

    print("=" * 80)


if __name__ == "__main__":

    main()