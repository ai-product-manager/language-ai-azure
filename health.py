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


# create function to recognize health entities
def recognize_health_entities_from_list(client, documents):
    try:
        result = client.begin_analyze_healthcare_entities(
            documents, show_stats=True
        ).result()

        docs = [doc for doc in result if not doc.is_error]
        for idx, doc in enumerate(docs):
            print("Document #{} has the following healthcare entities:".format(idx))
            for entity in doc.entities:
                print("Entity: {}".format(entity.text))
                print("\tNormalized Text: {}".format(entity.normalized_text))
                print("\tCategory: {}".format(entity.category))
                print("\tSubcategory: {}".format(entity.subcategory))
                print("\tConfidence Score: {}".format(entity.confidence_score))
                print("\tOffset: {}".format(entity.offset))
                print("\tLength: {}".format(entity.length))
            for relation in doc.entity_relations:
                print("Relation:")
                print("\tRelation Type: {}".format(relation.relation_type))
                for role in relation.roles:
                    print(
                        "\tRole: {} with entity {}".format(role.name, role.entity.text)
                    )
    except HttpResponseError as err:
        print("Encountered HTTP response error. {}".format(err))
    except Exception as err:  # pylint: disable=broad-exception-caught
        print("Encountered exception. {}".format(err))


documents_sample = [
    "Paciente necesita ibuprofeno de 50mg para el dolor de cabeza",
    "Mujer embarazada con presión 170 sobre 100, administrado metildopa 500 cada 4 horas",
]

recognize_health_entities_from_list(client_subscription, documents_sample)
