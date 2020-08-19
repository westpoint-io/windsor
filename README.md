# Windsor
> Bootstrap your AWS CDK project resources by running CLI commands.

## Getting started

### Prerequisites
To use windsor and all of its features make sure you have the following dependencies installed.

- Python >= 3.6
- npm
- [AWS CLI](https://aws.amazon.com/cli/)
- [AWS CDK](https://aws.amazon.com/cdk/)

### Installation
Install windsor using PyPI

`pip install windsor`

### Create a CDK application using windsor
Each CDK app have its own dependencies and must be in its own folder. Start by creating an empty folder in your terminal.

```
$ mkdir my-app
$ cd my-app
```

After that start your CDK application and windsor configuration simply running `windsor init`.

The command `windsor init` doesn't need to be ran in an empty folder. If you want to use windsor in a project in development `init` will identify your project and just setup its own configuration.

### Control your dependencies
Windsor can help you manage your CDK dependencies by locking the CDK version and providing commands to install and update these dependencies. The following example shows how to install the package `@aws-cdk/aws-lambda`.

`windsor install aws-lambda`

Notice that you also don't need to specify the namespace `@aws-cdk`, windsor will prefix that in all packages listed to install.

If you have packages with different versions, windsor provides a command to update all of them to the version specified in the `CDKVersion` attribute of `windsor.json` file. To update all your packages run.

`windsor lock`

### Generate resources
To speed up the development of our instrastructure at [Westpoint](https://westpoint.io), we made some ready to use templates that we can generate using windsor.

`windsor generate lambda-function --function-name HelloWorld`

The example above shows how to generate a lambda function. The only required parameter to generate lambda functions is `function-name`, since windsor will store a default runtime for them in its configuration. To change the default runtime change the attribute `DefaultRuntime` in windsor configuration file.

#### Resources available
`lambda-function`

Parameters:
 - function-name
 - runtime

`codepipeline-react`
Parameters:
 - pipeline-name
