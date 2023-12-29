import logging
from typing import Optional

from fuzzy_secret_stdout.models import SecretStoreItem
from fuzzy_secret_stdout.integrations import SecretIntegration

logger = logging.getLogger(__name__)

class AWSParameterStore(SecretIntegration):

    def __init__(self, boto_client) -> None:
        self._boto_client = boto_client

    def fetch_all(self, max_batch_results: Optional[int] = 3) -> list[SecretStoreItem]:

        def inner(boto_client, **kwargs):
            return boto_client.describe_parameters(**kwargs)

        return self._paginate_results(inner, max_batch_results, 'Parameters', 'Name', 'ssm')

    def fetch_secrets(self, item_names: list[str]) -> list[SecretStoreItem]:
        result = self._boto_client.get_parameters(Names=item_names, WithDecryption=True)
        result = [SecretStoreItem(x['Name'], x['Value']) for x in result['Parameters']]
        return result
