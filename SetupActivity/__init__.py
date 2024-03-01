# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import os

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, ContainerSasPermissions, generate_container_sas
from shared_code import createContainerFile

blob_service_client = BlobServiceClient.from_connection_string(os.getenv("AzureWebJobsStorage"))


#  create destination container in blob storage
#  return sas blob sas urls for both newly created containers
def main(sourceSas) -> str:
    
    destination_sas = createContainerFile(blob_service_client, None, None)

    return destination_sas
