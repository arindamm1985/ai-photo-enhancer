
import boto3
import os

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)
BUCKET = "ai-photo-enhancer-bucket"

def upload_file(file_path, s3_key):
    s3.upload_file(file_path, BUCKET, s3_key)

def download_file(s3_key, dest_path):
    s3.download_file(BUCKET, s3_key, dest_path)

def get_s3_url(s3_key):
    return f"https://{BUCKET}.s3.amazonaws.com/{s3_key}"
