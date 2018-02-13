from boto3_assistant import world


def test_world():
    response = world.invoke({}, {})
    assert response == "Hello World"
