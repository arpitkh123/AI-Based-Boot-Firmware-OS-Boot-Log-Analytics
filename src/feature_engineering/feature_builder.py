import logging
from typing import Dict, List, Optional


logger = logging.getLogger(__name__)


class FeatureBuilder:

    def build_features(
        self,
        classified_logs: List[Dict],
        boot_analysis: Dict,
        templates: List[Dict],
        label: Optional[str] = None
    ) -> Dict:

        try:

            feature_vector = {}

            feature_vector.update(
                self._extract_boot_features(
                    boot_analysis
                )
            )

            feature_vector.update(
                self._extract_severity_features(
                    classified_logs
                )
            )

            feature_vector.update(
                self._extract_subsystem_features(
                    classified_logs
                )
            )

            feature_vector.update(
                self._extract_template_features(
                    templates
                )
            )

            feature_vector.update(
                self._extract_failure_features(
                    boot_analysis
                )
            )

            if label is not None:

                feature_vector["label"] = label

            logger.info(
                "Successfully built feature vector."
            )

            return feature_vector

        except Exception as error:

            logger.exception(
                f"Feature generation failed. "
                f"Reason: {error}"
            )

            raise


    def _extract_boot_features(
        self,
        boot_analysis: Dict
    ) -> Dict:

        return {

            "boot_duration":
                boot_analysis.get(
                    "boot_duration",
                    0.0
                ),

            "boot_successful":
                int(
                    boot_analysis.get(
                        "boot_successful",
                        False
                    )
                ),

            "kernel_started":
                int(
                    boot_analysis.get(
                        "kernel_started",
                        False
                    )
                ),

            "rootfs_mounted":
                int(
                    boot_analysis.get(
                        "rootfs_mounted",
                        False
                    )
                ),

            "init_started":
                int(
                    boot_analysis.get(
                        "init_started",
                        False
                    )
                ),

            "login_prompt_detected":
                int(
                    boot_analysis.get(
                        "login_prompt_detected",
                        False
                    )
                ),

            "kernel_panic_detected":
                int(
                    boot_analysis.get(
                        "kernel_panic_detected",
                        False
                    )
                ),

            "error_count":
                boot_analysis.get(
                    "error_count",
                    0
                ),

            "warning_count":
                boot_analysis.get(
                    "warning_count",
                    0
                )
        }
    

    def _extract_failure_features(
        self,
        boot_analysis: Dict
    ) -> Dict:

        return {

            "irq_failure":

                int(
                    boot_analysis.get(
                        "irq_failure",
                        False
                    )
                ),

            "dma_failure":

                int(
                    boot_analysis.get(
                        "dma_failure",
                        False
                    )
                ),

            "rootfs_failure":

                int(
                    boot_analysis.get(
                        "rootfs_failure",
                        False
                    )
                ),

            "dtb_failure":

                int(
                    boot_analysis.get(
                        "dtb_failure",
                        False
                    )
                ),

            "oom_detected":

                int(
                    boot_analysis.get(
                        "oom_detected",
                        False
                    )
                ),

            "init_failure":

                int(
                    boot_analysis.get(
                        "init_failure",
                        False
                    )
                ),

            "cpu_failure":

                int(
                    boot_analysis.get(
                        "cpu_failure",
                        False
                    )
                ),

            "filesystem_failure":

                int(
                    boot_analysis.get(
                        "filesystem_failure",
                        False
                    )
                )
        }


    def _extract_severity_features(
        self,
        classified_logs: List[Dict]
    ) -> Dict:

        severities = {

            "INFO": 0,
            "WARNING": 0,
            "ERROR": 0,
            "SUCCESS": 0
        }

        for log in classified_logs:

            severity = log.get(
                "severity"
            )

            if severity in severities:

                severities[
                    severity
                ] += 1

        return {

            "info_logs":
                severities["INFO"],

            "warning_logs":
                severities["WARNING"],

            "error_logs":
                severities["ERROR"],

            "success_logs":
                severities["SUCCESS"]
        }


    def _extract_subsystem_features(
        self,
        classified_logs: List[Dict]
    ) -> Dict:

        subsystem_counts = {}

        for log in classified_logs:

            subsystem = log.get(
                "subsystem",
                "UNKNOWN"
            )

            subsystem_counts[
                subsystem
            ] = subsystem_counts.get(
                subsystem,
                0
            ) + 1

        return {

            "boot_logs":
                subsystem_counts.get(
                    "BOOT",
                    0
                ),

            "kernel_logs":
                subsystem_counts.get(
                    "KERNEL",
                    0
                ),

            "memory_logs":
                subsystem_counts.get(
                    "MEMORY",
                    0
                ),

            "filesystem_logs":
                subsystem_counts.get(
                    "FILESYSTEM",
                    0
                ),

            "network_logs":
                subsystem_counts.get(
                    "NETWORK",
                    0
                ),

            "uart_logs":
                subsystem_counts.get(
                    "UART",
                    0
                ),

            "usb_logs":
                subsystem_counts.get(
                    "USB",
                    0
                ),

            "unknown_logs":
                subsystem_counts.get(
                    "UNKNOWN",
                    0
                )
        }
    



    def _extract_template_features(
        self,
        templates: List[Dict]
    ) -> Dict:

        if not templates:

            return {

                "template_count": 0,

                "total_log_messages": 0,

                "unique_templates": 0,

                "largest_template_frequency": 0,

                "repeated_templates": 0,

                "compression_ratio": 0.0,

                "template_info": 0,

                "template_warning": 0,

                "template_error": 0,

                "template_usb": 0,

                "template_kernel": 0,

                "template_memory": 0
            }

        total_messages = sum(
            template["count"]
            for template in templates
        )

        largest_cluster = max(
            template["count"]
            for template in templates
        )

        repeated_templates = sum(
            1
            for template in templates
            if template["count"] > 1
        )

        compression_ratio = (
            len(templates) / total_messages
            if total_messages > 0
            else 0
        )

        severity_distribution = {

            "INFO": 0,

            "WARNING": 0,

            "ERROR": 0,

            "SUCCESS": 0
        }

        subsystem_distribution = {}

        for template in templates:

            for severity, count in template.get(
                "severity_counts",
                {}
            ).items():

                severity_distribution[
                    severity
                ] += count


            for subsystem, count in template.get(
                "subsystem_counts",
                {}
            ).items():

                subsystem_distribution[
                    subsystem
                ] = (

                    subsystem_distribution.get(
                        subsystem,
                        0
                    )

                    + count
                )        

        # severity_distribution = {}

        # subsystem_distribution = {}

        # for template in templates:

        #     severity = template.get(
        #         "severity",
        #         "UNKNOWN"
        #     )

        #     subsystem = template.get(
        #         "subsystem",
        #         "UNKNOWN"
        #     )

        #     severity_distribution[severity] = (
        #         severity_distribution.get(
        #             severity,
        #             0
        #         ) + 1
        #     )

        #     subsystem_distribution[subsystem] = (
        #         subsystem_distribution.get(
        #             subsystem,
        #             0
        #         ) + 1
        #     )

        return {

            "template_count":
                total_messages,

            # "total_log_messages":
            #     total_messages,

            "unique_templates":
                len(templates),

            "largest_template_frequency":
                largest_cluster,

            "repeated_templates":
                repeated_templates,

            "compression_ratio":
                round(
                    compression_ratio,
                    4
                ),

            "template_info":
                severity_distribution.get(
                    "INFO",
                    0
                ),

            "template_warning":
                severity_distribution.get(
                    "WARNING",
                    0
                ),

            "template_error":
                severity_distribution.get(
                    "ERROR",
                    0
                ),

            "template_success":
                severity_distribution.get(
                    "SUCCESS",
                    0
                ),    

            "template_usb":
                subsystem_distribution.get(
                    "USB",
                    0
                ),

            "template_kernel":
                subsystem_distribution.get(
                    "KERNEL",
                    0
                ),

            "template_memory":
                subsystem_distribution.get(
                    "MEMORY",
                    0
                ),

            "template_network":
                subsystem_distribution.get(
                    "NETWORK",
                    0
                ),

            "template_uart":
                subsystem_distribution.get(
                    "UART",
                    0
                ),

            "template_filesystem":
                subsystem_distribution.get(
                    "FILESYSTEM",
                    0
                ),

            "template_boot":
                subsystem_distribution.get(
                    "BOOT",
                    0
                ),

            "template_unknown":
                subsystem_distribution.get(
                    "UNKNOWN",
                    0
                )   
        }
    

        
    # def _extract_template_features(
    #     self,
    #     templates: List[Dict]
    # ) -> Dict:

    #     if not templates:

    #         return {
    #             "template_count": 0,
    #             "total_log_messages": 0,
    #             "unique_templates": 0,
    #             "largest_template_frequency": 0,
    #             "repeated_templates": 0,
    #             "compression_ratio": 0.0
    #         }

    #     total_messages = sum(
    #         template["count"]
    #         for template in templates
    #     )

    #     largest_cluster = max(
    #         template["count"]
    #         for template in templates
    #     )

    #     repeated_templates = sum(
    #         1
    #         for template in templates
    #         if template["count"] > 1
    #     )

    #     compression_ratio = (
    #         len(templates) / total_messages
    #         if total_messages > 0
    #         else 0
    #     )

    #     return {

    #         "template_count": total_messages,

    #         "total_log_messages": total_messages,

    #         "unique_templates": len(templates),

    #         "largest_template_frequency": largest_cluster,

    #         "repeated_templates": repeated_templates,

    #         "compression_ratio": round(
    #             compression_ratio,
    #             4
    #         )
    #     }
    



