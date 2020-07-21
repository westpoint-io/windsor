intiate a CDK environment and you can generate lambdas and test lambdas.

1. Create a bootstrap command to create a config file.
> The config file will be used to keep some options defined for the CDK and AWS resources, like lambda function runtime for instance

2. Register jinja2 template engine on cookiecutter.
3. Build code for lambdas functions for each runtime.
4. Build code for the tests of lambdas functions for each runtime.
