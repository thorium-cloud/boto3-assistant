"""Functions to retrieve information about the callers account."""
import boto3

IAM = boto3.client('iam')


def get_region():
    """
    Get the current region.

    Return:
        region: The region.
    """
    region = boto3.session.Session().region_name
    return region


def get_account_id():
    """
    Get the users account id.

    Return:
        account_id: The callers AWS account id.
    """
    sts = boto3.client('sts')
    account_id = sts.get_caller_identity().get('Account')
    return account_id


def get_alias():
    """
    Get the users account alias.

    Return:
        alias: The first known account alias.
    """
    aliases = IAM.list_account_aliases()
    if aliases and aliases['AccountAliases']:
        return aliases['AccountAliases'][0]
