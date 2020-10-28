import os
import logging
import json

from importlib import import_module
from windsor.config import current_config, DefaultConfig
from windsor.cdkdependencies import CDKDependencies


class Windsor:
    """Windsor CLI main class designed to be used with fire. """

    @staticmethod
    def init():
        """Start CDK environment using windsor config. """

        config = DefaultConfig()

        CDKDependencies.init_cdk(cfg=config)

        config.setup()

    @staticmethod
    def lock():
        """Lock the current CDK version by reinstalling packages with different
        versions. """

        current_config.read()

        CDKDependencies.lock_version()

    @staticmethod
    def install(*args):
        """Install CDK dependencies. """

        current_config.read()

        CDKDependencies.install(*args)

    @staticmethod
    def generate(resource, **kwargs):
        """Generate files and folders for a new CDK resource.

        kwargs will be the arguments needed for each resource.

        Parameters
        ----------
            resource -> str
                Name of the resource to generate.
        """

        current_config.read()

        resources_path = os.path.join(DefaultConfig.WINDSOR_DIR, 'data', 'resources.json')

        with open(resources_path) as resbuf:
            resources = json.load(resbuf)

        resourcecls_info = resources.get(resource)
        resourcecls_params = resourcecls_info.get('parameter_requires', [])

        if not resourcecls_info:
            logging.info(f'Resource `{resource}` not found')
            return

        for param in resourcecls_params:
            if param not in kwargs:
                logging.info(f'Missing parameter {param}')
                return

        strmodule = resourcecls_info.get('module')
        strclass = resourcecls_info.get('class')

        module = import_module(strmodule)

        getattr(module, strclass)(**kwargs)
