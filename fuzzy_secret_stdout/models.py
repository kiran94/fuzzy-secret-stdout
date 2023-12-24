from dataclasses import dataclass

@dataclass
class SecretStoreItem:
    key: str
    value: str = None
