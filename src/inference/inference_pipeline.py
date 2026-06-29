from pathlib import Path

import logging

from src.parsers.uart_parser import UARTParser
from src.parsers.kernel_parser import KernelParser

# from src.boot_engine.boot_parser import BootParser
from src.parsers.boot_parser import BootParser

from src.feature_engineering.template_extraction import (
    TemplateExtractor
)

from src.feature_engineering.feature_builder import (
    FeatureBuilder
)

from src.models.iforest import (
    IsolationForestModel
)

from src.inference.llm_explainer import (
    LLMExplainer
)


logger = logging.getLogger(__name__)


class InferencePipeline:
    """
    Complete AI Boot Log
    Inference Pipeline.
    """

    def __init__(self):

        logger.info(
            "Initializing Inference Pipeline..."
        )

        self.uart_parser = (
            UARTParser()
        )

        self.kernel_parser = (
            KernelParser()
        )

        self.boot_parser = (
            BootParser()
        )

        self.template_extractor = (
            TemplateExtractor()
        )

        self.feature_builder = (
            FeatureBuilder()
        )

        self.detector = (
            IsolationForestModel()
        )

        self.detector.load_model()

        self.llm = (
            LLMExplainer()
        )

        logger.info(
            "Inference Pipeline Initialized Successfully."
        )




    def run(
        self,
        log_file: str | Path
    ):
        """
        Run the complete
        parsing pipeline.
        """
        try:

            log_file = Path(
                log_file
            )

            logger.info(

                f"Starting inference for: "

                f"{log_file.name}"

            )

            # --------------------------------------------------
            # Step 1 : UART Parsing
            # --------------------------------------------------

            parsed_logs = (

                self.uart_parser.parse_file(

                    log_file

                )

            )

            logger.info(

                f"UART Parser : "

                f"{len(parsed_logs)} logs parsed."

            )

            # --------------------------------------------------
            # Step 2 : Kernel Classification
            # --------------------------------------------------

            classified_logs = (

                self.kernel_parser.classify_logs(

                    parsed_logs

                )

            )

            logger.info(

                "Kernel Parser Completed."

            )

            # --------------------------------------------------
            # Step 3 : Boot Analysis
            # --------------------------------------------------

            boot_analysis = (

                self.boot_parser.analyze_boot(

                    classified_logs

                )

            )

            logger.info(

                "Boot Analysis Completed."

            )

            # --------------------------------------------------
            # Step 4 : Template Extraction
            # --------------------------------------------------

            templates = (

                self.template_extractor.extract_templates(

                    classified_logs

                )

            )

            logger.info(

                f"Extracted "

                f"{len(templates)} templates."

            )







        # --------------------------------------------------
            # Step 5 : Feature Extraction
            # --------------------------------------------------

            feature_vector = (

                self.feature_builder.build_features(

                    classified_logs=classified_logs,

                    boot_analysis=boot_analysis,

                    templates=templates

                )

            )

            logger.info(

                "Feature Extraction Completed."

            )

            # --------------------------------------------------
            # Step 6 : ML Prediction
            # --------------------------------------------------

            anomaly_result = (

                self.detector.predict_feature_vector(

                    feature_vector

                )

            )

            logger.info(

                "Isolation Forest Prediction Completed."

            )

            # --------------------------------------------------
            # Step 7 : LLM Explanation
            # --------------------------------------------------

            report = (

                self.llm.explain(

                    file_name=log_file.name,

                    boot_analysis=boot_analysis,

                    anomaly_result=anomaly_result

                )

            )

            logger.info(

                "LLM Explanation Generated."

            )


            logger.info(

                "Inference Completed Successfully."

            )

            return {

                "metadata":

                    report["metadata"],

                "boot_analysis":

                    boot_analysis,

                "feature_vector":

                    feature_vector,

                "anomaly_result":

                    anomaly_result,

                "llm_explanation":

                    report["llm_explanation"]

            }
        
        except Exception as error:

            logger.exception(

                "Inference Pipeline Failed."

            )

            raise RuntimeError(

                f"Inference failed: {error}"

            )