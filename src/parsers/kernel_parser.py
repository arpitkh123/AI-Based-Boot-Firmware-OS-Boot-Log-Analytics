# src/parsers/kernel_parser.py

import logging
from typing import Dict, List

from src.config.parser_config import (
    SEVERITY_KEYWORDS,
    SUBSYSTEM_KEYWORDS
)


logger = logging.getLogger(__name__)


class KernelParser:
    """
    Classifies parsed UART log entries into:

    1. Severity
       - ERROR
       - WARNING
       - SUCCESS
       - INFO

    2. Subsystem
       - UART
       - NETWORK
       - FILESYSTEM
       - USB
       - MEMORY
       - BOOT
       - KERNEL
    """

    

    def determine_severity(self, message: str) -> str:
        """
        Determine severity level from message.
        """

        try:

            message = message.lower()

            for severity, keywords in SEVERITY_KEYWORDS.items():

                if any(keyword in message for keyword in keywords):
                    return severity

            return "INFO"

        except Exception as error:

            logger.exception(
                f"Failed to determine severity. Reason: {error}"
            )

            return "INFO"

    def determine_subsystem(self, message: str) -> str:
        """
        Determine subsystem from message.
        """

        try:

            message = message.lower()

            for subsystem, keywords in SUBSYSTEM_KEYWORDS.items():

                if any(keyword in message for keyword in keywords):
                    return subsystem

            return "KERNEL"

        except Exception as error:

            logger.exception(
                f"Failed to determine subsystem. Reason: {error}"
            )

            return "KERNEL"

    def classify_log(self, log: Dict) -> Dict:
        """
        Classify a single log entry.
        """

        try:

            if not isinstance(log, dict):
                raise TypeError(
                    "Expected log entry to be a dictionary."
                )

            message = log.get("message", "")

            classified_log = log.copy()

            classified_log["severity"] = (
                self.determine_severity(message)
            )

            classified_log["subsystem"] = (
                self.determine_subsystem(message)
            )

            return classified_log

        except Exception as error:

            logger.exception(
                f"Failed to classify log entry. Reason: {error}"
            )

            raise

    def classify_logs(
        self,
        logs: List[Dict]
    ) -> List[Dict]:
        """
        Classify multiple log entries.
        """

        classified_logs = []

        try:

            for log in logs:

                try:

                    classified_logs.append(
                        self.classify_log(log)
                    )

                except Exception as error:

                    logger.error(
                        f"Skipping invalid log entry. "
                        f"Reason: {error}"
                    )

            logger.info(
                f"Successfully classified "
                f"{len(classified_logs)} log entries."
            )

            return classified_logs

        except Exception as error:

            logger.exception(
                f"Failed to classify logs. Reason: {error}"
            )

            raise