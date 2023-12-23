from unittest.mock import Mock, call
from ssm_view.ssm import fetch_all_ssm_keys

import pytest


@pytest.mark.parametrize("describe_parameters_return", [
    pytest.param({}, id='empty_response'),
    pytest.param({'Parameters': []}, id='empty_parameters')
])
def test_fetch_all_ssm_keys_no_parameters(describe_parameters_return: dict):

    mock_ssm: Mock = Mock()
    mock_ssm.describe_parameters.return_value = describe_parameters_return

    result = fetch_all_ssm_keys(mock_ssm)

    assert result == []
    assert mock_ssm.describe_parameters.call_args_list == [call(MaxResults=3)]


@pytest.mark.parametrize("max_results", [
    3,
    5,
    10
])
def test_fetch_all_ssm_keys_max_results_override(max_results: int):
    mock_ssm: Mock = Mock()
    mock_ssm.describe_parameters.return_value = []

    fetch_all_ssm_keys(mock_ssm, max_batch_results=max_results)

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

    result = fetch_all_ssm_keys(mock_ssm)

    assert result == [{'Name': 'param1'}, {'Name': 'param2'}, {'Name': 'param3'}]
    assert mock_ssm.describe_parameters.call_args_list == [call(MaxResults=3)]

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

    result = fetch_all_ssm_keys(mock_ssm)

    assert result == [{'Name': 'param1'}, {'Name': 'param2'}, {'Name': 'param3'}, {'Name': 'param4'}]
    assert mock_ssm.describe_parameters.call_args_list == [call(MaxResults=3), call(NextToken='token1', MaxResults=3), call(NextToken='token2', MaxResults=3)]
