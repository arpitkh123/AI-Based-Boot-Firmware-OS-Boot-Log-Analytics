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


# def get_first_log_file():

#     dataset_path = Path(
#         "src/dataset/normal_boot_logs"
#     )

#     log_files = list(
#         dataset_path.glob("*")
#     )

#     if not log_files:

#         raise FileNotFoundError(
#             f"No log files found in "
#             f"{dataset_path}"
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

        # print(
        #     f"\nTesting File: "
        #     f"{log_file.name}"
        # )

        log_files = get_all_log_files()

        print(
            f"\nFound {len(log_files)} log files.\n"
        )

        uart_parser = UARTParser()

        # parsed_logs = (
        #     uart_parser.parse_file(
        #         log_file
        #     )
        # )

        kernel_parser = KernelParser()

        # classified_logs = (
        #     kernel_parser.classify_logs(
        #         parsed_logs
        #     )
        # )

        extractor = (
            TemplateExtractor()
        )

        total_files = 0

        passed_files = 0

        failed_files = 0

        total_templates = 0

        compression_ratios = []

        # templates = (
        #     extractor.extract_templates(
        #         classified_logs
        #     )
        # )

        # stats = (
        #     extractor.get_template_statistics(
        #         templates
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

                parsed_logs = (
                    uart_parser.parse_file(
                        log_file
                    )
                )

                # kernel_parser = KernelParser()

                classified_logs = (

                    kernel_parser.classify_logs(

                        parsed_logs

                    )

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

                total_files += 1

                passed_files += 1

                total_templates += stats[
                    "total_templates"
                ]

                compression_ratios.append(

                    stats[
                        "compression_ratio"
                    ]

                )

                print(
                    "Status : PASS"
                )

            except Exception as error:

                total_files += 1

                failed_files += 1

                print(
                    "Status : FAIL"
                )

                print(error)

                continue

            print(
                f"Largest Cluster : "
                f"{stats['largest_cluster']}"
            )

            print(
                f"Smallest Cluster : "
                f"{stats['smallest_cluster']}"
            )

            print(
                f"Average Cluster Size : "
                f"{stats['average_cluster_size']}"
            )

            print(
                f"Repeated Templates : "
                f"{stats['repeated_templates']}"
            )

            print(
                f"Compression Ratio : "
                f"{stats['compression_ratio']}"
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

            for template in templates[:10]:

                print(
                    f"\nCluster ID : "
                    f"{template['cluster_id']}"
                )

                print(
                    f"Count      : "
                    f"{template['count']}"
                )

                print(
                    f"Severity   : "
                    f"{template['severity_counts']}"
                )

                print(
                    f"Subsystem  : "
                    f"{template['subsystem_counts']}"
                )

                print(
                    f"Template   : "
                    f"{template['template']}"
                )

                print("-" * 70)

        # print(
        #     "\nTemplate Extraction "
        #     "Test Completed Successfully"
        # )

        print("\n" + "=" * 70)

        print("TEMPLATE EXTRACTION SUMMARY")

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
            f"Total Templates : {total_templates}"
        )

        print(
            f"Average Templates/File : "
            f"{round(total_templates / total_files, 2)}"
        )

        print(
            f"Average Compression Ratio : "
            f"{round(sum(compression_ratios) / len(compression_ratios), 4)}"
        )

        print("=" * 70)

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