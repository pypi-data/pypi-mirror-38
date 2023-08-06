"""
Administration of Amazon S3 Resources through a boto3 client.
"""


def download_artifact(resource, bucket, key='alppbBuilder/alppb.zip',
                      local_path='alppb.zip'):
    """
    Fetches the artifact from Amazon S3 built by alppb .

    Parameters
    ----------
    resource : boto3.resources.factory.s3.ServiceResource
        A boto3 Resource interface for S3.
    bucket : str
        Name of the bucket the artifact exists in.
    key: str
        The S3 key of the artifact to download from the bucket. Defaults to
        "alppbBuilder/alppb.zip".
    local_path: str
        The local path where the artifact will be downloaded. Defaults to the
        current directory alppb is being run from.

    Returns
    -------
    """
    print("Downloading built package(s) to {}...".format(local_path))
    resource.meta.client.download_file(bucket, key, local_path)
    print("Download complete...")


def delete_artifact(client, bucket, key='alppbBuilder/alppb.zip'):
    """
    Deletes the artifact from Amazon S3 built by alppb.

    Parameters
    ----------
    client : botocore.client.S3
        A boto3 client for S3.
    bucket : str
        Name of the bucket the artifact exists in.
    key: str
        The S3 key of the artifact to delete from the bucket. Defaults to
        "alppbBuilder/alppb.zip".

    Returns
    -------
    """
    print("Deleting {} from S3 bucket {}...".format(key, bucket))
    client.delete_object(Bucket=bucket, Key=key)


def bucket_region(client, bucket):
    """
    Gets the region where this bucket exists.

    Parameters
    ----------
    client : botocore.client.S3
        A boto3 client for S3.

    Returns
    -------
    str
        Region of the bucket.
    """
    response = client.get_bucket_location(Bucket=bucket)
    location = response.get('LocationConstraint')
    if location is None:
        return 'us-east-1'
    return str(location)
