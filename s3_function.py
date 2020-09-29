import boto3
from botocore.exceptions import NoCredentialsError
import zipfile
import os

BUCKET = 's3qingdao'
def upload_to_aws_s3(local_file, bucket_name, s3_file):
    #initiate s3
    s3 = boto3.client('s3',region_name = 'cn-northwest-1')
    try:
        s3.upload_file(local_file,bucket_name,s3_file)
        print("upload success!")
        return True
    except:
        print("File {} didn't upload successfully.".format(local_file))
        return False

def get_file_by_key(file_name):
    bucket = BUCKET
    s3 = boto3.client('s3', region_name='cn-northwest-1')
    s3.download_file(bucket,file_name,file_name)

def zip_ya(start_dir):
    start_dir = start_dir  # 要压缩的文件夹路径
    file_news = start_dir + '.zip'  # 压缩后文件夹的名字

    z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)
    for dir_path, dir_names, file_names in os.walk(start_dir):
        f_path = dir_path.replace(start_dir, '')  # 这一句很重要，不replace的话，就从根目录开始复制
        f_path = f_path and f_path + os.sep or ''  # 实现当前文件夹以及包含的所有文件的压缩
        for filename in file_names:
            z.write(os.path.join(dir_path, filename), f_path + filename)
    z.close()
    return file_news

#这是上传文件
# upload_to_aws_s3('wenjian.zip',bucket_name=BUCKET,s3_file='wenjian.zip')
#这是下载文件
# upload_to_aws_s3('badge.pdf',BUCKET,'badge.pdf')