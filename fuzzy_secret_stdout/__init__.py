import os
import logging

LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', logging.WARN)
logging.basicConfig(format=logging.BASIC_FORMAT, level=LOGGING_LEVEL)
