import os
import logging
import fire

from windsor.main import Windsor


def run():
    """Run Windsor cli using fire. """

    LOG_LEVEL = os.getenv('WINDSOR_LOG_LEVEL', None)

    logging.basicConfig(format='[*] %(message)s', level=LOG_LEVEL or logging.INFO)

    fire.Fire(Windsor)
