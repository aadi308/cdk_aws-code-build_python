# from ssl import ALERT_DESCRIPTION_BAD_CERTIFICATE_STATUS_RESPONSE
# from typing_extensions import Self
from aws_cdk import (
    # Duration,
    Stack,
    aws_codecommit as codecommit,
    pipelines as pipelines,
    aws_sqs as sqs,
)
import aws_cdk.aws_eks as eks

from constructs import Construct

class CdkEksCodebuildPythonStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        cfn_fargate_profile = eks.CfnFargateProfile(self, "MyFargateProfile",                                        
        cluster_name="aadieks",
        pod_execution_role_arn="arn:aws:iam::885300287765:role/AmazonEKSFargatePodExecutionRole-aadi",
        selectors=[eks.CfnFargateProfile.SelectorProperty(
        namespace="default",

       # the properties below are optional
    #    labels=[eks.CfnFargateProfile.LabelProperty(
    #        key="key",
    #        value="value"
    #    )]
   )],

   # the properties below are optional
   fargate_profile_name="eks_fargate",
   subnets=["subnet-0dd2f4e1d6a9254bd", "subnet-0cc9708ec93bb0156"],
  
)
        repository = codecommit.Repository.from_repository_name(
            self,
            "RepositoryFromArn",
            "eks-repo",
            )
 
        # repo = codecommit.Repository(
        #     self, "WorkshopRepo", repository_name="aadirepo"
           
        # )

        pipeline = pipelines.CodePipeline(
            self,
            "Pipeline",
            synth= pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.code_commit(repository, "master"),
                commands=[
                    "npm install -g aws-cdk",
                    "python -m pip install -r requirements.txt",
                    "pip install pytest",  # Installs the cdk cli on Codebuild
                    "pytest",  # Instructs Codebuild to install required packages
                    "cdk synth",
                ]
            ),
        )
   

