import boto3
from botocore.exceptions import BotoCoreError, ClientError
from app.config.aws_config import AWS_REGION, S3_BUCKET
from app.services.aws_clients import s3_client

def upload_file_to_s3(file_obj, filename):
    """
    Uploads a file object to the configured S3 bucket.

    Args:
        file_obj: File-like object from Flask (e.g., request.files['file'])
        filename: Name to save the file as in the bucket

    Returns:
        str: Public URL of uploaded file

    Raises:
        Exception: If upload fails
    """
    try:
        s3_client.upload_fileobj(
            file_obj,
            S3_BUCKET,
            f"uploads/{filename}"
        )
        file_url = f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/uploads/{filename}"

        return file_url

    except (BotoCoreError, ClientError) as e:
        # Log the error if needed
        raise Exception(f"S3 upload failed: {str(e)}")


def download_file_from_s3(filename):
    file_obj = BytesIO()
    s3_client.download_fileobj(S3_BUCKET, filename, file_obj)
    file_obj.seek(0)
    return file_obj