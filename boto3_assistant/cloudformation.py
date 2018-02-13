"""Functions to retrieve information about cloudformation stacks."""
import boto3

CFN = boto3.client('cloudformation')


def list_parameters(url):
    """
    Get the parameters that are defined in a cloudformation template.

    See <a href="http://boto3.readthedocs.io/en/latest/reference/services/cloudformation.html#CloudFormation.Client.get_template_summary">Cloudformation.Client.get_template_summary</a> for the response syntax.

    Parameters:
        url (str): The url to a cloudformation template in an accessible S3 bucket. 

    Return:
        parameters: A collection of objects representing parameters in the cfn stack.
    """
    summary = CFN.get_template_summary(
        TemplateURL=url
    )
    if 'Parameters' in summary:
        return summary['Parameters']
    return []
