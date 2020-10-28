import os

from marshmallow import Schema, fields


class CDKLanguage:
    """CDK language that windsor have compatibility. """

    TYPESCRIPT = 'typescript'


class ConfigResourcePropertySchema(Schema):
    Name = fields.Str(required=True)
    Value = fields.Str(required=True)


class ConfigResourceSchema(Schema):
    Resource = fields.Str(required=True)
    Properties = fields.List(fields.Nested(ConfigResourcePropertySchema()), required=True)


class ConfigSchema(Schema):
    CDKLanguage = fields.Str(required=True)
    CDKVersion = fields.Str(required=True)
    Resources = fields.List(fields.Nested(ConfigResourceSchema()), required=True)


class ConfigResource(object):
    """Config resource as object.

    :param res: Resource to load.
    :type res: dict
    """

    def __init__(self, res):
        self.name = res.get('Resource')
        self.properties = {}

        for prop in res.get('Properties'):
            k, v = prop.get('Name'), prop.get('Value')
            self.properties[k] = v


class ConfigBase(object):
    """Windsor base configuration class. """

    def __init__(self, config_path):
        self.config_path = config_path
        self.schema = ConfigSchema()
        self.cfg = None

    def __getattr__(self, attr):
        if not self.cfg:
            return None

        return self.cfg.get(attr)

    def read(self):
        """Reads the file located at self.config_path, validates it and return
        its contents as a dict-like object."""

        if self.cfg:
            return self.cfg

        with open(self.config_path) as buf:
            s = buf.read()

        self.cfg = self.schema.loads(s)

        return self

    def write(self, obj):
        """Writes the config to the current project directory.

        :param obj: Config as dict-like object to dump into a file.
        :type obj: dict
        """

        with open(os.path.join(os.getcwd(), 'windsor.json'), 'w') as buf:
            buf.write(self.schema.dumps(obj, indent=4))

    def update(self, obj):
        """Updates the current configuration with a new object. """

        self.cfg.update(obj)

    def setup(self):
        """Reads `defaultconfig.json` file and dumps its content into the
        project directory. """

        default_config = self.read()

        self.write(default_config)

    def resource(self, n):
        """Get a resource from property Resources of config.

        :param n: Name of the resource the get.
        :type n: str
        """

        cfg = self.read()

        for res in cfg.get('Resources', []):
            res_name = res.get('Resource')

            if res_name == n:
                return ConfigResource(res)


class DefaultConfig(ConfigBase):
    """Windsor configuration class. """

    WINDSOR_DIR = os.path.abspath(os.path.dirname(__file__))
    DEFAULT_CONFIG_PATH = os.path.join(WINDSOR_DIR, 'data',
                                       'configdefault.json')

    def __init__(self):
        super().__init__(self.DEFAULT_CONFIG_PATH)
        self.read()


class ProjectConfig(ConfigBase):
    CONFIG_PATH = os.path.join(os.getcwd(), 'windsor.json')

    def __init__(self):
        super().__init__(self.CONFIG_PATH)


if os.path.isfile(ProjectConfig.CONFIG_PATH):
    current_config = ProjectConfig()
else:
    current_config = DefaultConfig()
