from enum import Enum

import boto3

from fuzzy_secret_stdout.integrations.aws_ssm import AWSParameterStore
from fuzzy_secret_stdout.integrations import SecretIntegration

class Integration(str, Enum):
    AWS_SSM = "AWS_SSM"


def create_integration(integration: Integration) -> SecretIntegration:
    if integration == Integration.AWS_SSM:
        return AWSParameterStore(boto3.client('ssm'))
    else:
        raise NotImplementedError(f'integration {integration} not implemented')
