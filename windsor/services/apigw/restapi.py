import logging

from cookiecutter.main import cookiecutter
from windsor.utils import get_cookiecutter_path
from windsor.cdkdependencies import CDKDependencies


class RestApi:
    def __init__(self, restapi_name, *args, **kwargs):
        cookiecutter_context = {
            'restapi_name': restapi_name
        }

        cookiecutter(
            get_cookiecutter_path('apigw-restapi'),
            no_input=True,
            extra_context=cookiecutter_context,
            overwrite_if_exists=True
        )

        CDKDependencies.install('aws-apigateway')

        logging.info(f'Added RestAPI {restapi_name}')
