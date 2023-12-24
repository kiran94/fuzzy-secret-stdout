from fuzzy_secret_stdout.integrations import SecretIntegration

def test_secret_integration_abc():
    assert hasattr(SecretIntegration, 'fetch_all')
    assert hasattr(SecretIntegration, 'fetch_secrets')
