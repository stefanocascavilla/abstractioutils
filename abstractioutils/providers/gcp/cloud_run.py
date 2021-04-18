from datetime import datetime

from abstractioutils.providers.gcp.base import Base
from googleapiclient.discovery import build

from abstractioutils.exceptions.gcp.cloud_run_exception import CloudRunException


class CloudRun(Base):
    def __init__(self, service_account_info: str):
        super().__init__(service_account_info)

    def list_services(self, project_id: str, region: str) -> dict:
        print(f"{datetime.now()} - Listing Cloud Run services...")

        service = build('run', 'v1', credentials=self._get_credentials(), cache_discovery=False)
        try:
            service._baseUrl = f'https://{region}-run.googleapis.com'
            return service.namespaces().services().list(
                parent=f'namespaces/{project_id}'
            ).execute()
        except Exception as exc:
            print(f"{datetime.now()} - Error while listing Cloud Run clusters - {exc.__str__()}")
            raise CloudRunException(status_code=500, message='Error while listing Cloud Run clusters')

    def get_service(self, name: str, region: str) -> dict:
        print(f"{datetime.now()} - Getting Cloud Run service {name}...")

        service = build('run', 'v1', credentials=self._get_credentials(), cache_discovery=False)
        try:
            service._baseUrl = f'https://{region}-run.googleapis.com'
            return service.namespaces().services().get(
                name=name
            ).execute()
        except Exception as exc:
            print(f"{datetime.now()} - Error while getting Cloud Run cluster - {exc.__str__()}")
            raise CloudRunException(status_code=500, message=f'Error while getting Cloud Run cluster {name}')

    def create_cloud_run_service(self, project_id: str, region: str, body: dict) -> dict:
        print(f"{datetime.now()} - Creating the Cloud Run service...")

        service = build('run', 'v1', credentials=self._get_credentials(), cache_discovery=False)
        try:
            service._baseUrl = f'https://{region}-run.googleapis.com'
            return service.namespaces().services().create(
                parent=f'namespaces/{project_id}',
                body=body
            ).execute()
        except Exception as exc:
            print(f"{datetime.now()} - Error while creating Cloud Run service - {exc.__str__()}")
            raise CloudRunException(status_code=500, message='Error while creating Cloud Run service')

    def update_cloud_run_service(self, name: str, region: str, body: dict) -> dict:
        print(f"{datetime.now()} - Updating the Cloud Run service...")

        service = build('run', 'v1', credentials=self._get_credentials(), cache_discovery=False)
        try:
            service._baseUrl = f'https://{region}-run.googleapis.com'
            return service.namespaces().services().replaceService(
                name=name,
                body=body
            ).execute()
        except Exception as exc:
            print(f"{datetime.now()} - Error while updating Cloud Run service - {exc.__str__()}")
            raise CloudRunException(status_code=500, message='Error while updating Cloud Run service')

    def delete_cloud_run_service(self, service_name: str, region: str) -> dict:
        print(f"{datetime.now()} - Deleting the {service_name} cloud run service...")

        service = build('run', 'v1', credentials=self._get_credentials(), cache_discovery=False)
        try:
            service._baseUrl = f'https://{region}-run.googleapis.com'
            return service.namespaces().services().delete(
                name=service_name
            ).execute()
        except Exception as exc:
            print(f"{datetime.now()} - Error while deleting the service - {exc.__str__()}")
            raise CloudRunException(status_code=500, message='Error while deleting the service')

    def allow_unauthenticated_invokations(self, service_name: str) -> dict:
        print(f"{datetime.now()} - Allowing unauth calls for the {service_name} service...")

        service = build('run', 'v1', credentials=self._get_credentials(), cache_discovery=False)
        try:
            return service.projects().locations().services().setIamPolicy(
                resource=service_name,
                body={
                    "policy": {
                        "bindings": [{
                            "role": 'roles/run.invoker',
                            "members": ['allUsers']
                        }]
                    }
                }
            ).execute()
        except Exception as exc:
            print(f"{datetime.now()} - Error while allowing unauth calls - {exc.__str__()}")
            raise CloudRunException(status_code=500, message='Error while allowing unauth calls')