import boto3
from app.config.aws_config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

sqs_client = session.client('sqs')
s3_client = session.client('s3')

