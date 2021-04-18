from datetime import datetime

from abstractioutils.providers.aws.base import Base
from abstractioutils.exceptions.aws.dynamodb_exception import DynamoDBException


class DynamoDB(Base):
    def __init__(self):
        super().__init__('dynamodb')

    def get_item(
        self,
        table_name: str,
        key: dict
    ) -> dict:
        try:
            return self._get_client().get_item(
                TableName=table_name,
                Key=key
            )
        except Exception as exc:
            print(f"{datetime.now()} - Error while getting item from the DynamoDB table - {exc}")
            raise DynamoDBException(status_code=500, message=exc.__str__())

    def scan(
        self,
        table_name: str,
        attributes_to_get: list
    ) -> dict:
        try:
            return self._get_client().scan(
                TableName=table_name,
                AttributesToGet=attributes_to_get,
                Select='SPECIFIC_ATTRIBUTES'
            )
        except Exception as exc:
            print(f"{datetime.now()} - Error while scanning items from the DynamoDB table - {exc}")
            raise DynamoDBException(status_code=500, message=exc.__str__())

    def query(
        self,
        table_name: str,
        index_name: str,
        key_condition_expression: str,
        expression_attribute_values: dict
    ) -> dict:
        try:
            return self._get_client().query(
                TableName=table_name,
                IndexName=index_name,
                KeyConditionExpression=key_condition_expression,
                ExpressionAttributeValues=expression_attribute_values
            )
        except Exception as exc:
            print(f"{datetime.now()} - Error while querying the DynamoDB table - {exc}")
            raise DynamoDBException(status_code=500, message=exc.__str__())

    def put_item(
        self,
        table_name: str,
        new_item: dict
    ) -> None:
        try:
            self._get_client().put_item(
                TableName=table_name,
                Item=new_item
            )
        except Exception as exc:
            print(f"{datetime.now()} - Error while creating a new DynamoDB item - {exc}")
            raise DynamoDBException(status_code=500, message=exc.__str__())

    def update_item(
        self,
        table_name: str,
        key: dict,
        expression_attribute_names: dict,
        expression_attribute_values: dict,
        update_expression: str
    ) -> dict:
        try:
            return self._get_client().update_item(
                TableName=table_name,
                Key=key,
                ExpressionAttributeNames=expression_attribute_names,
                ExpressionAttributeValues=expression_attribute_values,
                UpdateExpression=update_expression,
                ReturnValues='UPDATED_NEW'
            )
        except Exception as exc:
            print(f"{datetime.now()} - Error while updating a DynamoDB item - {exc}")
            raise DynamoDBException(status_code=500, message=exc.__str__())