import logging
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from django.conf import settings
from django.utils.text import get_valid_filename
from celery import shared_task

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME,
)

#upload a file
def file_upload(file_obj, user_id):
    """
    Django-compatible S3 file upload
    """
    filename = get_valid_filename(file_obj.name)
    s3_key = f"documents/{user_id}_{filename}"

    try:
        s3_client.upload_fileobj(
            file_obj,
            settings.AWS_STORAGE_BUCKET_NAME,
            s3_key,
            ExtraArgs={"ContentType": file_obj.content_type},
        )

        file_url = f"https://{settings.CLOUDFRONT_DOMAIN}/{s3_key}"
        return {"success": True, "url": file_url}

    except (NoCredentialsError, PartialCredentialsError):
        logging.error("AWS credentials error")
        return {"success": False, "error": "AWS credentials error"}

    except Exception as e:
        logging.error(f"Upload failed: {e}")
        return {"success": False, "error": str(e)}

#upload multiple files
@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={"max_retries": 3})
def upload_multiple_files(self, files, user_id):
    results = []

    for file in files:
        response = file_upload(file, user_id)
        results.append(response)

    return results