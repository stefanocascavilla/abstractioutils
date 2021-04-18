import json

from datetime import datetime

from abstractioutils.providers.aws.base import Base
from abstractioutils.exceptions.aws.sns_exception import SNSException


class SNS(Base):
    def __init__(self):
        super().__init__('sns')

    def publish_message(self, topic_arn: str, message: dict) -> str:
        try:
            message_ack = self._get_client().publish(
                TopicArn=topic_arn,
                Message=json.dumps(message)
            )

            return message_ack.get('MessageId')
        except Exception as exc:
            print(f"{datetime.now()} - Error while publishing message to SNS - {exc}")
            raise SNSException(status_code=500, message=exc.__str__())
