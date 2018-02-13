from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    include_package_data=True,
    name='boto3_assistant',
    packages=['boto3_assistant'],
    version='0.0.1',
    description='A collection of helper functions for working with Boto3',
    author='Connor Bray',
    author_email='connor@cbscl.co.uk',
    install_requires=required
)
