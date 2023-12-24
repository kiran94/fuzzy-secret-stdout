import logging
from typing import Optional

from fuzzy_secret_stdout.models import SecretStoreItem
from fuzzy_secret_stdout.integrations import SecretIntegration

logger = logging.getLogger(__name__)

class AWSParameterStore(SecretIntegration):

    def __init__(self, boto_client) -> None:
        self._boto_client = boto_client

    def fetch_all(self, max_batch_results: Optional[int] = 3) -> list[SecretStoreItem]:
        logging.info("fetching all ssm keys with batch results %s", max_batch_results)

        raw_result: dict = self._boto_client.describe_parameters(MaxResults=max_batch_results)

        if 'Parameters' not in raw_result or not raw_result['Parameters']:
            logging.debug("could not find any ssm keys")
            return []

        results: list[SecretStoreItem] = []
        for parameter in raw_result['Parameters']:
            results.append(SecretStoreItem(parameter['Name']))

        while 'NextToken' in raw_result:
            logging.info("found %s ssm keys and a NextToken, fetching next batch", len(raw_result['Parameters']))

            raw_result = self._boto_client.describe_parameters(NextToken=raw_result['NextToken'], MaxResults=max_batch_results)
            for parameter in raw_result['Parameters']:
                results.append(SecretStoreItem(parameter['Name']))

        logging.info("found %s total ssm keys", len(results))
        return results

    def fetch_secrets(self, item_names: list[str]) -> list[SecretStoreItem]:
        result = self._boto_client.get_parameters(Names=item_names, WithDecryption=True)
        result = [SecretStoreItem(x['Name'], x['Value']) for x in result['Parameters']]
        return result
