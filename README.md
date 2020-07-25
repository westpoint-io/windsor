# Windsor
> Bootstrap your AWS CDK project resources by running CLI commands.

## Installing
`pip install windsor`

## How to use
Initialize `windsor` by running the following command

`windsor init`

`init` will create a windsor configuration file inside the current folder. If a CDK project is not found `windsor` will create one.

After `windsor` is initialized, you can generate a lambda function by running.

`windsor generate lambda-function --function-name HelloWorld`

Inside the `windsor.json` there is parameter called `lambda-function-default-runtime`. This parameters sets the default lambda runtime to `PYTHON_3_7`, if you want to change this value use the parameter `--runtime` when running `windsor generate lambda-function`. The allowed values are:

`PYTHON_3_7`

`NODEJS_10_X`

After the command finishes your project will have a new file located under the folder `constructs`. This file contains a construct class that can be used to build the lambda function.

Windsor can manage CDK package versions by keeping they locked to the same version as `@aws-cdk/core`. Run the command
`windsor lock` to verify all CDK packages and check their versions, if any package have a different version than CDK core windsor will reinstall it using a compatible version.

To install packages using always the same version, use command `windsor install [package1] [package2]`.

## Available resources
`lambda-function`

Built by [Westpoint](https://westpoint.io)
