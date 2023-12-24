from typing import Optional
from abc import ABC, abstractmethod

from ssm_view.models import SecretStoreItem

class SecretIntegration(ABC):

    @abstractmethod
    def fetch_all(self, max_batch_results: Optional[int] = 3) -> list[SecretStoreItem]:
        pass

    @abstractmethod
    def fetch_secrets(self, item_names: list[str]) -> list[SecretStoreItem]:
        pass
