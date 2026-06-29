from typing import Dict
import time

from src.inference.prompt_builder import (
    PromptBuilder
)

from src.inference.providers.gemini_provider import (
    GeminiProvider
)

from src.inference.report_generator import (
    ReportGenerator
)


class LLMExplainer:
    """
    Coordinates the complete
    LLM inference pipeline.
    """

    def __init__(
        self
    ):

        self.prompt_builder = (

            PromptBuilder()

        )

        self.provider = (

            GeminiProvider()

        )

        self.report_generator = (

            ReportGenerator()

        )

    def explain(
        self,
        file_name: str,
        boot_analysis: Dict,
        anomaly_result: Dict
    ) -> Dict:
        """
        Generate a complete
        AI explanation report.
        """

        start_time = time.perf_counter()

        prompt = (

            self.prompt_builder

            .build_prompt(

                boot_analysis,

                anomaly_result

            )

        )

        llm_response = (

            self.provider.generate(

                prompt

            )

        )


        processing_time = (

            time.perf_counter()

            - start_time

        )

        report = (

            self.report_generator.generate(

                file_name=file_name,

                boot_analysis=boot_analysis,

                anomaly_result=anomaly_result,

                llm_response=llm_response,

                processing_time=processing_time

            )

        )





        # report = (

        #     self.report_generator.generate(

        #         boot_analysis=boot_analysis,

        #         anomaly_result=anomaly_result,

        #         llm_response=llm_response

        #     )

        # )

        return report