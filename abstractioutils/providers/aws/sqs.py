import json

from datetime import datetime

from abstractioutils.providers.aws.base import Base
from abstractioutils.exceptions.aws.sqs_exception import SQSException


class SQS(Base):
    def __init__(self):
        super().__init__('sqs')

    def send_message(self, queue_url: str, message_body: dict) -> str:
        try:
            message_ack = self._get_client().send_message(
                QueueUrl=queue_url,
                MessageBody=json.dumps(message_body)
            )

            return message_ack.get('MessageId')
        except Exception as exc:
            print(f"{datetime.now()} - Error while sending message to SQS - {exc}")
            raise SQSException(status_code=500, message=exc.__str__())
