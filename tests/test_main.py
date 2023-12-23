from unittest.mock import patch, Mock, call
from ssm_view.__main__ import main


@patch("ssm_view.__main__.fetch_all_ssm_keys")
@patch("ssm_view.__main__.FzfPrompt")
@patch("ssm_view.__main__.boto3")
@patch("builtins.print")
def test_main(mock_print: Mock, mock_boto: Mock, mock_prompt: Mock, mock_fetch_all_ssm_keys: Mock):
    mock_ssm = Mock()
    mock_boto.client.return_value = mock_ssm

    mock_fetch_all_ssm_keys.return_value = [ {'Name': 'param1'} ]

    mock_prompt.prompt.return_value = "param1"

    mock_ssm.get_parameters.return_value = {
        'Parameters': [ {'Name': 'param1', 'Value': 'value1'} ]
    }

    main()

    assert mock_print.call_args_list == [call("value1")]

    assert mock_fetch_all_ssm_keys.call_args_list == [call(mock_ssm)]
    assert mock_prompt.return_value.prompt.call_args_list == [call(['param1'])]
    assert mock_ssm.get_parameters.call_args_list == [call(Names=mock_prompt.return_value.prompt.return_value, WithDecryption=True)]
