from enum import Enum

import boto3

from fuzzy_secret_stdout.integrations.aws_ssm import AWSParameterStore
from fuzzy_secret_stdout.integrations import SecretIntegration

class Integration(str, Enum):
    AWS_SSM = "AWS_SSM"
    AWS_SECRET_MAN = "AWS_SECRET_MAN"

    @staticmethod
    def list_options():
        return [x.value for x in Integration]


def create_integration(integration: Integration) -> SecretIntegration:
    if integration == Integration.AWS_SSM:
        return AWSParameterStore(boto3.client('ssm'))
    else:
        raise NotImplementedError(f'integration {integration} not implemented')
