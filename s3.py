import boto3
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

AWS_ACCESS = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET = os.environ.get('AWS_SECRET_KEY')
AWS_REGION = os.environ.get('AWS_REGION')
AWS_BUCKET = os.environ.get('AWS_BUCKET_NAME')

s3 = boto3.client('s3',
                  AWS_REGION,
                  aws_access_key_id=AWS_ACCESS,
                  aws_secret_access_key=AWS_SECRET)

def upload_file_to_s3(file_name):
    """uploads a file to AWS. saves file name to database(TODO)"""

    object_name = str(uuid.uuid4())
    print(object_name)
    print(AWS_BUCKET)
    s3.upload_file(file_name, AWS_BUCKET, object_name)
    return object_name

def download_file_from_s3(object_name, file_extension):
    """downloads file by object name. return path to that file"""

    s3.download_file(AWS_BUCKET, object_name, f'downloads/{object_name}.{file_extension}')

# upload_file("uploads/cat.jpg")
# download_file_from_s3("531c09ff-5289-4abb-acb1-d971d137f2de")
