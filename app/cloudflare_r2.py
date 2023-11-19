import boto3
import os

bucket_name = 'heartread'

account_id = '029f0106964074a4f770bec895bc9d60'
access_key = 'eb7735c096afb7255ae3f420966a2d04'
access_token = '7a843eb2e7759aebfdf147419123c443e71cd4f9ecc6af15b458ca73e88627d5'

s3 = boto3.client(
    endpoint_url = f"https://{account_id}.r2.cloudflarestorage.com",
    aws_access_key_id = access_key,
    aws_secret_access_key = access_token
)

def deleteFile(filename):
    s3.delete_object(Bucket=bucket_name, Key=filename)

def downloadFile(filename):
    s3.download_file(bucket_name, filename, filename)

def uploadFile(filename):
    s3.upload_file(bucket_name, filename, filename)
