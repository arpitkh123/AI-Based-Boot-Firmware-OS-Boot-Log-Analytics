# src/parsers/uart_parser.py

import re
import logging
from pathlib import Path
from typing import Dict, List, Optional


# -----------------------------------------------------------------------------
# Logging Configuration
# -----------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# UART Parser
# -----------------------------------------------------------------------------

class UARTParser:
    """
    Parses Raspberry Pi UART boot logs.

    Example Input:
    [    1.615709] serial serial0: tty port ttyAMA1 registered

    Example Output:
    {
        "line_number": 120,
        "timestamp": 1.615709,
        "message": "serial serial0: tty port ttyAMA1 registered"
    }
    """

    LOG_PATTERN = re.compile(
        # r"^\[\s*(?P<timestamp>\d+\.\d+)\]\s*(?P<message>.*)$"
        # r"^\[\s*(?P<timestamp>\d+(?:\.\d+)?)\]\s*(?P<message>.*)$"
        r"\[\s*(?P<timestamp>\d+(?:\.\d+)?)\s*\]\s*(?P<message>.*)"
    )

    SHELL_PREFIXES = (

        "~ #",

        "# ",

        "$ ",

        "root@",

        "ubuntu@",

        "pi@"
    )

    def parse_line(
        self,
        line: str,
        line_number: int
    ) -> Optional[Dict]:
        """
        Parse a single UART log line.

        Supports:
        1. Linux Kernel log lines with timestamps.
        2. U-Boot / Bootloader messages.
        3. Login shell / User-space messages.
        """

        try:

            line = line.strip()

            if not line:
                return None

            if line.startswith(self.SHELL_PREFIXES):

                return None
            
            
            # Ignore separator lines
            if all(
                character in "-=*_#."
                for character in line
            ):
                return None

            # ---------------------------------------------------------
            # Case 1 : Linux Kernel Log
            # ---------------------------------------------------------

            # match = self.LOG_PATTERN.match(line)
            match = self.LOG_PATTERN.search(line)

            if match:

                message = match.group("message").strip()

                return {

                    "line_number": line_number,

                    "timestamp": float(
                        match.group("timestamp")
                    ),

                    # "stage": self._detect_boot_stage(
                    #     message
                    # ),
                    "raw_line": line,

                    "message": message
                }

            # ---------------------------------------------------------
            # Case 2 : U-Boot / Raw UART Log
            # ---------------------------------------------------------

            return {

                "line_number": line_number,

                "timestamp": None,

                # "stage": self._detect_boot_stage(
                #     line
                # ),
                "raw_line": line,

                "message": line
            }

        except ValueError as error:

            logger.error(
                f"Line {line_number}: "
                f"Timestamp conversion failed. {error}"
                f"Raw Line: {line}"
            )

            return None

        except Exception as error:

            logger.exception(
                f"Line {line_number}: "
                f"Unexpected parsing error. {error}"
            )

            return None

    # def parse_line(
    #     self,
    #     line: str,
    #     line_number: int
    # ) -> Optional[Dict]:
    #     """
    #     Parse a single UART log line.
    #     """

    #     try:
    #         line = line.strip()

    #         if not line:
    #             return None

    #         match = self.LOG_PATTERN.match(line)

    #         if not match:
    #             logger.debug(
    #                 f"Line {line_number}: Invalid log format skipped."
    #             )
    #             return None

    #         return {
    #             "line_number": line_number,
    #             "timestamp": float(match.group("timestamp")),
    #             "message": match.group("message").strip()
    #         }

    #     except ValueError as e:
    #         logger.error(
    #             f"Line {line_number}: Timestamp conversion failed. {e}"
    #         )
    #         return None

    #     except Exception as e:
    #         logger.exception(
    #             f"Line {line_number}: Unexpected parsing error. {e}"
    #         )
    #         return None

    def parse_file(self, file_path: str) -> List[Dict]:
        """
        Parse an entire UART log file.
        """

        parsed_logs = []

        try:

            file_path = Path(file_path)

            if not file_path.exists():
                raise FileNotFoundError(
                    f"File not found: {file_path}"
                )

            if not file_path.is_file():
                raise ValueError(
                    f"Provided path is not a file: {file_path}"
                )

            logger.info(
                f"Started parsing file: {file_path.name}"
            )

            with open(
                file_path,
                mode="r",
                encoding="utf-8",
                errors="replace"
            ) as file:

                for line_number, line in enumerate(file, start=1):

                    parsed_line = self.parse_line(
                        line=line,
                        line_number=line_number
                    )

                    if parsed_line:
                        parsed_logs.append(parsed_line)



