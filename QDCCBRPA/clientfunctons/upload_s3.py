import boto3
from botocore.exceptions import NoCredentialsError

ACCESS_KEY = 'AKIAYUNRJAHCN56F32F4'
SECRET_KEY = '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'

def upload_to_aws_s3(local_file, bucket_name, s3_file):
    #initiate s3
    s3 = boto3.client('s3',region_name = 'us-east-2',aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    try:
        s3.upload_file(local_file,bucket_name,s3_file)
        print("upload success!")
        return True
    except:
        print("File {} didn't upload successfully.".format(local_file))
        return False

