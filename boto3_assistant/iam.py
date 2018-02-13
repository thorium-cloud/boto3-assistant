"""Functions for interacting with the IAM service."""
import json

import boto3

from boto3_assistant import account

IAM = boto3.client('iam')


def create_role(name, description):
    """
    Create a role that is assumable by the callers account.

    The role will be created with no policies.

    Parameters:
        name (str): The name of the role to create.
        description (str): The description for the role to create.

    Returns:
        role: Information about the role that is created.
    """
    basic_policy = {
        'Statement': [
            {
                'Principal': {
                    'AWS': account.get_account_id()
                },
                'Effect': 'Allow',
                'Action': ['sts:AssumeRole']
            }
        ]
    }
    response = IAM.create_role(
        Path='/',
        RoleName=name,
        AssumeRolePolicyDocument=json.dumps(basic_policy),
        Description=description
    )
    return response['Role']


def add_policy(role_name, policy_name):
    """
    Attach an IAM Policy to a Role.

    Parameters:
        role_name (str): The name of the role to attach the policy to.
        policy_name (str): The name of the policy to attach to the role.
    """
    IAM.attach_role_policy(
        RoleName=role_name,
        PolicyArn='arn:aws:iam::aws:policy/{}'.format(policy_name)
    )


def list_roles(prefix):
    """
    List all the roles for the given path prefix.

    Parameters:
        prefix (str): The prefix to filter by.
    """
    response = IAM.list_roles(
        PathPrefix=prefix
    )
    return response['Roles']


def put_role_policy(role_name, policy_name, policy):
    """
    Add or update an inline role policy document.

    Parameters:
        role_name (str): The name of the role to update.
        policy_name (str): The name of the policy to update.
        policy (obj): The policy document to update.
    """
    IAM.put_role_policy(
        RoleName=role_name,
        PolicyName=policy_name,
        PolicyDocument=json.dumps(policy)
    )
