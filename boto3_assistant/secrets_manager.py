import boto3


def get(self, id):
    """
        Returns the string value of the stored secret.

        Parameters:
            id: The id of the secret stored in AWS Secrets Manager.

        Returns: The string value of the secret.
    """
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(
        SecretId=id
    )
    if response and 'SecretString' in response:
        return response['SecretString']
    else:
        return None
