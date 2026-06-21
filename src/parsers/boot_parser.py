# src/parsers/boot_parser.py

import logging
from typing import Dict, List, Optional

from src.config.parser_config import (
    KERNEL_START_KEYWORDS,
    ROOTFS_KEYWORDS,
    INIT_KEYWORDS,
    LOGIN_KEYWORDS,
    BOOT_SUCCESS_KEYWORDS,
    BOOT_FAILURE_KEYWORDS,
    KERNEL_PANIC_KEYWORDS,
)


logger = logging.getLogger(__name__)


class BootParser:
    """
    Analyzes classified boot logs and determines
    boot health, boot stages, and boot duration.
    """

    def _contains_keyword(
        self,
        message: str,
        keywords: List[str]
    ) -> bool:

        message = message.lower()

        return any(
            keyword.lower() in message
            for keyword in keywords
        )

    def _find_first_matching_log(
        self,
        logs: List[Dict],
        keywords: List[str]
    ) -> Optional[Dict]:

        for log in logs:

            message = log.get(
                "message",
                ""
            )

            if self._contains_keyword(
                message,
                keywords
            ):
                return log

        return None

    def detect_kernel_start(
        self,
        logs: List[Dict]
    ) -> bool:

        return (
            self._find_first_matching_log(
                logs,
                KERNEL_START_KEYWORDS
            )
            is not None
        )

    def detect_rootfs_mount(
        self,
        logs: List[Dict]
    ) -> bool:

        return (
            self._find_first_matching_log(
                logs,
                ROOTFS_KEYWORDS
            )
            is not None
        )

    def detect_init_start(
        self,
        logs: List[Dict]
    ) -> bool:

        return (
            self._find_first_matching_log(
                logs,
                INIT_KEYWORDS
            )
            is not None
        )

    # def detect_login_prompt(
    #     self,
    #     logs: List[Dict]
    # ) -> bool:

    #     return (
    #         self._find_first_matching_log(
    #             logs,
    #             LOGIN_KEYWORDS
    #         )
    #         is not None
    #     )

    def detect_login_prompt(
        self,
        logs: List[Dict]
    ) -> bool:

        matching_log = (
            self._find_first_matching_log(
                logs,
                LOGIN_KEYWORDS
            )
        )

        if matching_log:

            print(
                "\n[DEBUG] Login Prompt Match Found:"
            )

            print(
                matching_log
            )

        return matching_log is not None

    def detect_boot_success(
        self,
        logs: List[Dict]
    ) -> bool:

        return (
            self._find_first_matching_log(
                logs,
                BOOT_SUCCESS_KEYWORDS
            )
            is not None
        )

    def detect_kernel_panic(
        self,
        logs: List[Dict]
    ) -> bool:

        panic_log = self._find_first_matching_log(
            logs,
            KERNEL_PANIC_KEYWORDS
        )

        failure_log = self._find_first_matching_log(
            logs,
            BOOT_FAILURE_KEYWORDS
        )

        return (
            panic_log is not None
            or failure_log is not None
        )

    def determine_boot_stage(
        self,
        logs: List[Dict]
    ) -> str:

        if self.detect_boot_success(logs):
            return "BOOT_SUCCESS"

        if self.detect_login_prompt(logs):
            return "LOGIN_PROMPT"

        if self.detect_init_start(logs):
            return "INIT_STARTED"

        if self.detect_rootfs_mount(logs):
            return "ROOTFS_MOUNTED"

        if self.detect_kernel_start(logs):
            return "KERNEL_STARTED"

        return "BOOT_FAILED"

    def calculate_boot_duration(
        self,
        logs: List[Dict]
    ) -> float:

        success_log = (
            self._find_first_matching_log(
                logs,
                BOOT_SUCCESS_KEYWORDS
            )
        )

        if success_log:

            return float(
                success_log.get(
                    "timestamp",
                    0.0
                )
            )

        login_log = (
            self._find_first_matching_log(
                logs,
                LOGIN_KEYWORDS
            )
        )

        if login_log:

            return float(
                login_log.get(
                    "timestamp",
                    0.0
                )
            )

        if logs:

            return float(
                logs[-1].get(
                    "timestamp",
                    0.0
                )
            )

        return 0.0

    def count_severity(
        self,
        logs: List[Dict],
        severity: str
    ) -> int:

        return sum(
            1
            for log in logs
            if log.get(
                "severity"
            ) == severity
        )

    def analyze_boot(
        self,
        logs: List[Dict]
    ) -> Dict:

        try:

            kernel_started = (
                self.detect_kernel_start(
                    logs
                )
            )

            rootfs_mounted = (
                self.detect_rootfs_mount(
                    logs
                )
            )

            init_started = (
                self.detect_init_start(
                    logs
                )
            )

            login_prompt_detected = (
                self.detect_login_prompt(
                    logs
                )
            )

            custom_boot_marker_detected = (
                self.detect_boot_success(
                    logs
                )
            )

            kernel_panic_detected = (
                self.detect_kernel_panic(
                    logs
                )
            )

            boot_successful = (
                (
                    login_prompt_detected
                    or
                    custom_boot_marker_detected
                )
                and
                not kernel_panic_detected
            )

            result = {
                "kernel_started":
                    kernel_started,

                "rootfs_mounted":
                    rootfs_mounted,

                "init_started":
                    init_started,

                "login_prompt_detected":
                    login_prompt_detected,

                "custom_boot_marker_detected":
                    custom_boot_marker_detected,

                "kernel_panic_detected":
                    kernel_panic_detected,

                "boot_successful":
                    boot_successful,

                "boot_stage_reached":
                    self.determine_boot_stage(
                        logs
                    ),

                "boot_duration":
                    self.calculate_boot_duration(
                        logs
                    ),

                "error_count":
                    self.count_severity(
                        logs,
                        "ERROR"
                    ),

                "warning_count":
                    self.count_severity(
                        logs,
                        "WARNING"
                    ),
            }

            logger.info(
                "Boot analysis completed "
                "successfully."
            )

            return result

        except Exception as error:

            logger.exception(
                f"Boot analysis failed. "
                f"Reason: {error}"
            )

            raise