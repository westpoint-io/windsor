from windsor.loader import AttributeLoader

import windsor.services.lambda_.attributes as lambda_attrs


attr_loader = AttributeLoader()

attr_loader.register(lambda_attrs.DEFAULT_RUNTIME, 'PYTHON_3_7')
