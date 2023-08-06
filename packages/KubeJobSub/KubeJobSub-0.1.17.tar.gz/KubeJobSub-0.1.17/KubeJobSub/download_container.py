import os
from azure.storage.blob import BlockBlobService


def download_container(blob_service, container_name, output_dir):
    # Modified from https://blogs.msdn.microsoft.com/brijrajsingh/2017/05/27/downloading-a-azure-blob-storage-container-python/
    generator = blob_service.list_blobs(container_name)
    for blob in generator:
        # check if the path contains a folder structure, create the folder structure
        if "/" in blob.name:
            # extract the folder path and check if that folder exists locally, and if not create it
            head, tail = os.path.split(blob.name)
            if os.path.isdir(os.path.join(output_dir, head)):
                # download the files to this directory
                blob_service.get_blob_to_path(container_name, blob.name, os.path.join(output_dir, head, tail))
            else:
                # create the diretcory and download the file to it
                os.makedirs(os.path.join(output_dir, head))
                blob_service.get_blob_to_path(container_name, blob.name, os.path.join(output_dir, head, tail))
        else:
            blob_service.get_blob_to_path(container_name, blob.name, blob.name)


if __name__ == '__main__':
    blob_service = BlockBlobService(account_key='hdN6oocT4clbBK9KmC4oMSsY47isrqSTm1eJlVJ6rR5uWpk4arZSKtfG/eMXt3izGBRCXnaCsCJ5nil7b6kijg==',
                                    account_name='carlingst01')
    download_container(blob_service=blob_service,
                       container_name='180828-m05722-output',
                       output_dir='.')
