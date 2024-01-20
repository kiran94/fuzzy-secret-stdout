from unittest.mock import Mock, call
from fuzzy_secret_stdout.integrations.aws_ssm import AWSParameterStore
from fuzzy_secret_stdout.models import SecretStoreItem

import pytest


@pytest.mark.parametrize("describe_parameters_return", [
    pytest.param({}, id='empty_response'),
    pytest.param({'Parameters': []}, id='empty_parameters')
])
def test_fetch_all_no_parameters(describe_parameters_return: dict):

    mock_ssm: Mock = Mock()
    mock_ssm.describe_parameters.return_value = describe_parameters_return

    integration = AWSParameterStore(mock_ssm)
    result = integration.fetch_all()

    assert result == []
    assert mock_ssm.describe_parameters.call_args_list == [call(MaxResults=50)]


@pytest.mark.parametrize("max_results", [
    3,
    5,
    10
])
def test_fetch_all_max_results_override(max_results: int):
    mock_ssm: Mock = Mock()
    mock_ssm.describe_parameters.return_value = []

    integration = AWSParameterStore(mock_ssm)
    integration.fetch_all(max_batch_results=max_results)

    assert mock_ssm.describe_parameters.call_args_list == [call(MaxResults=max_results)]

def test_fetch_all_ssm_keys_no_pagination():

    mock_ssm: Mock = Mock()
    mock_ssm.describe_parameters.return_value = {
        'Parameters': [
            {'Name': 'param1'},
            {'Name': 'param2'},
            {'Name': 'param3'},
        ]
    }

    integration = AWSParameterStore(mock_ssm)
    result = integration.fetch_all()

    assert mock_ssm.describe_parameters.call_args_list == [call(MaxResults=50)]
    assert result == [
        SecretStoreItem(key='param1'),
        SecretStoreItem(key='param2'),
        SecretStoreItem(key='param3')
    ]

def test_fetch_all_ssm_keys_pagination():

    mock_ssm: Mock = Mock()
    mock_ssm.describe_parameters.side_effect = [
        # initial call
        {
            'Parameters': [ {'Name': 'param1'}],
            'NextToken': 'token1'
        },
        # second call
        {
            'Parameters': [ {'Name': 'param2'}, {'Name': 'param3'} ],
            'NextToken': 'token2'
        },
        # final call
        {
            'Parameters': [
                {'Name': 'param4'}
            ]
        },
    ]

    integration = AWSParameterStore(mock_ssm)
    result = integration.fetch_all()

    assert result == [
        SecretStoreItem(key='param1'),
        SecretStoreItem(key='param2'),
        SecretStoreItem(key='param3'),
        SecretStoreItem(key='param4')
    ]

    assert mock_ssm.describe_parameters.call_args_list == [call(MaxResults=50), call(NextToken='token1', MaxResults=50), call(NextToken='token2', MaxResults=50)]


def test_fetch_secrets():
    input = ['param1']

    mock_ssm: Mock = Mock()
    mock_ssm.get_parameters.return_value = {
        'Parameters': [
            {'Name': 'param1', 'Value': 'value1'}
        ]
    }

    integration = AWSParameterStore(mock_ssm)
    result = integration.fetch_secrets(input)

    assert result == [SecretStoreItem(key='param1', value='value1')]
    assert mock_ssm.get_parameters.call_args_list == [call(Names=['param1'], WithDecryption=True)]
