from unittest.mock import patch, Mock, call

from fuzzy_secret_stdout.__main__ import main
from fuzzy_secret_stdout.integrations.factory import Integration
from fuzzy_secret_stdout.models import SecretStoreItem

@patch('fuzzy_secret_stdout.__main__.sys')
@patch('fuzzy_secret_stdout.__main__.FzfPrompt')
@patch('fuzzy_secret_stdout.__main__.create_integration')
def test_main(mock_create_integration: Mock, mock_prompt: Mock, mock_sys: Mock):

    mock_integration_client = Mock()
    mock_integration_client.fetch_all.return_value = [ SecretStoreItem("param1"), SecretStoreItem("param2") ]
    mock_integration_client.fetch_secrets.return_value = [ SecretStoreItem("param2", 'my_super_cool_value')]
    mock_create_integration.return_value = mock_integration_client

    mock_prompt.prompt.return_value = 'param2'

    main()

    assert mock_sys.stdout.write.call_args_list == [call('my_super_cool_value')]
    assert mock_create_integration.call_args_list == [call(Integration.AWS_SSM)]
