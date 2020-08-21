import * as cdk from '@aws-cdk/core';
import * as codepipeline from '@aws-cdk/aws-codepipeline';
import * as codebuild from '@aws-cdk/aws-codebuild';
import * as s3 from '@aws-cdk/aws-s3';
import * as codepipelineactions from '@aws-cdk/aws-codepipeline-actions';


interface IReactPipelineProps {
    owner: string,
    repo: string
    oauthToken: string,
    branch?: string
}


class ReactPipeline extends cdk.Construct {
    constructor(scope: cdk.Construct, id: string, props: IReactPipelineProps) {
        super(scope, id);

        const websiteBucket: s3.Bucket = new s3.Bucket(this, 'WebsiteBucket', {
            websiteIndexDocument: 'index.html',
            websiteErrorDocument: 'index.html',
            publicReadAccess: true
        });

        const sourceOutput: codepipeline.Artifact = new codepipeline.Artifact('SourceArtifact');
        const buildOutput: codepipeline.Artifact = new codepipeline.Artifact('BuildArtifact');

        const pipeline: codepipeline.Pipeline = new codepipeline.Pipeline(this, 'Pipeline', {
            pipelineName: '{{cookiecutter.pipeline_name}}',
            restartExecutionOnUpdate: true
        });

        pipeline.addStage({
            stageName: 'Source',
            actions: [
                new codepipelineactions.GitHubSourceAction({
                    actionName: 'GithubSource',
                    owner: props.owner,
                    repo: props.repo,
                    branch: props.branch || 'master',
                    oauthToken: new cdk.SecretValue(props.oauthToken),
                    output: sourceOutput
                })
            ]
        });

        pipeline.addStage({
            stageName: 'Build',
            actions: [
                new codepipelineactions.CodeBuildAction({
                    actionName: 'BuildApp',
                    project: new codebuild.PipelineProject(this, 'AppCodebuild', {
                        projectName: '{{cookiecutter.pipeline_name}}CodeBuildProject',
                        buildSpec: codebuild.BuildSpec.fromSourceFilename('buildspec.yaml')
                    }),
                    input: sourceOutput,
                    outputs: [buildOutput]
                })
            ]
        });

        pipeline.addStage({
            stageName: 'Deploy',
            actions: [
                new codepipelineactions.S3DeployAction({
                    actionName: 'DeployApp',
                    input: buildOutput,
                    bucket: websiteBucket
                })
            ]
        });
    }
}

export default ReactPipeline;
