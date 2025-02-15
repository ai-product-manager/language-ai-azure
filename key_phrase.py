import os
from dotenv import load_dotenv

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError

load_dotenv()

# set values from .venv, language_key and language_endpoint
language_key = os.getenv("LANGUAGE_KEY")
language_endpoint = os.getenv("LANGUAGE_ENDPOINT")

client_subscription = TextAnalyticsClient(
    language_endpoint, AzureKeyCredential(language_key)
)


# create a function to get key phrases from a list using try and except
def get_key_phrases_from_list(client, documents):
    try:
        result = client.extract_key_phrases(documents=documents)[0]
        print("Key Phrases:")
        for phrase in result.key_phrases:
            print("\t", phrase)
    except HttpResponseError as err:
        print("Encountered HTTP response error. {}".format(err))
    except Exception as err:  # pylint: disable=broad-exception-caught
        print("Encountered exception. {}".format(err))


# create a function to get key phrases from a file txt
def get_key_phrases_from_file(client, file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        documents = file.readlines()
    documents = [doc.strip() for doc in documents]
    get_key_phrases_from_list(client, documents)


# documents_sample = ["Las oficinas de Microsoft están en Redmond, Washington donde se creó la empresa, además de en Seattle, Washington y en Silicon Valley, California."]

get_key_phrases_from_file(client_subscription, "biography.txt")
