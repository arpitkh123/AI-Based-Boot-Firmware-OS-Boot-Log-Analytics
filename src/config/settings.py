import os

from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = (

    Path(__file__)

    .resolve()

    .parent

    .parent

    .parent

)

load_dotenv(

    PROJECT_ROOT / ".env"

)


class Settings:
    """
    Centralized application
    configuration.
    """

    GEMINI_API_KEY = os.getenv(

        "GEMINI_API_KEY"

    )

    LLM_PROVIDER = os.getenv(

        "LLM_PROVIDER",

        "gemini"

    )

    MODEL_NAME = os.getenv(

        "LLM_MODEL",

        "gemini-2.5-flash"

    )

    TEMPERATURE = float(

        os.getenv(

            "TEMPERATURE",

            0.2

        )

    )

    MAX_OUTPUT_TOKENS = int(

        os.getenv(

            "MAX_OUTPUT_TOKENS",

            2048

        )

    )