from datetime import datetime

from typing import Dict

from src.config.settings import (
    Settings
)


class ReportGenerator:
    """
    Generate the final
    inference report.
    """

    def generate(
        self,
        file_name: str,
        boot_analysis: Dict,
        anomaly_result: Dict,
        llm_response: str,
        processing_time: float
    ) -> Dict:

        report = {

            "metadata": {

                "file_name": file_name,

                "timestamp": (

                    datetime.now()

                    .strftime(

                        "%Y-%m-%d %H:%M:%S"

                    )

                ),

                "processing_time_seconds":

                    round(

                        processing_time,

                        3

                    ),

                "llm_provider":

                    Settings.LLM_PROVIDER,

                "llm_model":

                    Settings.MODEL_NAME

            },

            "boot_analysis":

                boot_analysis,

            "anomaly_result":

                anomaly_result,

            "llm_explanation":

                llm_response

        }

        return report




# from typing import Dict


# class ReportGenerator:
#     """
#     Generates the final
#     inference report by
#     combining ML results
#     and LLM explanation.
#     """

#     def generate(
#         self,
#         boot_analysis: Dict,
#         anomaly_result: Dict,
#         llm_response: str
#     ) -> Dict:
#         """
#         Generate the final
#         structured report.
#         """

#         report = {

#             "boot_analysis":

#                 boot_analysis,

#             "anomaly_result":

#                 anomaly_result,

#             "llm_explanation":

#                 llm_response

#         }

#         return report