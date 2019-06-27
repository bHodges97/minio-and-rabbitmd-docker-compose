import pytest
import boto3
import boto3.session
from s3utils import *

access_key = os.environ.get('S3_KEY')#'minio'
secret_key = os.environ.get('S3_SECRET')#'miniosecretkey'
endpoint = os.environ.get('S3_ENDPOINT')

session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        )

@pytest.fixture
def resource():
    return session.resource(
        service_name='s3',
        endpoint_url = endpoint)
