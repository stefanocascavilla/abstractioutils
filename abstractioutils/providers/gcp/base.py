import json
import abc

from google.oauth2 import service_account


class Base(metaclass=abc.ABCMeta):
    def __init__(self, service_account_info: str):
        self.__service_account_info = service_account_info

    def __get_credentials(self, scopes: list) -> service_account.Credentials:
        credentials = service_account.Credentials.from_service_account_info(json.loads(self.__service_account_info))
        credentials = credentials.with_scopes([single_scope for single_scope in scopes])
        return credentials

    def _get_credentials(self) -> service_account.Credentials:
        return self.__get_credentials(scopes=['https://www.googleapis.com/auth/cloud-platform'])
