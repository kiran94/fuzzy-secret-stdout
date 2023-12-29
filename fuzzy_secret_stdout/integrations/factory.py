from enum import Enum

import boto3

from fuzzy_secret_stdout.integrations.aws_ssm import AWSParameterStore
from fuzzy_secret_stdout.integrations.aws_secret_manager import AWSSecretManager
from fuzzy_secret_stdout.integrations import SecretIntegration

class Integration(str, Enum):
    AWS_SSM = "AWS_SSM"
    AWS_SECRET_MAN = "AWS_SECRET_MAN"

    @staticmethod
    def list_options() -> list[str]:
        return [x.value for x in Integration]


def create_integration(integration: Integration) -> SecretIntegration:
    if integration == Integration.AWS_SSM:
        return AWSParameterStore(boto3.client('ssm'))
    elif integration == Integration.AWS_SECRET_MAN:
        return AWSSecretManager(boto3.client('secretsmanager'))
    else:
        raise NotImplementedError(f'integration {integration} not implemented')
