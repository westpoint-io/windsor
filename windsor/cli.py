import fire

from windsor.main import Windsor


def run():
    """Run Windsor cli using fire. """

    fire.Fire(Windsor)
