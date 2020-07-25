class AttributeLoader:
    """Load attributes and facilitate operations on them. """

    def __init__(self):
        self.attributes = {}

    def register(self, attr, default=None):
        """Register a new attribute.

        Parameters
        ----------
            attr -> str
                Name of the attribute.

            default -> any
                Default value of the attribute. Default None
        """

        self.attributes.update({attr: default})

    def contains(self, attr):
        """Check if loader contains an attribute.

        Parameters
        ----------
            attr -> str
                Name of the attribute to check.

        Returns
        -------
            Bool indicating if attr exists or not.
        """

        return attr in self.attributes
