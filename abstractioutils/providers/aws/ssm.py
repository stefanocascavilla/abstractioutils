from datetime import datetime

from abstractioutils.providers.aws.base import Base
from abstractioutils.exceptions.aws.ssm_exception import SSMException


class SSM(Base):
    def __init__(self):
        super().__init__('ssm')

    def get_parameter(self, name: str) -> str:
        try:
            parameter = self._get_client().get_parameter(
                Name=name
            )
        except Exception as exc:
            print(f"{datetime.now()} - Error while getting SSM param - {exc}")
            raise SSMException(status_code=500, message=exc.__str__())
        if 'Parameter' not in parameter:
            print(f"{datetime.now()} - Parameter {name} not found")
            raise SSMException(status_code=500, message='Parameter not found')
        return parameter['Parameter']['Value']
