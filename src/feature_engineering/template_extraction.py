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
        logs: List[Dict]
    ) -> List[Dict]:

        try:

            template_counts = {}

            for log in logs:

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
                            0
                    }

                template_counts[key][
                    "count"
                ] += 1

            templates = list(
                template_counts.values()
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

            total_templates = len(
                templates
            )

            total_occurrences = sum(
                template["count"]
                for template in templates
            )

            return {
                "total_templates":
                    total_templates,

                "total_occurrences":
                    total_occurrences
            }

        except Exception as error:

            logger.exception(
                f"Failed to generate template "
                f"statistics. "
                f"Reason: {error}"
            )

            raise