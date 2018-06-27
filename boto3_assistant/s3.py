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


def empty_bucket(bucket_name):
    bucket = S3_RESOURCE.Bucket(bucket_name)
    bucket.objects.all().delete()


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
        object_summary: Details about the requested file.
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


def download_versioned_file(bucket_name, key, download_location, version):
    """Download a versioned object from an S3 bucket.

    Parameters:
        bucket_name (str): The name of the bucket to upload to.
        key (str): The key to upload to.
        download_location (str): The path to a local file to download to.
        version (str): The S3 version id of the object.
    """
    S3_CLIENT.download_file(bucket_name, key, download_location, ExtraArgs={
        'VersionId': version
    })


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


def list_files_in_bucket(bucket_name, prefix, token=None):
    """
    Returns a complete list of all the objects in the bucket, making recursive
    calls to S3 with the next continuation token.

    Parameters:
        bucket_name (str): The name of the S3 bucket
        prefix (str): The prefix to list
        token (str): The optional boto3 continuation token

    Return Type:
        list

    Returns:
        A list of s3 objects

        Syntax:
            [
                {
                    'Key': 'string',
                    'LastModified': datetime(2015, 1, 1),
                    'ETag': 'string',
                    'Size': 123,
                    'StorageClass': 'STANDARD'|'REDUCED_REDUNDANCY'|'GLACIER'|'STANDARD_IA'|'ONEZONE_IA',
                    'Owner': {
                        'DisplayName': 'string',
                        'ID': 'string'
                    }
                },
            ]
    """
    if token is not None:
        response = S3_CLIENT.list_objects_v2(
            Bucket=bucket_name,
            Prefix=prefix,
            ContinuationToken=token
        )
    else:
        response = S3_CLIENT.list_objects_v2(
            Bucket=bucket_name,
            Prefix=prefix
        )
    contents = response['Contents']
    if 'NextContinuationToken' in response:
        next_contents = list_files_in_bucket(bucket_name, prefix, response['NextContinuationToken'])
        contents = contents + next_contents
    return contents


def exists(bucket_name, prefix):
    """Determines if an object with the given prefix exists in a S3 bucket.

    Parameters:
        bucket_name (str): The name of the S3 bucket
        prefix (str): The prefix of the object to test for.

    Return Type:
        bool
    """
    found = True
    try:
        S3_RESOURCE.Object(bucket_name, prefix).load()
    except ClientError:
        found = False
    return found


def get_file_size(bucket, prefix):
    response = S3_CLIENT.head_object(Bucket=bucket, Key=prefix)
    return response['ContentLength']


def is_deleted(bucket_name, prefix):
    """Determines if the latest version of an object is a delete marker

    Parameters:
        bucket_name (str): The name of the bucket to check in.
        prefix (str): The prefix of the object to test.

    Return Type:
        bool
    """
    deleted = False

    response = S3_CLIENT.list_object_versions(
        Bucket=bucket_name,
        Prefix=prefix
    )
    if 'DeleteMarkers' in response:
        for marker in response['DeleteMarkers']:
            if marker['IsLatest']:
                deleted = True
                break
    return deleted


def get_previous_version(bucket_name, key):
    """Retrieve the previous version id of the specified key.

    Parameters:
        bucket_name (str): The name of the S3 bucket to search in.
        key (str): The key of the S3 object to get the version for.

    Return Type:
        str or None

    Returns:
        version_id (str): The version id of the previous version.
                          If there was no previous version then None
                          is returned.
    """
    response = S3_CLIENT.list_object_versions(
        Bucket=bucket_name,
        Prefix=key
    )
    version_id = None
    if 'Versions' in response:
        number_of_versions = len(response['Versions'])
        if number_of_versions > 2:
            version_id = response['Versions'][1]['VersionId']
    return version_id
