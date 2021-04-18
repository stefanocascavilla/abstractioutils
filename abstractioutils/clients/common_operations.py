import os

from time import sleep
from datetime import datetime

from abstractioutils.providers.aws.dynamodb import DynamoDB
from abstractioutils.providers.aws.sqs import SQS
from abstractioutils.providers.aws.sns import SNS
from abstractioutils.providers.aws.ssm import SSM

from abstractioutils.providers.gcp.cloud_run import CloudRun
from abstractioutils.providers.gcp.compute_engine import ComputeEngine

from abstractioutils.exceptions.helpers_exception import HelpersException

from abstractioutils.dto.cluster_dto import ClusterDTO


class CommonOperations(object):
    def __init__(self):
        self._dynamodb = DynamoDB()
        self._sqs = SQS()
        self._sns = SNS()
        self._ssm = SSM()

        self._cloud_run = None
        self._compute_engine = None

    @staticmethod
    def _lint_cluster(dynamo_obj: dict) -> ClusterDTO:
        def lint_env_variables() -> dict:
            return_value = dict()
            if dynamo_obj.get('env_variables') is not None:
                for single_item in dynamo_obj['env_variables']['SS']:
                    split_item = single_item.split('=')
                    return_value[split_item[0]] = split_item[1]
            return return_value

        return ClusterDTO.parse_obj({
            'id': dynamo_obj['id']['S'],
            'name': dynamo_obj['id']['S'],
            'image_url': dynamo_obj['image_url']['S'],
            'vcpus': dynamo_obj['vcpus']['N'],
            'memory': dynamo_obj['memory']['N'],
            'user_id': dynamo_obj['user_id']['S'],
            'port': dynamo_obj['port']['N'],
            'has_ip': dynamo_obj['has_ip']['BOOL'],
            'type': dynamo_obj['type']['S'],
            'region': dynamo_obj['region']['S'],
            'status': dynamo_obj['status']['S'],
            'creation_date': dynamo_obj['creation_date']['S'],
            'env_variables': lint_env_variables(),
            'project': dynamo_obj['gcp_project']['S'] if dynamo_obj.get('gcp_project') else None,
            'endpoint': dynamo_obj['endpoint']['S'] if dynamo_obj.get('endpoint') else None,
            'ip_address': dynamo_obj['ip_address']['S'] if dynamo_obj.get('ip_address') else None,
            'error_message': dynamo_obj['error_message']['S'] if dynamo_obj.get('error_message') else None,
            'username': dynamo_obj['username']['S'] if dynamo_obj.get('username') else None,
            'password': dynamo_obj['password']['S'] if dynamo_obj.get('password') else None
        })

    @staticmethod
    def _lint_environment_variables(env_variables: dict) -> list:
        return [f"{key}={env_variables[key]}" for key in env_variables.keys()]

    def _loop_over_cloud_run_service(
        self,
        cluster_id: str,
        cloud_run_name: str,
        region: str,
        has_ip: bool,
        static_ip: str
    ) -> bool:
        print(f"{datetime.now()} - Looping over the Cloud Run service {cloud_run_name}...")

        count = 0
        run_info = None
        while count < int(os.environ.get("CLOUD_RUN_RETRIES")):
            print(f"{datetime.now()} - Attempt number {count}")
            run_info = self._cloud_run.get_service(name=cloud_run_name, region=region)
            if 'conditions' in run_info['status']:
                for single_condition in run_info['status']['conditions']:
                    if single_condition['type'] == 'Ready' and single_condition['status'] == 'True':
                        print(f"{datetime.now()} - Updating the cluster status...")
                        if has_ip:
                            self.update_cluster_information(
                                cluster_id=cluster_id,
                                expression_attribute_names={
                                    '#ip_address': 'ip_address',
                                    '#endpoint': 'endpoint',
                                    '#status': 'status'
                                },
                                expression_attribute_values={
                                    ':ip_address': {
                                        'S': static_ip
                                    },
                                    ':endpoint': {
                                        'S': run_info['status']['url']
                                    },
                                    ':status': {
                                        'S': 'COMPLETED'
                                    }
                                },
                                update_expression='SET #ip_address = :ip_address, #endpoint = :endpoint, #status = :status'
                            )
                        else:
                            self.update_cluster_information(
                                cluster_id=cluster_id,
                                expression_attribute_names={
                                    '#endpoint': 'endpoint',
                                    '#status': 'status'
                                },
                                expression_attribute_values={
                                    ':endpoint': {
                                        'S': run_info['status']['url']
                                    },
                                    ':status': {
                                        'S': 'COMPLETED'
                                    }
                                },
                                update_expression='SET #endpoint = :endpoint, #status = :status'
                            )
                        return True
            count += 1
            sleep(5)

        print(f"{datetime.now()} - Error while creating the Cloud Run service - {run_info['status']}")
        return False

    def _set_gcp_service_account(self, cluster: ClusterDTO) -> None:
        print(f"{datetime.now()} - Setting the service account...")
        service_account = self._ssm.get_parameter(
            name=f"/gcp/{cluster.project}/sa"
        )

        self._cloud_run = CloudRun(service_account_info=service_account)
        self._compute_engine = ComputeEngine(service_account_info=service_account)

    def get_cluster_information(self, cluster_id: str) -> ClusterDTO:
        print(f"{datetime.now()} - Getting the cluster {cluster_id}")
        cluster_info = self._dynamodb.get_item(
            table_name=os.environ.get('TABLE_CLUSTERS'),
            key={
                'id': {'S': cluster_id}
            }
        )

        if cluster_info.get('Item') is None:
            print(f"{datetime.now()} - No cluster found with the given id")
            raise HelpersException(status_code=404, message='No cluster found with the given id')
        return self._lint_cluster(dynamo_obj=cluster_info['Item'])

    def update_cluster_information(
        self,
        cluster_id: str,
        expression_attribute_names: dict,
        expression_attribute_values: dict,
        update_expression: str
    ) -> dict:
        return self._dynamodb.update_item(
            table_name=os.environ.get('TABLE_CLUSTERS'),
            key={
                'id': {
                    'S': cluster_id,
                }
            },
            expression_attribute_names=expression_attribute_names,
            expression_attribute_values=expression_attribute_values,
            update_expression=update_expression
        )

    def send_message_to_sqs(self, message_body: dict, queue_url: str) -> str:
        print(f"{datetime.now()} - Sending the message to SQS - {queue_url}")
        message_ack = self._sqs.send_message(
            queue_url=queue_url,
            message_body=message_body
        )

        if message_ack is None:
            print(f"{datetime.now()} - Something wrong with SQS send message")
            raise HelpersException(status_code=500, message='Something wrong with SQS send message')
        return message_ack

    def publish_message_to_sns(self, message_body: dict, topic_arn: str) -> str:
        print(f"{datetime.now()} - Publishing the failure message to SNS - {topic_arn}")
        publish_ack = self._sns.publish_message(
            topic_arn=topic_arn,
            message=message_body
        )

        if publish_ack is None:
            print(f"{datetime.now()} - Something wrong with SNS publish message")
            raise HelpersException(status_code=500, message='Something wrong with SNS publish message')
        return publish_ack
