import json

import boto3

from python_basic_utils.logging.interceptors import trace


@trace
def call_lambda(name, body):
    client = boto3.client('lambda')
    client.invoke(
        FunctionName=name,
        InvocationType='Event',
        LogType='None',
        Payload=json.dumps(body)
    )


@trace
def call_lambda_sync(name, body):
    client = boto3.client('lambda')
    response = client.invoke(
        FunctionName=name,
        InvocationType='RequestResponse',
        LogType='None',
        Payload=json.dumps(body)
    )
    if 'Payload' in response:
        try:
            return json.loads(response['Payload'].read())
        except ValueError:
            return response['Payload'].read()
    return response
