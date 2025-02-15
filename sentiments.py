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

def get_sentiments_from_documents(client, documents):
    try:
        result = client.analyze_sentiment(documents, show_opinion_mining=True)
        docs = [doc for doc in result if not doc.is_error]
        
        for idx, doc in enumerate(docs):
            print(f"Text: {documents[idx]}")
            print(f"Global sentiment: {doc.sentiment}")
        
    except HttpResponseError as err:
        print("Encountered HTTP response error. {}".format(err))
    except Exception as err:
        print("Encountered exception. {}".format(err))   
        
documents_sample = ["Tuve el mejor día de mi vida. Decidó hacer paracaidisimo y me hizo apreciar toda mi vida.",
                    "Esto fue una perdida de tiempo. Todas las vistas de este descenso son extremadamente aburridas",
                    "Solo tengo una palabra para mi experiecnia ¡WOW!"]

get_sentiments_from_documents(client_subscription, documents_sample)