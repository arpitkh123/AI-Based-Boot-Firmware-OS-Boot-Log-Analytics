import logging

from typing import Dict
from typing import List

from src.config.boot_events import (
    BOOT_EVENTS
)

from src.config.boot_event_patterns import (
    BOOT_EVENT_PATTERNS
)


logger = logging.getLogger(__name__)


class BootEventEngine:

    """
    Extract canonical boot events
    from classified boot logs.
    """

    def __init__(self):

        self.boot_events = BOOT_EVENTS

        self.boot_patterns = BOOT_EVENT_PATTERNS


    def extract_events(
        self,
        classified_logs: List[Dict]
    ) -> List[Dict]:
        """
        Extract canonical boot events while
        maintaining boot stage progression.
        """

        extracted_events = []

        detected_events = set()

        current_stage = None

        stage_order = [

            "UBOOT",

            "KERNEL",

            "FILESYSTEM",

            "INIT",

            "LOGIN"
        ]

        for log in classified_logs:

            message = (
                log.get(
                    "message",
                    ""
                ).lower()
            )

            timestamp = log.get(
                "timestamp"
            )

            for event_name, event_rule in self.boot_patterns.items():

                if event_name in detected_events:
                    continue

                patterns = event_rule["patterns"]

                if not any(

                    pattern.lower() in message

                    for pattern in patterns

                ):
                    continue

                event_stage = event_rule["stage"]

                previous_stage = event_rule["previous_stage"]

                # ------------------------------------------
                # Stage Validation
                # ------------------------------------------

                if previous_stage is not None:

                    if current_stage is None:

                        if previous_stage != "UBOOT":
                            continue

                    else:

                        current_index = (
                            stage_order.index(
                                current_stage
                            )
                        )

                        previous_index = (
                            stage_order.index(
                                previous_stage
                            )
                        )

                        # Prevent going backwards

                        if previous_index < current_index:
                            continue

                extracted_events.append(

                    {

                        "event":
                            event_name,

                        "stage":
                            event_stage,

                        "description":
                            self.boot_events[
                                event_name
                            ]["description"],

                        "timestamp":
                            timestamp,

                        "status":
                            "SUCCESS",

                        "log":
                            log
                    }
                )

                detected_events.add(
                    event_name
                )

                current_stage = event_stage

        logger.info(

            f"Extracted "

            f"{len(extracted_events)} "

            f"boot events."

        )

        return extracted_events






    # def extract_events(
    #     self,
    #     classified_logs: List[Dict]
    # ) -> List[Dict]:

    #     extracted_events = []

    #     detected_events = set()

    #     for log in classified_logs:

    #         message = (
    #             log.get(
    #                 "message",
    #                 ""
    #             ).lower()
    #         )

    #         timestamp = log.get(
    #             "timestamp"
    #         )

    #         for event_name, event_rule in self.boot_patterns.items():

    #             if event_name in detected_events:
    #                 continue

    #             patterns = event_rule["patterns"]

    #             if any(

    #                 pattern.lower() in message

    #                 for pattern in patterns

    #             ):

    #                 extracted_events.append(

    #                     {

    #                         "event":
    #                             event_name,

    #                         "stage":
    #                             self.boot_events[
    #                                 event_name
    #                             ]["stage"],

    #                         "description":
    #                             self.boot_events[
    #                                 event_name
    #                             ]["description"],

    #                         "timestamp":
    #                             timestamp,

    #                         "status":
    #                             "SUCCESS",

    #                         "log":
    #                             log
    #                     }
    #                 )

    #                 detected_events.add(
    #                     event_name
    #                 )

    #     logger.info(

    #         f"Extracted "

    #         f"{len(extracted_events)} "

    #         f"boot events."

    #     )

    #     return extracted_events