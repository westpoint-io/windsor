from cookiecutter.main import cookiecutter
from windsor.utils import get_cookiecutter_path
from windsor.services.lambda_ import runtime as runtimemod
from windsor.cdkdependencies import CDKDependencies


class Function:
    """AWS Lambda Function.

    Parameters
    ----------
        function_name -> str
            Name of the function that will be created.

        runtime -> str
            Lambda function runtime.
    """

    def __init__(self, function_name, runtime):
        runtimecls = getattr(runtimemod, runtime)

        cookiecutter(
            get_cookiecutter_path('lambda'),
            no_input=True,
            extra_context={
                'function_name': function_name,
                'runtime': runtimecls.code,
                'file_extension': runtimecls.file_extension,
                'dependencies_file': runtimecls.dependencies_file
            },
            overwrite_if_exists=True
        )

        CDKDependencies.install('aws-lambda')
