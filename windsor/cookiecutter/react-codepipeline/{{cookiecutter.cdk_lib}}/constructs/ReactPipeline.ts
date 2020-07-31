import {
  Construct,
  RemovalPolicy,
  SecretValue
} from '@aws-cdk/core';

import {
  CorsRule,
  HttpMethods,
  Bucket,
} from '@aws-cdk/aws-s3';

import {
  PipelineProject,
  BuildSpec,
  LinuxBuildImage,
  ComputeType,
  BuildEnvironmentVariable
} from '@aws-cdk/aws-codebuild';

import {
  CloudFrontWebDistribution,
  HttpVersion,
  PriceClass
} from '@aws-cdk/aws-cloudfront';

import {
  Pipeline, Artifact
} from '@aws-cdk/aws-codepipeline';

import {
  GitHubSourceAction,
  CodeBuildAction,
  S3DeployAction
} from '@aws-cdk/aws-codepipeline-actions';

import {
  RecordSet,
  IHostedZone,
  RecordType,
  RecordTarget
} from '@aws-cdk/aws-route53';

import { CloudFrontTarget } from '@aws-cdk/aws-route53-targets';

import { Role, PolicyStatement, Effect, CompositePrincipal, ServicePrincipal } from '@aws-cdk/aws-iam';


interface ICustomAliasConfiguration {
  names: string[],
  acmCertRef: string
}

interface IReactPipelineRepositoryProps {
  repo: string,
  branch: string,
  owner: string,
  oauthToken: string
}

interface IReactPipelineProps {
  DeploymentBucket: Bucket,
  ResourcePrefix: string,
  Repository: IReactPipelineRepositoryProps,
  HostedZone?: IHostedZone,
  CertificateArn?: string,
  CloudFrontAlias?: string,
  Environment?: { [name: string]: BuildEnvironmentVariable },
  Prefix?: string
}

export default class ReactPipeline extends Construct {
  constructor(scope: Construct, id: string, props: IReactPipelineProps) {
    super(scope, id);

    const corsRule: CorsRule = {
      allowedOrigins: ['*'],
      allowedMethods: [HttpMethods.GET]
    };

    const resourcePrefix: string = props.Prefix || '';

    const bucketName: string = `${resourcePrefix.toLowerCase()}-{{cookiecutter.pipeline_name}}-bucket`;
    const bucket: Bucket = new Bucket(this, 'ReactAppBucket', {
      bucketName: bucketName,
      websiteIndexDocument: 'index.html',
      publicReadAccess: true,
      cors: [corsRule],
      removalPolicy: RemovalPolicy.DESTROY
    });

    let cloudFrontDistributionAliasConfig: ICustomAliasConfiguration = {
      names: [],
      acmCertRef: ''
    }

    if (props.CloudFrontAlias) {
      cloudFrontDistributionAliasConfig.names = [props.CloudFrontAlias];
    }

    if (props.CertificateArn) {
      cloudFrontDistributionAliasConfig.acmCertRef = props.CertificateArn;
    }

    const cloudFrontDistribution: CloudFrontWebDistribution = new CloudFrontWebDistribution(this, 'CloudFront', {
      originConfigs: [
        {
          s3OriginSource: {
            s3BucketSource: bucket
          },
          behaviors: [{
            isDefaultBehavior: true
          }]
        }
      ],
      defaultRootObject: 'index.html',
      httpVersion: HttpVersion.HTTP2,
      priceClass: PriceClass.PRICE_CLASS_ALL,
      errorConfigurations: [
        {
          errorCode: 404,
          responseCode: 200,
          responsePagePath: '/index.html'
        },
        {
          errorCode: 403,
          responseCode: 200,
          responsePagePath: '/index.html'
        }
      ],
      aliasConfiguration: cloudFrontDistributionAliasConfig
    });

    if (props.HostedZone) {
      new RecordSet(this, 'ReactAppRecordSet', {
        recordType: RecordType.A,
        target: RecordTarget.fromAlias(new CloudFrontTarget(cloudFrontDistribution)),
        zone: props.HostedZone,
        recordName: props.CloudFrontAlias
      });
    }

    const CodeBuildRole: Role = new Role(this, 'CodeBuildRole', {
      assumedBy: new ServicePrincipal('codebuild.amazonaws.com')
    });

    CodeBuildRole.addToPolicy(new PolicyStatement({
      effect: Effect.ALLOW,
      actions: [
        'logs:CreateLogGroup',
        'logs:CreateLogStream',
        'logs:PutLogEvents',
        's3:*',
        'cognito-idp:UpdateUserPoolClient'
      ],
      resources: ['*']
    }))

    const CodeBuild: PipelineProject = new PipelineProject(this, 'ReactAppCodeBuildProject', {
      buildSpec: BuildSpec.fromSourceFilename('buildspec.yaml'),
      role: CodeBuildRole,
      environment: {
        buildImage: LinuxBuildImage.STANDARD_2_0,
        computeType: ComputeType.SMALL,
        privileged: true,
        environmentVariables: props.Environment
      }
    });

    const PipelineRole: Role = new Role(this, 'ReactAppPipelineRole', {
      assumedBy: new CompositePrincipal(
        new ServicePrincipal('codepipeline.amazonaws.com'),
        new ServicePrincipal('cloudformation.amazonaws.com')
      ),
      path: '/'
    });

    PipelineRole.addToPolicy(new PolicyStatement({
      effect: Effect.ALLOW,
      actions: [
        'codebuild:BatchGetBuilds',
        'codebuild:StartBuild',
        'iam:PassRole',
        'cloudwatch:*',
        's3:CreateBucket',
        's3:GetBucketPolicy',
        's3:GetObject',
        's3:ListAllMyBuckets',
        's3:ListBucket',
        's3:PutBucketPolicy',
        'codepipeline:*'
      ],
      resources: ['*']
    }));

    const CodepipelineName: string = `${resourcePrefix}{{cookiecutter.pipeline_name}}`;
    const repo: IReactPipelineRepositoryProps = props.Repository;
    const sourceOutput = new Artifact('SourceArtifact');
    const buildOutput = new Artifact('BuildArtifact');
    new Pipeline(this, 'ReactAppPipeline', {
      pipelineName: CodepipelineName,
      role: PipelineRole,
      artifactBucket: props.DeploymentBucket,
      stages: [
        {
          stageName: 'SourceAction',
          actions: [
            new GitHubSourceAction({
              actionName: 'GithubWebhook',
              repo: repo.repo,
              owner: repo.owner,
              branch: repo.branch,
              oauthToken: new SecretValue(repo.oauthToken),
              output: sourceOutput,
              runOrder: 1
            }),
          ]
        },
        {
          stageName: 'Build',
          actions: [
            new CodeBuildAction({
              actionName: 'Build',
              project: CodeBuild,
              input: sourceOutput,
              outputs: [buildOutput],
              runOrder: 1
            })
          ]
        },
        {
          stageName: 'Deploy',
          actions: [
            new S3DeployAction({
              actionName: 'ReactAppDeploy',
              input: buildOutput,
              bucket: props.DeploymentBucket
            })
          ]
        }
      ]
    });
  }
}