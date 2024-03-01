# This function an HTTP starter function for Durable Functions.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable activity function (default name is "Hello")
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt
 
import logging
import os



from azure.functions import HttpRequest, HttpResponse
from azure.durable_functions import DurableOrchestrationClient
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, ContainerSasPermissions, generate_container_sas

from shared_code import createContainerFile

blob_service_client = BlobServiceClient.from_connection_string(os.getenv("STORAGE_CONNECTION_STRING"))


async def main(req: HttpRequest, starter: str) -> HttpResponse:
    logging.warning('starting starter')

    if 'document' in req.files:
        file = req.files['document']
        file_name = file.filename
        file_content = file.read()

        # create conatiner and upload file to the container
        source_container_sas = createContainerFile(blob_service_client,file_name, file_content)

        client = DurableOrchestrationClient(starter)
        logging.warning('calling orch')
        instance_id = await client.start_new(req.route_params["functionName"], None, source_container_sas)

        logging.info(f"Started orchestration with ID = '{instance_id}'.")

        #  waits for response from orchestrator
        return await client.wait_for_completion_or_create_check_status_response(request=req, instance_id=instance_id, timeout_in_milliseconds=30000)
    else:
        logging.error('no file')

    # return client.create_check_status_response(req, instance_id)
        

