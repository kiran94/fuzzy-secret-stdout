from unittest.mock import Mock, call
from fuzzy_secret_stdout.integrations.aws_secret_manager import AWSSecretManager
from fuzzy_secret_stdout.models import SecretStoreItem

import pytest

@pytest.mark.parametrize("list_secrets_return", [
    pytest.param({}, id='empty_response'),
    pytest.param({'SecretList': []}, id='empty_parameters')
])
def test_fetch_all_no_parameters(list_secrets_return: dict):

    mock_secret_man: Mock = Mock()
    mock_secret_man.list_secrets.return_value = list_secrets_return

    integration = AWSSecretManager(mock_secret_man)
    result = integration.fetch_all()

    assert result == []
    assert mock_secret_man.list_secrets.call_args_list == [call(MaxResults=3)]


@pytest.mark.parametrize("max_results", [
    3,
    5,
    10
])
def test_fetch_all_max_results_override(max_results: int):
    mock_secret_man: Mock = Mock()
    mock_secret_man.list_secrets.return_value = []

    integration = AWSSecretManager(mock_secret_man)
    integration.fetch_all(max_batch_results=max_results)

    assert mock_secret_man.list_secrets.call_args_list == [call(MaxResults=max_results)]

def test_fetch_all__keys_no_pagination():

    mock_secret_man: Mock = Mock()
    mock_secret_man.list_secrets.return_value = {
        'SecretList': [
            {'Name': 'param1'},
            {'Name': 'param2'},
            {'Name': 'param3'},
        ]
    }

    integration = AWSSecretManager(mock_secret_man)
    result = integration.fetch_all()

    assert mock_secret_man.list_secrets.call_args_list == [call(MaxResults=3)]
    assert result == [
        SecretStoreItem(key='param1'),
        SecretStoreItem(key='param2'),
        SecretStoreItem(key='param3')
    ]

def test_fetch_all_keys_pagination():

    mock_secret_man: Mock = Mock()
    mock_secret_man.list_secrets.side_effect = [
        # initial call
        {
            'SecretList': [ {'Name': 'param1'}],
            'NextToken': 'token1'
        },
        # second call
        {
            'SecretList': [ {'Name': 'param2'}, {'Name': 'param3'} ],
            'NextToken': 'token2'
        },
        # final call
        {
            'SecretList': [
                {'Name': 'param4'}
            ]
        },
    ]

    integration = AWSSecretManager(mock_secret_man)
    result = integration.fetch_all()

    assert result == [
        SecretStoreItem(key='param1'),
        SecretStoreItem(key='param2'),
        SecretStoreItem(key='param3'),
        SecretStoreItem(key='param4')
    ]

    assert mock_secret_man.list_secrets.call_args_list == [call(MaxResults=3), call(NextToken='token1', MaxResults=3), call(NextToken='token2', MaxResults=3)]
