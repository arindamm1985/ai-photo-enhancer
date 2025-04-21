
import boto3
import os

s3 = boto3.client(
    's3',
    aws_access_key_id="AKIAZLWA3MJN2V2ILR7Y",
    aws_secret_access_key="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",
)
BUCKET = "ai-photo-enhancer-bucket"

def upload_file(file_path, s3_key):
    s3.upload_file(file_path, BUCKET, s3_key)

def download_file(s3_key, dest_path):
    s3.download_file(BUCKET, s3_key, dest_path)

def get_s3_url(s3_key):
    return f"https://{BUCKET}.s3.amazonaws.com/{s3_key}"
