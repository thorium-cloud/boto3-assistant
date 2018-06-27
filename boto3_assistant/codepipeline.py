
import boto3

def get_pipeline(name):
    client = boto3.client('codepipeline')
    response = client.get_pipeline(
        name=name
    )
    return response['pipeline']


def get_state(name):
    client = boto3.client('codepipeline')
    response = client.get_pipeline_state(
        name=name
    )
    state = 'Succeeded'
    for stage in response['stageStates']:
        for action in stage['actionStates']:
            this_state = action['latestExecution']['status']
            if this_state is 'Failed':
                state = this_state
            if this_state is 'InProgress':
                state = this_state
                break
        if state is 'InProgress':
            break
    return state
