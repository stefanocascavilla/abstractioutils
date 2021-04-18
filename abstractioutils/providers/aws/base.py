import abc
import boto3


class Base(metaclass=abc.ABCMeta):
    def __init__(self, service: str):
        self.__client = boto3.client(service)

    def _get_client(self):
        return self.__client
