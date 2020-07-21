# Windsor
> Bootstrap your AWS CDK project resources by running CLI commands.

### Installing
`pip install windsor`

### How to use
Bootstrap a lambda function

`windsor generate --resource lambda-function --function-name HelloWorld --runtime PYTHON_3_7`

After the command finishes your project will have a new file located under the folder `constructs`. This file contains a construct class that can be used to build the lambda function.
