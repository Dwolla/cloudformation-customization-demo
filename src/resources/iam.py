from troposphere.iam import Role, Policy
from helpers import make_alphanumeric


def accelerate_configuration_policy(role_name):
    policy_name = make_alphanumeric(role_name + 'EventsInvokeLambdaPolicy')
    policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetAccelerateConfiguration",
                    "s3:GetBucketPolicy",
                    "s3:ListAllMyBuckets",
                    "s3:ListBucket",
                    "s3:PutAccelerateConfiguration"
                ],
                "Resource": [
                    "*"
                ]
            }
        ]
    }
    return Policy(
        PolicyName=policy_name,
        PolicyDocument=policy_document
    )


def lambda_base_policy(role_name):
    policy_name = make_alphanumeric(role_name + "BaseLambdaPolicy")
    policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ],
            "Resource": "*"
        }
      ]
    }
    return Policy(
        PolicyName=policy_name,
        PolicyDocument=policy_document
    )


def assume_role_policy(service):
    policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                      "Service": ["%s.amazonaws.com" % service]
                  },
                "Action": ["sts:AssumeRole"]
            }
        ]
    }
    return policy_document


class S3AccelerateProvisionerRole(Role):
    def __init__(self):
        role_name = 's3accelerateProvisionerRole'
        resource_path = '/s3accelerate/provisioner/'
        super(S3AccelerateProvisionerRole, self).__init__(
            role_name,
            Path=resource_path,
            AssumeRolePolicyDocument=assume_role_policy('lambda'),
            Policies=[
                accelerate_configuration_policy(role_name),
                lambda_base_policy(role_name)
            ]
        )
