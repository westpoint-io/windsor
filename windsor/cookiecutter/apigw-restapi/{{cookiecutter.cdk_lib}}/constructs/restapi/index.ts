import * as cdk from '@aws-cdk/core';
import * as apigw from '@aws-cdk/aws-apigateway';


class RestApi extends apigw.RestApi {
  constructor(scope: cdk.Construct, id: string) {
    super(scope, id);
  }
}

export default RestApi;
