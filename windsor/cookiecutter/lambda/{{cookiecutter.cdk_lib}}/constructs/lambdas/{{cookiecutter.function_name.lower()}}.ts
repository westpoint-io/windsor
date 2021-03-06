import * as cdk from '@aws-cdk/core';
import * as lambda from '@aws-cdk/aws-lambda';


class {{cookiecutter.construct_name}}Function extends lambda.Function {
    constructor(scope: cdk.Construct, id: string) {
        super(scope, id, {
          code: lambda.Code.fromAsset('lib/handlers/{{cookiecutter.function_name}}'),
          handler: '{{cookiecutter.handler}}',
          functionName: '{{cookiecutter.function_name}}',
          runtime: lambda.Runtime.{{cookiecutter.runtime}},
          // Put your extra configuration below
        });
    }
}

export default {{cookiecutter.function_name.replace('-', '')}}Function;
