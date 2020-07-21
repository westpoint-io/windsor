from importlib import import_module
from windsor.resources import resources


class Windsor:
    def generate(self, resource, **kwargs):
        _resource = resources.get(resource)
        _module = _resource.get('module')
        _class = _resource.get('class')

        if not _resource:
            raise AttributeError(f'Resource {resource} not found')

        module = import_module(_module)

        getattr(module, _class)(**kwargs)
