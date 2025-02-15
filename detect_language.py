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

def get_sentiments_from_documents(client: TextAnalyticsClient, documents):
    try:
        response = client.detect_language(documents, country_hint='cn')
        for idx, response in enumerate(response):
            print("Document: {} | Detected language: {}".format(documents[idx], response.primary_language.name))
    except HttpResponseError as err:
        print("Encountered HTTP response error. {}".format(err))
    except Exception as err:
        print("Encountered exception. {}".format(err)) 
        
documents_sample = ["这是法语和中文的文本",
                    "Ceci est un texte en français et en chinois"]

get_sentiments_from_documents(client_subscription,documents_sample)
