"""
Administration of AWS IAM Resources through a boto3 client.
"""
import json
import time


def create_role(client, bucket):
    """
    Creates an IAM Role to use with AWS CodeBuild

    Parameters
    ----------
    client : botocore.client.iam
        A boto3 client for IAM.

    bucket : str
        Name of an existing S3 bucket.

    Returns
    -------
    str
        ARN of the newly created IAM Role.
    """
    print("Creating IAM Role...")
    try:
        response = client.create_role(
            RoleName='alppbBuilderRole',
            AssumeRolePolicyDocument=json.dumps({
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {
                            "Service": "codebuild.amazonaws.com"
                        },
                        "Action": "sts:AssumeRole"
                    }
                ]
            }),
            Description="This role is used by "
                        "https://github.com/irlrobot/alppb",
        )
    except client.exceptions.EntityAlreadyExistsException:
        print(">>alppbBuilderRole already exists, skipping...")
        response = client.get_role(RoleName='alppbBuilderRole')

    add_role_policy(client, bucket)

    # TODO be smarter about checking if the role is ready
    print(">>Waiting for policy propagation before continuing...")
    time.sleep(12)

    return str(response.get('Role').get('Arn'))


def generate_role_policy(bucket):
    """
    Generates a valid IAM Role policy from a template. The template requires
    the name of an existing S3 bucket.

    Parameters
    ----------
    bucket : str
        Name of an existing S3 bucket.

    Returns
    -------
    str
        The IAM Policy document in JSON.
    """
    return json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "CloudWatchLogsPolicy",
                "Effect": "Allow",
                "Action": [
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ],
                "Resource": [
                    "*"
                ]
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:ListBucket"
                ],
                "Resource": [
                    "arn:aws:s3:::{}".format(bucket)
                ]
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:PutObject",
                    "s3:GetObject",
                    "s3:DeleteObject"
                ],
                "Resource": [
                    "arn:aws:s3:::{}/*".format(bucket)
                ]
            }
        ]
    })


def add_role_policy(client, bucket):
    """
    Adds an IAM Policy to a newly created IAM Role from iam.create_role().

    Parameters
    ----------
    client : botocore.client.iam
        A boto3 client for IAM.

    bucket : str
        Name of an existing S3 bucket.

    Returns
    -------
    """
    print(">>Attaching Policy to the the IAM Role...")
    client.put_role_policy(
        RoleName='alppbBuilderRole',
        PolicyName='alppbBuilderPolicy',
        PolicyDocument=generate_role_policy(bucket),
    )


def delete_role(client):
    """
    Deletes an IAM Role created from iam.create_role().

    Parameters
    ----------
    client : botocore.client.iam
        A boto3 client for IAM.

    Returns
    -------
    """
    print("Deleting IAM Role...")
    # AWS API wants all role policies deleted before the role itself.
    # TODO get all policies on the role and then delete in case it was modified
    client.delete_role_policy(
        RoleName='alppbBuilderRole',
        PolicyName='alppbBuilderPolicy'
    )
    client.delete_role(RoleName='alppbBuilderRole')
