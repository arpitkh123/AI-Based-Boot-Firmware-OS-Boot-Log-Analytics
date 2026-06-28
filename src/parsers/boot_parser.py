# src/parsers/boot_parser.py

import logging
from typing import Dict, List, Optional

from src.config.boot_parser_config import (
    KERNEL_START_KEYWORDS,
    ROOTFS_KEYWORDS,
    INIT_KEYWORDS,
    LOGIN_KEYWORDS,
    BOOT_SUCCESS_KEYWORDS,
    BOOT_FAILURE_KEYWORDS,
    KERNEL_PANIC_KEYWORDS,
    IRQ_FAILURE_KEYWORDS,
    DMA_FAILURE_KEYWORDS,
    ROOTFS_FAILURE_KEYWORDS,
    DTB_FAILURE_KEYWORDS,
    OOM_KEYWORDS,
    INIT_FAILURE_KEYWORDS,
    CPU_FAILURE_KEYWORDS,
    FILESYSTEM_FAILURE_KEYWORDS,
    FAILURE_PRIORITY,
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

        message = message.lower().strip()

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
    
    def _detect_failure(
        self,
        logs: List[Dict],
        keywords: List[str]
    ) -> bool:

        return (
            self._find_first_matching_log(
                logs,
                keywords
            )
            is not None
        )
    

    def detect_irq_failure(self, logs: List[Dict]) -> bool:
        return self._detect_failure(logs, IRQ_FAILURE_KEYWORDS)


    def detect_dma_failure(self, logs: List[Dict]) -> bool:
        return self._detect_failure(logs, DMA_FAILURE_KEYWORDS)


    def detect_rootfs_failure(self, logs: List[Dict]) -> bool:
        return self._detect_failure(logs, ROOTFS_FAILURE_KEYWORDS)


    def detect_dtb_failure(self, logs: List[Dict]) -> bool:
        return self._detect_failure(logs, DTB_FAILURE_KEYWORDS)


    def detect_oom(self, logs: List[Dict]) -> bool:
        return self._detect_failure(logs, OOM_KEYWORDS)


    def detect_init_failure(self, logs: List[Dict]) -> bool:
        return self._detect_failure(logs, INIT_FAILURE_KEYWORDS)


    def detect_cpu_failure(self, logs: List[Dict]) -> bool:
        return self._detect_failure(logs, CPU_FAILURE_KEYWORDS)


    def detect_filesystem_failure(self, logs: List[Dict]) -> bool:
        return self._detect_failure(logs, FILESYSTEM_FAILURE_KEYWORDS)

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

            logger.debug(
                "\n[DEBUG] Login Prompt Match Found:"
            )

            logger.debug(
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
        boot_successful: bool,
        login_prompt_detected: bool,
        init_started: bool,
        rootfs_mounted: bool,
        kernel_started: bool
    ) -> str:
        
        if boot_successful:
            return "BOOT_SUCCESS"

        if login_prompt_detected:
            return "LOGIN_PROMPT"

        if init_started:
            return "INIT_STARTED"

        if rootfs_mounted:
            return "ROOTFS_MOUNTED"

        if kernel_started:
            return "KERNEL_STARTED"

        return "BOOT_FAILED"

        # if self.detect_boot_success(logs):
        #     return "BOOT_SUCCESS"

        # if self.detect_login_prompt(logs):
        #     return "LOGIN_PROMPT"

        # if self.detect_init_start(logs):
        #     return "INIT_STARTED"

        # if self.detect_rootfs_mount(logs):
        #     return "ROOTFS_MOUNTED"

        # if self.detect_kernel_start(logs):
        #     return "KERNEL_STARTED"

        # return "BOOT_FAILED"
    



    def calculate_boot_duration(
        self,
        logs: List[Dict]
    ) -> float | None:

        timestamps = [

            log.get("timestamp")

            for log in logs

            if log.get("timestamp") is not None
        ]

        if not timestamps:
            return 0.0

        return round(
            timestamps[-1] - timestamps[0],
            6
        )
    




    # def calculate_boot_duration(
    #     self,
    #     logs: List[Dict]
    # ) -> float:

    #     success_log = (
    #         self._find_first_matching_log(
    #             logs,
    #             BOOT_SUCCESS_KEYWORDS
    #         )
    #     )

    #     if success_log:

    #         return float(
    #             success_log.get(
    #                 "timestamp",
    #                 0.0
    #             )
    #         )

    #     login_log = (
    #         self._find_first_matching_log(
    #             logs,
    #             LOGIN_KEYWORDS
    #         )
    #     )

    #     if login_log:

    #         return float(
    #             login_log.get(
    #                 "timestamp",
    #                 0.0
    #             )
    #         )

    #     if logs:

    #         return float(
    #             logs[-1].get(
    #                 "timestamp",
    #                 0.0
    #             )
    #         )

    #     return 0.0

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

    # def _determine_failure_type(
    #     self,
    #     logs: List[Dict]
    # ) -> Dict:
    #     """
    #     Determine the primary boot failure.

    #     Returns
    #     -------
    #     {
    #         "failure_type": ...,
    #         "failure_reason": ...,
    #         "failure_log": ...
    #     }
    #     """

    #     failure_checks = [

    #         (
    #             self.detect_dtb_failure,
    #             "DTB_FAILURE",
    #             "Device Tree Blob (DTB) could not be loaded."
    #         ),

    #         (
    #             self.detect_rootfs_failure,
    #             "ROOTFS_FAILURE",
    #             "Root filesystem could not be mounted."
    #         ),

    #         (
    #             self.detect_init_failure,
    #             "INIT_FAILURE",
    #             "Init process could not be started."
    #         ),

    #         (
    #             self.detect_dma_failure,
    #             "DMA_FAILURE",
    #             "DMA allocation failed."
    #         ),

    #         (
    #             self.detect_irq_failure,
    #             "IRQ_FAILURE",
    #             "Interrupt initialization failed."
    #         ),

    #         (
    #             self.detect_cpu_failure,
    #             "CPU_FAILURE",
    #             "CPU initialization failed."
    #         ),

    #         (
    #             self.detect_filesystem_failure,
    #             "FILESYSTEM_FAILURE",
    #             "Filesystem corruption or I/O failure detected."
    #         ),

    #         (
    #             self.detect_oom,
    #             "OOM",
    #             "Out Of Memory condition detected."
    #         ),

    #         (
    #             self.detect_kernel_panic,
    #             "KERNEL_PANIC",
    #             "Kernel panic detected."
    #         ),
    #     ]

    #     for detector, failure_type, reason in failure_checks:

    #         if detector(logs):

    #             return {

    #                 "failure_type":
    #                     failure_type,

    #                 "failure_reason":
    #                     reason,

    #                 "failure_log":
    #                     self._find_first_matching_log(
    #                         logs,
    #                         self._get_keywords(
    #                             failure_type
    #                         )
    #                     )
    #             }

    #     return {

    #         "failure_type": None,

    #         "failure_reason": None,

    #         "failure_log": None
    #     }


    def _determine_failure_type(
        self,
        logs: List[Dict]
    ) -> Dict:
        """
        Determine the primary failure based on
        configured failure priority.
        """

        for failure in FAILURE_PRIORITY:

            matching_log = self._find_first_matching_log(

                logs,

                failure["keywords"]
            )

            if matching_log:

                return {

                    "failure_type":
                        failure["name"],

                    "failure_reason":
                        failure["reason"],

                    "failure_log":
                        matching_log
                }

        return {

            "failure_type": None,

            "failure_reason": None,

            "failure_log": None
        }
    

    # def _get_keywords(
    #     self,
    #     failure_type: str
    # ) -> List[str]:

    #     keyword_map = {

    #         "DTB_FAILURE":
    #             DTB_FAILURE_KEYWORDS,

    #         "ROOTFS_FAILURE":
    #             ROOTFS_FAILURE_KEYWORDS,

    #         "INIT_FAILURE":
    #             INIT_FAILURE_KEYWORDS,

    #         "DMA_FAILURE":
    #             DMA_FAILURE_KEYWORDS,

    #         "IRQ_FAILURE":
    #             IRQ_FAILURE_KEYWORDS,

    #         "CPU_FAILURE":
    #             CPU_FAILURE_KEYWORDS,

    #         "FILESYSTEM_FAILURE":
    #             FILESYSTEM_FAILURE_KEYWORDS,

    #         "OOM":
    #             OOM_KEYWORDS,

    #         "KERNEL_PANIC":
    #             KERNEL_PANIC_KEYWORDS,
    #     }

    #     return keyword_map.get(
    #         failure_type,
    #         []
    #     )



    def analyze_boot(
        self,
        logs: List[Dict]
    ) -> Dict:

        try:

            if not logs:
                logger.warning(
                    "No boot logs available for analysis."
                )

                return {
                    "boot_successful": False,
                    "boot_stage_reached": "BOOT_FAILED",
                    "boot_duration": None,
                    "failure_type": None,
                    "failure_reason": None,
                    "failure_log": None,
                    "kernel_started": False,
                    "rootfs_mounted": False,
                    "init_started": False,
                    "login_prompt_detected": False,
                    "custom_boot_marker_detected": False,
                    "kernel_panic_detected": False,
                    "error_count": 0,
                    "warning_count": 0,
                }

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

            failure_details = (
                self._determine_failure_type(
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

                "failure_type":
                    failure_details["failure_type"],

                "failure_reason":
                    failure_details["failure_reason"],

                "failure_log":
                    failure_details["failure_log"],

                "boot_stage_reached":
                    self.determine_boot_stage(
                        boot_successful,

                        login_prompt_detected,

                        init_started,

                        rootfs_mounted,

                        kernel_started
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


    # def _detect_boot_stage(
    #     self,
    #     message: str
    # ) -> str:
    #     """
    #     Identify the boot stage from a log message.
    #     """

    #     message = message.lower()

    #     if any(
    #         keyword in message
    #         for keyword in [
    #             "u-boot",
    #             "starting kernel",
    #             "bootloader",
    #             "booting from"
    #         ]
    #     ):
    #         return "UBOOT"

    #     if any(
    #         keyword in message
    #         for keyword in [
    #             "linux version",
    #             "booting linux",
    #             "kernel",
    #             "cpu",
    #             "memory",
    #             "mmc",
    #             "usb",
    #             "gpio",
    #             "serial"
    #         ]
    #     ):
    #         return "KERNEL"

    #     if any(
    #         keyword in message
    #         for keyword in [
    #             "run /init",
    #             "init:",
    #             "systemd",
    #             "starting",
    #             "reached target"
    #         ]
    #     ):
    #         return "INIT"

    #     if any(
    #         keyword in message
    #         for keyword in [
    #             "login:",
    #             "raspberrypi login:",
    #             "ubuntu login:",
    #             "debian login:",
    #             "welcome",
    #             "last login"
    #         ]
    #     ):
    #         return "LOGIN"

    #     return "OTHER"