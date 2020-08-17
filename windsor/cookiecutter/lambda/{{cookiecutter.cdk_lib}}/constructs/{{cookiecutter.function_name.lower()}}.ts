import * as cdk from '@aws-cdk/core';
import * as lambda from '@aws-cdk/aws-lambda';


class {{cookiecutter.function_name.replace('-', '')}}Function extends lambda.Function {
    constructor(scope: cdk.Construct, id: string) {
        super(scope, id, {
          code: lambda.code.fromAsset('lib/handlers/{{cookiecutter.code}}'),
          handler: '{{cookiecutter.handler}}',
          functionName: '{{cookiecutter.function_name}}',
          runtime: lambda.Runtime.{{cookiecutter.runtime}},
          {...this.getExtraConfig()}
        });
    }

    getExtraConfig() {
        return {};
    }
}

export default {{cookiecutter.function_name.replace('-', '')}}Function;
