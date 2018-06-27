import boto3


def list_all_repos(token=None):
    client = boto3.client('codecommit')
    if token is None:
        response = client.list_repositories(
            sortBy='repositoryName',
            order='ascending'
        )
    else:
        response = client.list_repositories(
            sortBy='repositoryName',
            order='ascending',
            nextToken=token
        )
    if 'nextToken' in response:
        response['repositories'] += list_all_repos(token=response['nextToken'])
    return response['repositories']


def get_branches(repo_name, token=None):
    client = boto3.client('codecommit')
    if token is None:
        response = client.list_branches(
            repositoryName=repo_name
        )
    else:
        response = client.list_branches(
            repositoryName=repo_name,
            nextToken=token
        )
    if 'nextToken' in response:
        response['branches'] += get_branches(repo_name, token=response['nextToken'])
    return response['branches']


def get_repo(repo_name):
    client = boto3.client('codecommit')
    response = client.get_repository(
        repositoryName=repo_name
    )
    return response['repositoryMetadata']