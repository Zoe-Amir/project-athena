from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct
import aws_cdk as core
from aws_cdk import ( aws_ec2 as ec2, aws_ecs as ecs, aws_ecs_patterns as ecs_patterns)
from aws_cdk.aws_ecr_assets import DockerImageAsset

class AthenaApiStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, "AthenaVPC", max_azs=3)     # default is all AZs in region

        cluster = ecs.Cluster(self, "AthenaCluster", vpc=vpc)

        asset = DockerImageAsset(self, "AthenaApiImage", directory="backend")
        
        ecs_patterns.ApplicationLoadBalancedFargateService(self, "AthenaService",
                                                           cluster=cluster,            # Required
                                                           cpu=256,                    # Default is 256
                                                           desired_count=1,            # Default is 1
                                                           task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                                                               image=ecs.ContainerImage.from_docker_image_asset(asset)),
                                                           memory_limit_mib=512,      # Default is 512
                                                           public_load_balancer=True)  # Default is Fals
