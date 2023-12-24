import os
import boto3
import logging

from pyfzf.pyfzf import FzfPrompt

from ssm_view.integrations.aws_ssm import AWSParameterStore
from ssm_view.models import SecretStoreItem

from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text


LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', logging.WARN)
logging.basicConfig(format=logging.BASIC_FORMAT, level=LOGGING_LEVEL)
logger = logging.getLogger(__name__)


def main():
    search = FzfPrompt()

    # TODO: Move to Factory
    aws_ssm = AWSParameterStore(boto3.client('ssm'))

    with Live(Spinner('dots', text=Text('Loading')), transient=True):
        result: list[SecretStoreItem] = aws_ssm.fetch_all()

    ssm_keys: list[str] = [x.key for x in result]

    selected: list[str] = search.prompt(ssm_keys)
    result: list[SecretStoreItem] = aws_ssm.fetch_secrets(selected)

    for current_result in result:
        print(current_result.value)

if __name__ == '__main__': # pragma: nocover
    main()
