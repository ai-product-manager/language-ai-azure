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


# create function to recognize linked entities
def recognize_linked_entities_from_list(client, documents):
    try:
        result = client.recognize_linked_entities(documents, language="es")[0]

        print("Linked Entities:")
        for entity in result.entities:
            print("\tName:", entity.name)
            print("\tURL:", entity.url)
            print("\tData Source:", entity.data_source)
            print("\tDataSource Entity Id:", entity.data_source_entity_id)
            print("\tMatches:")
            for match in entity.matches:
                print("\t\t", "Text:", match.text)
                print("\t\t", "Confidence Score:", match.confidence_score)
                print("\t\t", "\tOffset:", match.offset)
                print("\t\t", "\tLength:", match.length)
    except HttpResponseError as err:
        print("Encountered HTTP response error. {}".format(err))
    except Exception as err:  # pylint: disable=broad-exception-caught
        print("Encountered exception. {}".format(err))


documents_sample = [
    "Microsoft fue fundado por Bill Gates y Paul Allen en 1975. La sede de Microsoft se encuentra en Redmond, Washington. En 1975, Bill Gates y Paul Allen fundaron Microsoft en Redmond, Washington. La empresa se trasladó a Seattle, Washington y a Silicon Valley, California."
]

recognize_linked_entities_from_list(client_subscription, documents_sample)
