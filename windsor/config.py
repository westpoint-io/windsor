import os
import json

from windsor.attributes import attr_loader


class CDKLanguage:
    """CDK language that windsor have compatibility. """

    TYPESCRIPT = 'typescript'


class Config:
    """Windsor config class. """

    def __init__(self):
        self.language = CDKLanguage.TYPESCRIPT

    def is_valid_key(self, key):
        """Validates the key verifying if it is present it is an attribute
        of this class or an attribute from resource.

        Parameters
        ----------
            key -> str
                Key to be validated.

        Returns
        -------
            Bool indicating if the key is valid or not.
        """

        return hasattr(self, key) or attr_loader.contains(key)

    def apply_updates(self, updates):
        """Apply updates to the default configuration.

        Parameters
        ----------
            updates -> dict
                Dict like object to update in the current windsor.config.Config
                instance.
        """

        for k, v in updates.items():
            if not self.is_valid_key(k):
                raise AttributeError(f'Attribute {k} not found')

            setattr(self, k, v)

    def setup(self, updates={}):
        """Setup the config class using the attributes defined in
        windsor.attributes.attributes.

        Parameters
        ----------
            updates -> dict
                Attributes to update in the current windsor.config.Config
                instance.
        """

        attr_loader.attributes.update(updates)

        self.apply_updates(attr_loader.attributes)

    def save(self, directory, updates={}):
        """Save the current config in the directory as well as update
        config attributes.

        Parameters
        ----------
            directory -> str
                Directory to store the config file.

            updates -> dict
                Attributes to update in the current config.config.Config
                instance.
        """

        self.apply_updates(updates)

        with open(os.path.join(directory, 'windsor.json'), 'w') as buf:
            buf.write(json.dumps(self.__dict__))

    def load(self, directory):
        """Loads the config from the current environment. """

        with open(os.path.join(directory, 'windsor.json')) as buf:
            c = json.load(buf)

        self.apply_updates(c)


current_config = Config()
