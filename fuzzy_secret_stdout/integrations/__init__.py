from typing import Optional
from abc import ABC, abstractmethod

from fuzzy_secret_stdout.models import SecretStoreItem

class SecretIntegration(ABC):

    @abstractmethod
    def fetch_all(self, max_batch_results: Optional[int] = 3) -> list[SecretStoreItem]: # pragma: nocover
        pass

    @abstractmethod
    def fetch_secrets(self, item_names: list[str]) -> list[SecretStoreItem]: # pragma: nocover
        pass
