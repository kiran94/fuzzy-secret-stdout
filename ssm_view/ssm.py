import logging
from typing import Optional

logger = logging.getLogger(__name__)


def fetch_all_ssm_keys(ssm, max_batch_results: Optional[int] = 3) -> list[dict]:
    logging.info("fetching all ssm keys with batch results %s", max_batch_results)

    raw_result: dict = ssm.describe_parameters(MaxResults=max_batch_results)

    if 'Parameters' not in raw_result or not raw_result['Parameters']:
        logging.debug("could not find any ssm keys")
        return []

    result: list[dict] = []
    result.extend(raw_result['Parameters'])

    while 'NextToken' in raw_result:
        logging.info("found %s ssm keys and a NextToken, fetching next batch", len(raw_result['Parameters']))

        raw_result = ssm.describe_parameters(NextToken=raw_result['NextToken'], MaxResults=max_batch_results)
        result.extend(raw_result['Parameters'])

    logging.info("found %s total ssm keys", len(result))
    return result
