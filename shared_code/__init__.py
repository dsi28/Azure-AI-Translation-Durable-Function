import hashlib
import uuid
from datetime import datetime, timedelta

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, ContainerSasPermissions, generate_container_sas



def hash_uuid(length=10):
    my_uuid = str(uuid.uuid4())
    hashed = hashlib.sha256(my_uuid.encode()).hexdigest()
    hashed_id = hashed[:length]
    return hashed_id


def createContainerFile(blob_service_client, input_file_name, input_file_content):
    container_name = hash_uuid()
    container_client = blob_service_client.create_container(container_name)
    sas_url = createContainerSas(blob_service_client, container_name, container_client)
    if input_file_name is not None and input_file_content is not None:
        blob_name = input_file_name
        blob_content = input_file_content
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(blob_content)

    return sas_url


def createContainerSas( blob_service_client,container_name, container_client):
    # Define the permissions for the SAS
    permissions = ContainerSasPermissions(read=True, write=True, delete=True, list=True)

    # Define the start and expiry time for the SAS
    start_time = datetime.utcnow() - timedelta(hours=1)
    expiry_time = datetime.utcnow() + timedelta(days=1) 

    # Generate the SAS token for the container
    sas_token = generate_container_sas(
        blob_service_client.account_name,
        container_name,
        account_key=blob_service_client.credential.account_key,
        permission=permissions,
        start=start_time,
        expiry=expiry_time
    )
    sas_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}?{sas_token}"

    return sas_url