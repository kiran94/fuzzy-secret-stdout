from unittest.mock import patch, Mock, call

import pytest

from fuzzy_secret_stdout.integrations.factory import create_integration, Integration
from fuzzy_secret_stdout.integrations.aws_ssm import AWSParameterStore

@patch('fuzzy_secret_stdout.integrations.factory.boto3')
def test_create_integration_ssm(mock_boto: Mock):
    result = create_integration(Integration.AWS_SSM)

    assert isinstance(result, AWSParameterStore)
    assert result._boto_client == mock_boto.client.return_value
    assert mock_boto.client.call_args_list == [call('ssm')]


def test_create_integration_unimplemented():
    with pytest.raises(NotImplementedError, match='integration DUMMY not implemented'):
        create_integration("DUMMY")

def test_integration_list_options():
    assert Integration.list_options() == ['AWS_SSM']
