import os


def get_cookiecutter_path(*dirs):
    """Get a cookiecutter project present on windsor cookiecutter directory.

    dirs is a list of dirs that will be used as commands for os.path.join
    method.
    """

    rootdir = os.path.abspath(os.path.dirname(__file__))
    cookiecutterdir = os.path.join(rootdir, 'cookiecutter')

    return os.path.join(cookiecutterdir, *dirs)
