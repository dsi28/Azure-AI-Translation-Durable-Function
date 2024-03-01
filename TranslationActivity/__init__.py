# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import os

#  import libraries
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.document import DocumentTranslationClient


def main(sasList) -> str:

    # initialize a new instance of the DocumentTranslationClient object to interact with the Document Translation feature
    client = DocumentTranslationClient(os.getenv("TRANSLATION_ENDPOINT"), AzureKeyCredential(os.getenv("TRANSLATION_KEY")))
    poller = client.begin_translation(sasList[0], sasList[1], "es")
    result = poller.result()

    logging.warning("Status: {}".format(poller.status()))
    logging.warning("Created on: {}".format(poller.details.created_on))
    logging.warning("Last updated on: {}".format(poller.details.last_updated_on))
    logging.warning(
        "Total number of translations on documents: {}".format(
            poller.details.documents_total_count
        )
    )

    logging.warning("\nOf total documents...")
    logging.warning("{} failed".format(poller.details.documents_failed_count))
    logging.warning("{} succeeded".format(poller.details.documents_succeeded_count))

    doc_location = "doc location"
    for document in result:
        logging.warning("Document ID: {}".format(document.id))
        logging.warning("Document status: {}".format(document.status))
        if document.status == "Succeeded":
            logging.warning("Source document location: {}".format(document.source_document_url))
            doc_location = "Translated document location: {}".format(document.translated_document_url)
            logging.warning(doc_location)
            logging.warning("Translated to language: {}\n".format(document.translated_to))
        else:
            logging.warning(
                "Error Code: {}, Message: {}\n".format(
                    document.error.code, document.error.message
                )
            )

    return doc_location
