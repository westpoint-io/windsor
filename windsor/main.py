from importlib import import_module
from windsor.resources import resources


class Windsor:
    """Windsor CLI main class designed to be used with fire. """

    def generate(self, resource, **kwargs):
        """Generate files and folders for a new CDK resource.

        kwargs will be the arguments needed for each resource.

        Parameters
        ----------
            resource -> str
                Name of the resource to generate.
        """

        resourcecls_info = resources.get(resource)
        strmodule = resourcecls_info.get('module')
        strclass = resourcecls_info.get('class')

        if not resourcecls_info:
            raise AttributeError(f'Resource {resource} not found')

        module = import_module(strmodule)

        getattr(module, strclass)(**kwargs)
