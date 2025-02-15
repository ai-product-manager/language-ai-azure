import os
from dotenv import load_dotenv

from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.translation.text.models import InputTextItem

load_dotenv()

# set values from .venv, language_key and language_endpoint
translation_key = os.getenv("TRANSLATION_KEY")
translation_endpoint = os.getenv("TRANSLATION_ENDPOINT")

client_subscription = TextTranslationClient(
    credential=AzureKeyCredential(translation_key), region="eastus"
)


def translate_from_to(client: TextTranslationClient, source, to, documents):
    try:
        response = client.translate(
            body=documents, to_language=to, from_language=source
        )
        translate = response[0] if response else None
        print(translate)
    except HttpResponseError as err:
        print("Encountered HTTP response error. {}".format(err))
    except Exception as err:  # pylint: disable=broad-exception-caught
        print("Encountered exception. {}".format(err))


translate_from_to(client_subscription, "en", ["es", "fr"], ["This is a text"])
