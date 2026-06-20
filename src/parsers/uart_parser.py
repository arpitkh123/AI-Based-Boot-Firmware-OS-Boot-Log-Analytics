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
        r"^\[\s*(?P<timestamp>\d+\.\d+)\]\s*(?P<message>.*)$"
    )

    def parse_line(
        self,
        line: str,
        line_number: int
    ) -> Optional[Dict]:
        """
        Parse a single UART log line.
        """

        try:
            line = line.strip()

            if not line:
                return None

            match = self.LOG_PATTERN.match(line)

            if not match:
                logger.debug(
                    f"Line {line_number}: Invalid log format skipped."
                )
                return None

            return {
                "line_number": line_number,
                "timestamp": float(match.group("timestamp")),
                "message": match.group("message").strip()
            }

        except ValueError as e:
            logger.error(
                f"Line {line_number}: Timestamp conversion failed. {e}"
            )
            return None

        except Exception as e:
            logger.exception(
                f"Line {line_number}: Unexpected parsing error. {e}"
            )
            return None

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

            start_time = parsed_logs[0]["timestamp"]
            end_time = parsed_logs[-1]["timestamp"]

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