from pathlib import Path

import sys


sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)


# PROJECT_ROOT = (

#     Path(__file__)

#     .resolve()

#     .parent

#     .parent

# )

# if str(PROJECT_ROOT) not in sys.path:

#     sys.path.insert(

#         0,

#         str(PROJECT_ROOT)

#     )


from src.inference.llm_explainer import (
    LLMExplainer
)


def main():

    boot_analysis = {

        "boot_successful": False,

        "boot_duration": 2.31,

        "kernel_started": True,

        "rootfs_mounted": False,

        "init_started": False,

        "login_prompt_detected": False,

        "kernel_panic_detected": True,

        "error_count": 18,

        "warning_count": 4,

        "failure_type": "ROOTFS_FAILURE",

        "failure_reason": "Unable to mount root filesystem"

    }

    anomaly_result = {

        "prediction": "ANOMALY",

        "anomaly_score": -0.1422,

        "anomaly_strength": 14.22

    }

    explainer = (

        LLMExplainer()

    )

    # report = (

    #     explainer.explain(

    #         boot_analysis,

    #         anomaly_result

    #     )

    # )


    report = (

        explainer.explain(

            file_name="sample_boot_log.txt",

            boot_analysis=boot_analysis,

            anomaly_result=anomaly_result

        )

    )

    print("\n")

    print("=" * 80)

    print("LLM INFERENCE REPORT")

    print("=" * 80)

    print()

    # print()

    print("Metadata")

    print("-" * 80)

    print(

        report["metadata"]

    )

    print("Boot Analysis")

    print("-" * 80)

    print(

        report["boot_analysis"]

    )

    print()

    print("Anomaly Result")

    print("-" * 80)

    print(

        report["anomaly_result"]

    )

    print()

    print("LLM Explanation")

    print("-" * 80)

    print(

        report["llm_explanation"]

    )

    print()

    print("=" * 80)

    print("Inference Test Completed Successfully.")

    print("=" * 80)


if __name__ == "__main__":

    main()