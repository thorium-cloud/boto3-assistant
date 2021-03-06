"""Functions to retrieve information about cloudformation stacks."""
import boto3


def list_parameters(url):
    """
    Get the parameters that are defined in a cloudformation template.

    Parameters:
        url (str): The url to a cfn template in an accessible S3 bucket.

    Return:
        parameters: A collection parameters in the cfn stack.
    """
    cfn = boto3.client('cloudformation')
    summary = cfn.get_template_summary(
        TemplateURL=url
    )
    if 'Parameters' in summary:
        return summary['Parameters']
    return []
