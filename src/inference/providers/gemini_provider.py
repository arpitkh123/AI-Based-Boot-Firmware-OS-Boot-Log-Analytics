# import google.generativeai as genai
from google import genai

from src.inference.llm_interface import (
    LLMProvider
)

from src.config.settings import (
    Settings
)


class GeminiProvider(
    LLMProvider
):
    """
    Gemini implementation of the
    LLMProvider interface.
    """

    def __init__(
        self,
        # api_key: str,
        # model_name: str
    ):
        """
        Initialize the Gemini client.
        """

        # self.api_key = api_key

        # self.model_name = model_name

        # genai.configure(

        #     api_key=self.api_key

        # )

        # self.model = genai.GenerativeModel(

        #     self.model_name

        # )



        if not Settings.GEMINI_API_KEY:

            raise ValueError(

                "GEMINI_API_KEY not found in environment."

            )


        # genai.configure(

        #     api_key=Settings.GEMINI_API_KEY

        # )

        # self.model = genai.GenerativeModel(

        #     Settings.MODEL_NAME

        # )

        self.client = genai.Client(

            api_key=Settings.GEMINI_API_KEY

        )



    def generate(
        self,
        prompt: str
    ) -> str:
        """
        Generate an explanation
        using Gemini.
        """

        try:

            # response = self.model.generate_content(

            #     prompt

            # )

            # # return response.text.strip()
            # if not response.text:

            #     raise RuntimeError(

            #         "Gemini returned an empty response."

            #     )

            # return response.text.strip()


            response = self.client.models.generate_content(

                model=Settings.MODEL_NAME,

                contents=prompt

            )

            if not response.text:

                raise RuntimeError(

                    "Gemini returned an empty response."

                )

            return response.text.strip()

        except Exception as error:

            raise RuntimeError(

                f"Gemini generation failed: {error}"

            ) from error