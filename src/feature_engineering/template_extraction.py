import logging
from typing import Dict, List

from drain3 import TemplateMiner
from drain3.template_miner_config import TemplateMinerConfig


logger = logging.getLogger(__name__)


class TemplateExtractor:

    def __init__(self):

        try:

            config = TemplateMinerConfig()

            self.template_miner = TemplateMiner(
                config=config
            )

            logger.info(
                "TemplateExtractor initialized successfully."
            )

        except Exception as error:

            logger.exception(
                f"Failed to initialize TemplateExtractor. "
                f"Reason: {error}"
            )

            raise

    def extract_templates(
        self,
        # logs: List[Dict]
        classified_logs: List[Dict]
    ) -> List[Dict]:

        try:

            template_counts = {}

            # for log in logs:
            for log in classified_logs:

                message = log.get(
                    "message",
                    ""
                )

                if not message:
                    continue

                result = (
                    self.template_miner.add_log_message(
                        message
                    )
                )

                # print("\nDEBUG RESULT:")
                # print(result)

                # break

                # cluster = result.get(
                #     "cluster"
                # )

                # if cluster is None:
                #     continue

                # cluster_id = cluster.cluster_id

                # template = (
                #     cluster.get_template()
                # )

                cluster_id = result.get(
                    "cluster_id"
                )

                template = result.get(
                    "template_mined"
                )

                if (
                    cluster_id is None
                    or
                    template is None
                ):
                    continue

                key = (
                    cluster_id,
                    template
                )


                if key not in template_counts:

                    template_counts[key] = {

                        "cluster_id":
                            cluster_id,

                        "template":
                            template,

                        "count":
                            0,

                        "severity_counts": {

                            "INFO": 0,

                            "WARNING": 0,

                            "ERROR": 0,

                            "SUCCESS": 0
                        },

                        "subsystem_counts": {}
                    }

                    # template_counts[key] = {

                    #     "cluster_id":
                    #         cluster_id,

                    #     "template":
                    #         template,

                    #     "count":
                    #         0,

                    #     "severity":
                    #         log.get(
                    #             "severity",
                    #             "UNKNOWN"
                    #         ),

                    #     "subsystem":
                    #         log.get(
                    #             "subsystem",
                    #             "UNKNOWN"
                    #         )
                    # }

                template_counts[key][
                    "count"
                ] += 1

                severity = log.get(
                    "severity",
                    "UNKNOWN"
                )

                if severity in template_counts[key]["severity_counts"]:

                    template_counts[key]["severity_counts"][
                        severity
                    ] += 1


                subsystem = log.get(
                    "subsystem",
                    "UNKNOWN"
                )

                template_counts[key]["subsystem_counts"][
                    subsystem
                ] = (

                    template_counts[key]["subsystem_counts"].get(
                        subsystem,
                        0
                    ) + 1
                )



                # if key not in template_counts:

                #     template_counts[key] = {
                #         "cluster_id":
                #             cluster_id,

                #         "template":
                #             template,

                #         "count":
                #             0
                #     }

                # template_counts[key][
                #     "count"
                # ] += 1

            # templates = list(
            #     template_counts.values()
            # )

            templates = sorted(
                template_counts.values(),
                key=lambda template: template["count"],
                reverse=True
            )

            logger.info(
                f"Extracted "
                f"{len(templates)} templates."
            )

            return templates

        except Exception as error:

            logger.exception(
                f"Template extraction failed. "
                f"Reason: {error}"
            )

            raise


    def get_template_statistics(
        self,
        templates: List[Dict]
    ) -> Dict:

        try:

            if not templates:

                return {

                    "total_templates": 0,

                    "total_occurrences": 0,

                    "largest_cluster": 0,

                    "smallest_cluster": 0,

                    "average_cluster_size": 0.0,

                    "repeated_templates": 0,

                    "compression_ratio": 0.0
                }

            total_templates = len(
                templates
            )

            total_occurrences = sum(

                template["count"]

                for template in templates
            )

            largest_cluster = max(

                template["count"]

                for template in templates
            )

            smallest_cluster = min(

                template["count"]

                for template in templates
            )

            average_cluster_size = (

                total_occurrences

                / total_templates
            )

            repeated_templates = sum(

                1

                for template in templates

                if template["count"] > 1
            )

            compression_ratio = round(

                total_templates
                / total_occurrences,

                4
            )

            return {

                "total_templates":
                    total_templates,

                "total_occurrences":
                    total_occurrences,

                "largest_cluster":
                    largest_cluster,

                "smallest_cluster":
                    smallest_cluster,

                "average_cluster_size":
                    round(
                        average_cluster_size,
                        2
                    ),

                "repeated_templates":
                    repeated_templates,

                "compression_ratio":
                    compression_ratio
            }

        except Exception as error:

            logger.exception(

                f"Failed to generate template "
                f"statistics. "
                f"Reason: {error}"
            )

            raise        

    # def get_template_statistics(
    #     self,
    #     templates: List[Dict]
    # ) -> Dict:

    #     try:

    #         total_templates = len(
    #             templates
    #         )

    #         total_occurrences = sum(
    #             template["count"]
    #             for template in templates
    #         )

    #         return {
    #             "total_templates":
    #                 total_templates,

    #             "total_occurrences":
    #                 total_occurrences
    #         }

    #     except Exception as error:

    #         logger.exception(
    #             f"Failed to generate template "
    #             f"statistics. "
    #             f"Reason: {error}"
    #         )

    #         raise