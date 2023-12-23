import os
import boto3
import logging

from pyfzf.pyfzf import FzfPrompt
from ssm_view.ssm import fetch_all_ssm_keys


LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', logging.WARN)
logging.basicConfig(format=logging.BASIC_FORMAT, level=LOGGING_LEVEL)
logger = logging.getLogger(__name__)


def main():
    ssm = boto3.client('ssm')
    search = FzfPrompt()

    result = fetch_all_ssm_keys(ssm)
    ssm_keys: list[str] = [x['Name'] for x in result]

    selected: list[str] = search.prompt(ssm_keys)
    result = ssm.get_parameters(Names=selected, WithDecryption=True)

    for current_result in result['Parameters']:
        print(current_result['Value'])

if __name__ == '__main__':
    main()
