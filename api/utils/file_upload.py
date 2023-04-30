#! NB: Don't mess with this file unless you know what you're doing!

import boto3
import os
import io


def get_s3_client():
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ["S3_ACCESS_KEY"],
        aws_secret_access_key=os.environ["S3_SECRET_KEY"],
        region_name="us-east-2",
    )
    return s3_client


def upload_image(file, filename):
    client = get_s3_client()
    with file.file as f:
        client.upload_fileobj(f, os.environ["S3_BUCKET_NAME"], f"{filename}")
    url = (
        f"https://{os.environ['S3_BUCKET_NAME']}.s3.us-east-2.amazonaws.com/{filename}"
    )
    return url
