from cookiecutter.main import cookiecutter
from windsor.utils import get_cookiecutter_path
from windsor.services.lambda_ import runtime as runtimemod
from windsor.cdkdependencies import CDKDependencies
from windsor.config import current_config


class Function:
    """AWS Lambda Function.

    Parameters
    ----------
        function_name -> str
            Name of the function that will be created.

        runtime -> str
            Lambda function runtime.
    """

    def __init__(self, function_name, runtime=None, handler=None, code=None):
        config_properties = current_config.resource('lambda').properties

        if not runtime:
            runtime = config_properties['DefaultRuntime']

        runtimecls = getattr(runtimemod, runtime)

        cookiecutter_context = {
            'function_name': function_name,
            'code': code,
            'runtime': runtimecls.code,
            'file_extension': runtimecls.file_extension,
            'dependencies_file': runtimecls.dependencies_file
        }

        if code:
            cookiecutter_context['code'] = code

        if handler:
            cookiecutter_context['handler'] = handler

        cookiecutter(
            get_cookiecutter_path('lambda'),
            no_input=True,
            extra_context=cookiecutter_context,
            overwrite_if_exists=True
        )

        CDKDependencies.install('aws-lambda')

        print('[*] Added Lambda Function:', function_name)
        print(f'''
To use it just paste the following lines to your CDK stack.

import {function_name.upper().replace('-', '')}Function from './constructs/{function_name.lower()}';
...
new {function_name.upper().replace('-', '')}Function(this, '{function_name.upper().replace('-', '')}Function');''')
