import * as cdk from '@aws-cdk/core';
import * as lambda from '@aws-cdk/aws-lambda';


export default class LambdaConstruct extends cdk.Construct {
  public function: lambda.Function;

  constructor(scope: cdk.Construct, id: string) {
    super(scope, id);

    this.function = new lambda.Function(this, '{{cookiecutter.function_name}}Function', {
      code: lambda.Code.fromAsset('lib/handlers/{{cookiecutter.function_name}}'),
      handler: 'handler.lambda_handler',
      runtime: lambda.Runtime.{{cookiecutter.runtime}}
    });
  }
}
