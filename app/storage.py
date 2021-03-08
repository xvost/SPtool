import boto3
from botocore.exceptions import ClientError


class Storage:
    def __init__(self, keyid=None, key=None, bucket=None):
        self.statickeyid = keyid
        self.statickey = key
        self.service = 's3'
        self.region = 'ru-central1'
        self.endpoint = 'storage.yandexcloud.net'
        self.bucket = bucket

    def putfile(self, filepath, filename):
        session = boto3.Session(
            aws_access_key_id=self.statickeyid,
            aws_secret_access_key=self.statickey,
        )
        try:
            response = session.client('s3',
                                      endpoint_url=f'https://{self.bucket}.{self.endpoint}')\
                .upload_file(filepath, self.bucket, filename)
        except ClientError as e:
            return e
        return {'url': f'https://{self.bucket}.{self.endpoint}/{filename}'}