# --- GUARDRAIL: Valid Log File Sanity Check ---
            
            if parsed_logs:
                valid_timestamp_count = sum(
                    1 for log in parsed_logs if log.get("timestamp") is not None
                )
                
                valid_ratio = valid_timestamp_count / len(parsed_logs)
                
                # Fallback: If timestamps fail, check the first 50 lines for obvious boot keywords
                is_raw_bootloader = any(
                    keyword in log.get("message", "").lower()
                    for log in parsed_logs[:50]
                    for keyword in ["booting linux", "u-boot", "linux version", "starting kernel"]
                )
                
                # If less than 5% timestamps AND no boot keywords are found, then it's garbage text.
                if valid_ratio < 0.05 and not is_raw_bootloader:
                    raise ValueError(
                        f"Invalid log file detected: {file_path.name}. "
                        f"Only {valid_ratio * 100:.1f}% valid timestamps and no boot keywords found. "
                        f"This does not appear to be a genuine boot log."
                    )


        # # --- GUARDRAIL: Valid Log File Sanity Check ---
                    
        #             if parsed_logs:
        #                 # Count how many lines actually have a valid timestamp
        #                 valid_timestamp_count = sum(
        #                     1 for log in parsed_logs if log.get("timestamp") is not None
        #                 )
                        
        #                 # Calculate the percentage of valid kernel logs
        #                 valid_ratio = valid_timestamp_count / len(parsed_logs)
                        
        #                 # If less than 10% of the file looks like a real log, reject it
        #                 if valid_ratio < 0.10:
        #                     raise ValueError(
        #                         f"Invalid log file detected: {file_path.name}. "
        #                         f"Only {valid_ratio * 100:.1f}% of lines have valid timestamps. "
        #                         f"This does not appear to be a genuine boot log."
        #                     )



            logger.info(
                f"Successfully parsed "
                f"{len(parsed_logs)} log entries "
                f"from {file_path.name}"
            )

            return parsed_logs

        except FileNotFoundError as e:
            logger.error(e)
            raise

        except PermissionError as e:
            logger.error(
                f"Permission denied while reading file. {e}"
            )
            raise

        except UnicodeDecodeError as e:
            logger.error(
                f"Encoding issue while reading file. {e}"
            )
            raise

        except Exception as e:
            logger.exception(
                f"Unexpected error while parsing file. {e}"
            )
            raise

    def parse_files(self, file_paths):
        """
        Parse multiple log files.
        """

        parsed_results = {}

        for file_path in file_paths:

            try:

                parsed_results[str(file_path)] = (
                    self.parse_file(file_path)
                )

            except Exception as error:

                logger.error(
                    f"Failed to parse {file_path}. "
                    f"Reason: {error}"
                )

        return parsed_results

    def get_basic_statistics(
        self,
        parsed_logs: List[Dict]
    ) -> Dict:
        """
        Generate basic statistics from parsed logs.
        """

        try:

            if not parsed_logs:
                return {
                    "total_lines": 0,
                    "start_timestamp": None,
                    "end_timestamp": None,
                    "boot_duration": 0
                }

            # start_time = parsed_logs[0]["timestamp"]
            # end_time = parsed_logs[-1]["timestamp"]

            # timestamps = [

            #     log["timestamp"]

            #     for log in parsed_logs

            #     if log["timestamp"] is not None
            # ]

            # return {
            #     "total_lines": len(parsed_logs),
            #     "start_timestamp": start_time,
            #     "end_timestamp": end_time,
            #     "boot_duration": round(
            #         end_time - start_time,
            #         6
            #     )
            # }


            timestamps = [

                log["timestamp"]

                for log in parsed_logs

                if log["timestamp"] is not None
            ]

            if not timestamps:

                return {

                    "total_lines": len(parsed_logs),

                    "start_timestamp": None,

                    "end_timestamp": None,

                    "boot_duration": None
                }

            start_time = timestamps[0]

            end_time = timestamps[-1]

            return {

                "total_lines": len(parsed_logs),

                "start_timestamp": start_time,

                "end_timestamp": end_time,

                "boot_duration": round(
                    end_time - start_time,
                    6
                )
            }

        except Exception as e:
            logger.exception(
                f"Failed to generate statistics. {e}"
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
        
