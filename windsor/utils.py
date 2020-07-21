import os


def get_cookiecutter_path(*dirs):
    rootdir = os.path.abspath(os.path.dirname(__file__))
    cookiecutterdir = os.path.join(rootdir, 'cookiecutter')

    return os.path.join(cookiecutterdir, *dirs)
