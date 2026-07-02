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

from src.rules.rule_engine import RuleEngine
from src.fusion.confidence_fusion import ConfidenceFusion


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

        self.rule_engine = RuleEngine()
        self.fusion_engine = ConfidenceFusion()

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

            uart_statistics = (
                self.uart_parser.get_basic_statistics(
                    parsed_logs
                )
            )

            kernel_statistics = (
                self.kernel_parser.get_statistics(
                    classified_logs
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

            template_statistics = (
                self.template_extractor.get_template_statistics(
                    templates
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
            # Step 6.5 : Rule Engine & Confidence Fusion
            # --------------------------------------------------
            
            rule_anomalies = self.rule_engine.evaluate(classified_logs, boot_analysis)
            
            fusion_result = self.fusion_engine.calculate_confidence(
                rule_anomalies=rule_anomalies,
                ml_anomaly=anomaly_result,
                boot_analysis=boot_analysis,
                template_stats=template_statistics
            )

            logger.info(
                f"Confidence Fusion Completed. Score: {fusion_result['anomaly_strength']}%"
            )

            # --------------------------------------------------
            # Step 7 : LLM Explanation
            # --------------------------------------------------
            
            kb_matches = [a for a in rule_anomalies if "kb_resolution" in a]
            if kb_matches:
                resolution_text = "\n".join([f"- {a['reason']}: {a['kb_resolution']}" for a in kb_matches])
                report = {
                    "metadata": {"processing_time_seconds": 0.0},
                    "llm_explanation": f"**Known Failure Detected (Bypassed AI)**\n{resolution_text}"
                }
                logger.info("LLM Explainer bypassed due to high-confidence Knowledge Base match.")
            else:
                report = (
                    self.llm.explain(
                        file_name=log_file.name,
                        boot_analysis=boot_analysis,
                        anomaly_result=fusion_result
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

                "uart_statistics":
                    uart_statistics,

                "kernel_statistics":
                    kernel_statistics,

                "boot_analysis":
                    boot_analysis,

                "template_statistics":
                    template_statistics,

                "templates":
                    templates,

                "feature_vector":
                    feature_vector,

                "anomaly_result":
                    fusion_result,

                "llm_explanation":
                    report["llm_explanation"]
            }





            # return {

            #     "metadata":

            #         report["metadata"],

            #     "boot_analysis":

            #         boot_analysis,

            #     "feature_vector":

            #         feature_vector,

            #     "anomaly_result":

            #         anomaly_result,

            #     "llm_explanation":

            #         report["llm_explanation"]

            # }
        
        except Exception as error:

            logger.exception(

                "Inference Pipeline Failed."

            )

            raise RuntimeError(

                f"Inference failed: {error}"

            )