from cookiecutter.main import cookiecutter
from windsor.utils import get_cookiecutter_path
from windsor.cdkdependencies import CDKDependencies


class ReactPipeline:
    def __init__(self, pipeline_name):
        cookiecutter(
            get_cookiecutter_path('react-codepipeline'),
            no_input=True,
            extra_context={
                'pipeline_name': pipeline_name
            },
            overwrite_if_exists=True
        )

        CDKDependencies.install(
            'aws-s3',
            'aws-codebuild',
            'aws-codepipeline',
            'aws-codepipeline-actions'
        )
