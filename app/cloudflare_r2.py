import boto3
import os

bucket_name = 'heartread'

with open('/run/secrets/CLOUDFLARE_ID', 'r') as cloudflare_id:
    account_id = cloudflare_id.read().strip()

with open('/run/secrets/CLOUDFLARE_ACCESS_KEY', 'r') as cloudflare_access_key:
    access_key = cloudflare_access_key.read().strip()

with open('/run/secrets/CLOUDFLARE_ACCESS_TOKEN', 'r') as cloudflare_access_token:
    access_token = cloudflare_access_token.read().strip()

s3 = boto3.client(
    endpoint_url: f"https://{account_id}.r2.cloudflarestorage.com",
    aws_access_key_id = access_key
    aws_secret_access_key = access_token
)

def deleteFile(filename):
    s3.delete_object(Bucket=bucket_name, Key=filename)

def downloadFile(filename):
    s3.download_file(bucket_name, filename, filename)

def uploadFile(filename):
    s3.upload_file(bucket_name, filename, filename)
