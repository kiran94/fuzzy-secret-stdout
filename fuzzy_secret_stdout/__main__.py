import sys
import logging

from pyfzf.pyfzf import FzfPrompt

from fuzzy_secret_stdout.models import SecretStoreItem
from fuzzy_secret_stdout.integrations.factory import create_integration, Integration

from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text

logger = logging.getLogger(__name__)


def main():
    search = FzfPrompt()

    integration_client = create_integration(Integration.AWS_SSM)

    with Live(Spinner('dots', text=Text('Loading')), transient=True):
        result: list[SecretStoreItem] = integration_client.fetch_all()

    keys: list[str] = [x.key for x in result]

    selected: list[str] = search.prompt(keys)
    result: list[SecretStoreItem] = integration_client.fetch_secrets(selected)

    for current_result in result:
        sys.stdout.write(current_result.value)

if __name__ == '__main__': # pragma: nocover
    main()
