#!/usr/bin/env python3

import boto3
import os
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv


load_dotenv()


def upload_to_s3(local_file_path, bucket_name, s3_file_name):
    # Set your AWS credentials (make sure your AWS CLI is configured or use environment variables)
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    s3 = boto3.client('s3', 
                      aws_access_key_id=aws_access_key_id,
         	      aws_secret_access_key=aws_secret_access_key)

    try:
        # Upload the file
        s3.upload_file(local_file_path, bucket_name, s3_file_name)
        print(f"File '{local_file_path}' uploaded to '{bucket_name}/{s3_file_name}'")
    except FileNotFoundError:
        print(f"The file '{local_file_path}' was not found.")
    except NoCredentialsError:
        print("Credentials not available or incorrect.")


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 4:
        local_file_path = sys.argv[1]
        bucket_name = sys.argv[2]
        s3_file_name = sys.argv[3]

        upload_to_s3(local_file_path, bucket_name, s3_file_name)
