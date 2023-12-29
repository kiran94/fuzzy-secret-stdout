from typing import Optional
from abc import ABC, abstractmethod
import logging

from fuzzy_secret_stdout.models import SecretStoreItem

logger = logging.getLogger(__name__)

class SecretIntegration(ABC):

    @abstractmethod
    def fetch_all(self, max_batch_results: Optional[int] = 3) -> list[SecretStoreItem]: # pragma: nocover
        pass

    @abstractmethod
    def fetch_secrets(self, item_names: list[str]) -> list[SecretStoreItem]: # pragma: nocover
        pass

    def _paginate_results(self, func, max_batch_results: int, outer_response_key: str, inner_response_key: str, label: str) -> list[SecretStoreItem]:
        """
        Paginates over a function to collect all the results

        Args:
            func (): the function repeat call e.g call to aws boto describe_parameters
            max_batch_results: the maximum number of results allowed per internal batch
            outer_response_key: the key in the response to use to get internal data
                e.g in an AWS describe_parameters, data is slotted into the "Parameters" payload
            inner_response_key: the key in the innner response to get secret names
                e.g in the AWS describe_parameters, data is slotted into the "Name" field
            label: name used for logging

        Returns:
            List of SecretStoreItem
        """
        logging.info("fetching all %s keys with batch results %s", label, max_batch_results)

        raw_result: dict = func(self._boto_client, MaxResults=max_batch_results)

        if outer_response_key not in raw_result or not raw_result[outer_response_key]:
            logging.debug("could not find any %s keys", label)
            return []

        results: list[SecretStoreItem] = []
        for parameter in raw_result[outer_response_key]:
            results.append(SecretStoreItem(parameter[inner_response_key]))

        while 'NextToken' in raw_result:
            logging.info("found %s %s keys and a NextToken, fetching next batch", label, len(raw_result[outer_response_key]))

            raw_result = func(self._boto_client, NextToken=raw_result['NextToken'], MaxResults=max_batch_results)

            for parameter in raw_result[outer_response_key]:
                results.append(SecretStoreItem(parameter['Name']))

        logging.info("found %s total %s keys", label, len(results))
        return results
