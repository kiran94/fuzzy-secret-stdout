import os
import logging

from pyfzf.pyfzf import FzfPrompt

from ssm_view.models import SecretStoreItem
from ssm_view.integrations.factory import create_integration, Integration

from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text


LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', logging.WARN)
logging.basicConfig(format=logging.BASIC_FORMAT, level=LOGGING_LEVEL)
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
        print(current_result.value)

if __name__ == '__main__': # pragma: nocover
    main()
