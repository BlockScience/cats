import boto3
from cats import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

s3_client = boto3.client(
    's3',
    region_name='us-east-2',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)