import os
import azure.storage.blob

URL = os.environ['CONTAINER_URL']

container = azure.storage.blob.ContainerClient.from_container_url(URL)

for blob in container.list_blobs():
    if blob.name.endswith(".LAS"):
        print(f'{blob.size:<20}{blob.name}')
