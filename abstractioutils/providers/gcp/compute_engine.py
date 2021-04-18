import os

from datetime import datetime
from time import sleep

from abstractioutils.providers.gcp.base import Base
from googleapiclient.discovery import build

from abstractioutils.exceptions.gcp.compute_engine_exception import ComputeEngineException


class ComputeEngine(Base):
    def __init__(self, service_account_info: str):
        super().__init__(service_account_info)

    def reserve_static_ip_address(self, project: str, name: str, region: str) -> dict:
        print(f"{datetime.now()} - Reserving static IP...")

        service = build('compute', 'v1', credentials=self._get_credentials(), cache_discovery=False)
        try:
            return service.addresses().insert(
                project=project,
                region=region,
                body={
                    "name": name
                }
            ).execute()
        except Exception as exc:
            print(f"{datetime.now()} - Error while reserving static IP - {exc.__str__()}")
            raise ComputeEngineException(status_code=500, message='Error while reserving static IP')

    def delete_static_ip_address(self, project: str, region: str, address: str) -> dict:
        print(f"{datetime.now()} - Deleting static IP {address}...")

        service = build('compute', 'v1', credentials=self._get_credentials(), cache_discovery=False)
        try:
            return service.addresses().delete(
                project=project,
                region=region,
                address=address
            ).execute()
        except Exception as exc:
            print(f"{datetime.now()} - Error while deleting static IP {address} - {exc.__str__()}")
            raise ComputeEngineException(status_code=500, message='Error while deleting static IP')

    def get_static_ip_address(self, project: str, name: str, region: str) -> (str, str):
        print(f"{datetime.now()} - Getting the {name} static IP...")

        service = build('compute', 'v1', credentials=self._get_credentials(), cache_discovery=False)
        try:
            count = 0
            while count < int(os.environ.get("STATIC_ADDRESS_RETRIES")):
                static_ip = service.addresses().get(
                    project=project,
                    region=region,
                    address=name
                ).execute()

                if 'address' in static_ip and 'selfLink' in static_ip:
                    return static_ip['address'], static_ip['selfLink']
                count += 1
                sleep(5)
            raise Exception("Not able to get IP address")
        except Exception as exc:
            print(f"{datetime.now()} - Error while getting static IP - {exc.__str__()}")
            raise ComputeEngineException(status_code=500, message='Error while getting static IP')

    def create_cloud_router_with_nat(
        self,
        project: str,
        name: str,
        region: str,
        static_ip: str,
        subnetwork: str
    ) -> dict:
        print(f"{datetime.now()} - Creating the Cloud Router...")

        service = build('compute', 'v1', credentials=self._get_credentials(), cache_discovery=False)
        try:
            return service.routers().insert(
                project=project,
                region=region,
                body={
                    "name": name,
                    "nats": [{
                        "name": name,
                        "natIpAllocateOption": "MANUAL_ONLY",
                        "natIps": [static_ip],
                        "sourceSubnetworkIpRangesToNat": "LIST_OF_SUBNETWORKS",
                        "subnetworks": [{
                            "name": f"regions/{region}/subnetworks/{subnetwork}"
                        }]
                    }],
                    "network": f"https://www.googleapis.com/compute/v1/projects/{project}/global/networks/abstractio"
                }
            ).execute()
        except Exception as exc:
            print(f"{datetime.now()} - Error while creating Cloud Router - {exc.__str__()}")
            raise ComputeEngineException(status_code=500, message='Error while creating Cloud Router')

    def delete_cloud_router(
        self,
        project: str,
        region: str,
        router_name: str
    ) -> dict:
        print(f"{datetime.now()} - Deleting the Cloud Router {router_name}...")

        service = build('compute', 'v1', credentials=self._get_credentials(), cache_discovery=False)
        try:
            return service.routers().delete(
                project=project,
                region=region,
                router=router_name
            ).execute()
        except Exception as exc:
            print(f"{datetime.now()} - Error while deleting the cloud router {router_name} - {exc.__str__()}")
            raise ComputeEngineException(status_code=500, message='Error while creating the cloud router')

    def create_compute_engine_instance(
        self,
        project: str,
        zone: str,
        body: dict
    ) -> dict:
        service = build('compute', 'v1', credentials=self._get_credentials(), cache_discovery=False)
        try:
            return service.instances().insert(
                project=project,
                zone=zone,
                body=body
            ).execute()
        except Exception as exc:
            print(f"{datetime.now()} - Error while creating the VM {body['name']} - {exc.__str__()}")
            raise ComputeEngineException(status_code=500, message='Error while creating the VM')

    def delete_compute_engine_virtual_machine(
        self,
        project: str,
        zone: str,
        name: str
    ) -> dict:
        print(f"{datetime.now()} - Deleting the {name} VM...")

        service = build('compute', 'v1', credentials=self._get_credentials(), cache_discovery=False)
        try:
            return service.instances().delete(
                project=project,
                zone=zone,
                instance=name
            ).execute()
        except Exception as exc:
            print(f"{datetime.now()} - Error while deleting the VM {name} - {exc.__str__()}")
            raise ComputeEngineException(status_code=500, message='Error while deleting the VM')