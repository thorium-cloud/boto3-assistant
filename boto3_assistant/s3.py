import boto3

S3_RESOURCE = boto3.resource('s3')
S3_CLIENT = boto3.client('s3')


def create_bucket(name, region):
    """
    Create a private versioned S3 bucket in the specified region.

    Parameters:
        name (str): The name of the S3 bucket to create.
        region (str): The name of the region to create the bucket in.
    """
    bucket = S3_RESOURCE.Bucket(name)
    bucket.create(
        ACL='private',
        CreateBucketConfiguration={
            'LocationConstraint': region
        }
    )
    bucket.Versioning().enable()


def delete_bucket(name):
    """
    Empty an S3 bucket and delete it.

    Parameters:
        name (str): The name of the S3 bucket to delete.
    """
    bucket = S3_RESOURCE.Bucket(name)
    bucket.objects.all().delete()
    bucket.delete()


def get_sub_folders(name, prefix):
    """
    Get what would usually be considered sub folders of an S3 prefix.

    Parameters:
        name (str): The name of the S3 bucket.
        prefix (str): The S3 prefix to search under.
    """
    sub_folders = []
    bucket = S3_RESOURCE.Bucket(name=name)
    for obj in bucket.objects.filter(Prefix=prefix):
        parts = obj.key.split("/")
        parts.pop(-1)
        folder = '/'.join(str(part) for part in parts)
        sub_folders.append(folder)
    return sub_folders


def delete_folder(name, prefix):
    """
    Delete all objects under a given prefix.

    Parameters:
        name (str): The name of the S3 bucket.
        prefix (str): The root prefix to delete objects under.
    """
    objects_to_delete = S3_RESOURCE.meta.client.list_objects(Bucket=name, Prefix=prefix)
    delete_keys = {'Objects': []}
    delete_keys['Objects'] = [{'Key': k} for k in [obj['Key'] for obj in objects_to_delete.get('Contents', [])]]
    if delete_keys['Objects']:
        print("Deleting keys: {}".format(delete_keys))
        S3_RESOURCE.meta.client.delete_objects(Bucket=name, Delete=delete_keys)


def get_file(name, prefix):
    """
    Get the S3 Object Summary for the given prefix.

    Parameters:
        name (str): The name of the S3 bucket.
        prefix (str): The prefix of the file to get the summary for.

    Returns:
        object_summary: See <a href="http://boto3.readthedocs.io/en/latest/reference/services/s3.html#objectsummary">S3.ObjectSummary</a>
    """
    bucket = S3_RESOURCE.Bucket(name)
    response = bucket.objects.filter(
        Prefix=prefix
    )
    return response


def download_file(name, prefix, download_location):
    """
    Download a file from S3 to a local directory.

    Parameters:
        name (str): The name of the S3 bucket.
        prefix (str): The prefix of the file to download.
        download_location (str): The path to the place to download the file to.
    """
    S3_CLIENT.download_file(name, prefix, download_location)


def upload_file(name, prefix, file_path):
    """
    Upload a file from a local directory to an S3 bucket.

    Parameters:
        name (str): The name of the S3 bucket.
        prefix (str): The prefix to upload the file to.
        file_path (str): The path to the file to upload to S3.
    """
    obj = S3_RESOURCE.Object(name, prefix)
    obj.upload_file(file_path)


def list_all_buckets():
    """
    Get a list of all the buckets you have access to see.

    Return:
        buckets: A list of all the buckets.
    """
    all_buckets = S3_CLIENT.list_buckets()
    return all_buckets['Buckets']
