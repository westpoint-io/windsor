import os

from importlib import import_module
from windsor.config import current_config
from windsor.resources import resources
from windsor.cdkdependencies import CDKDependencies


class Windsor:
    """Windsor CLI main class designed to be used with fire. """

    def init(self, **kwargs):
        """Start CDK environment using windsor config. """

        current_config.setup(updates=kwargs)
        CDKDependencies.init_cdk()
        current_config.save(os.getcwd())

    def lock(self):
        """Lock the current CDK version by reinstalling packages with different
        versions. """

        current_config.load(os.getcwd())

        CDKDependencies.lock_version()

    def install(self, *args):
        """Install CDK dependencies. """

        CDKDependencies.install(*args)

    def generate(self, resource, **kwargs):
        """Generate files and folders for a new CDK resource.

        kwargs will be the arguments needed for each resource.

        Parameters
        ----------
            resource -> str
                Name of the resource to generate.
        """

        current_config.load(os.getcwd())

        resourcecls_info = resources.get(resource)
        strmodule = resourcecls_info.get('module')
        strclass = resourcecls_info.get('class')

        if not resourcecls_info:
            raise AttributeError(f'Resource {resource} not found')

        module = import_module(strmodule)

        getattr(module, strclass)(**kwargs)