# def _extract_template_features(
#     self,
#     templates: List[Dict]
# ) -> Dict:

#         if not templates:

#             return {

#                 "template_count": 0,
#                 "unique_templates": 0,
#                 "largest_template_frequency": 0,
#                 "repeated_templates": 0
#             }

#         largest_cluster = max(

#             template["count"]

#             for template in templates
#         )

#         repeated_templates = sum(

#             1

#             for template in templates

#             if template["count"] > 1
#         )

#         # # "template_count":
#         # total_messages = sum(

#         #     template["count"]

#         #     for template in templates
#         # )
    

#         # compression_ratio = (

#         #     len(templates) / total_messages

#         #     if total_messages > 0

#         #     else 0
#         # )

#     return {

#             # # "template_count":
#             total_messages = sum(

#                 template["count"]

#                 for template in templates
#             )
        

#             compression_ratio = (

#                 len(templates) / total_messages

#                 if total_messages > 0

#                 else 0
#             )

#             "total_log_messages":
#                 total_messages,

#             "unique_templates":
#                 len(
#                     templates
#                 ),

#             "largest_template_frequency":
#                 largest_cluster,

#             "repeated_templates":
#                 repeated_templates

#             "compression_ratio":
#                 round(
#                     compression_ratio,
#                     4
#                 )    
#         }


# def _extract_template_features(
#     self,
#     templates: List[Dict]
# ) -> Dict:

#     if not templates:

#         return {
#             "template_count": 0,
#             "total_log_messages": 0,
#             "unique_templates": 0,
#             "largest_template_frequency": 0,
#             "repeated_templates": 0,
#             "compression_ratio": 0.0
#         }

#     total_messages = sum(
#         template["count"]
#         for template in templates
#     )

#     largest_cluster = max(
#         template["count"]
#         for template in templates
#     )

#     repeated_templates = sum(
#         1
#         for template in templates
#         if template["count"] > 1
#     )

#     compression_ratio = (
#         len(templates) / total_messages
#         if total_messages > 0
#         else 0
#     )

#     return {

#         "template_count": total_messages,

#         "total_log_messages": total_messages,

#         "unique_templates": len(templates),

#         "largest_template_frequency": largest_cluster,

#         "repeated_templates": repeated_templates,

#         "compression_ratio": round(
#             compression_ratio,
#             4
#         )
#     }