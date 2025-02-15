import os
from dotenv import load_dotenv

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()

# set values from .venv, language_key and language_endpoint
language_key = os.getenv("LANGUAGE_KEY")
language_endpoint = os.getenv("LANGUAGE_ENDPOINT")

client_subscription = TextAnalyticsClient(
    language_endpoint, AzureKeyCredential(language_key)
)


# create function to recognize pii entities
def recognize_pii_entities_from_list(client, documents):
    result = client.recognize_pii_entities(documents, language="es")
    result = [doc for doc in result if not doc.is_error]

    for doc in result:
        print("Redacted Text: {}".format(doc.redacted_text))
        for entity in doc.entities:
            print("Entity: {}".format(entity.text))
            print("Category: {}".format(entity.category))
            print("Confidence Score: {}".format(entity.confidence_score))
            print("Offset: {}".format(entity.offset))
            print("Length: {}".format(entity.length))
            print("")


# create function to recognize pii entities from a file txt
def recognize_pii_entities_from_file(client, file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        documents = file.readlines()
    documents = [doc.strip() for doc in documents]
    recognize_pii_entities_from_list(client, documents)


documents_sample = [
    "Mi número de teléfono es 555-555-5555",
    "Mi dirección de correo electrónico es alvaro@cc.com",
    "Mi número de seguro social es 3 9 6 1 2 0 4 6 5 8",
    "Mi dirección es 123 Calle Falsa, Springfield, USA",
    "Mi nombre es Alvaro y tengo 25 años",
]

# recognize_pii_entities_from_list(client_subscription, documents_sample)

recognize_pii_entities_from_file(client_subscription, "biography.txt")
