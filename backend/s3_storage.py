from storages.backends.s3boto3 import S3Boto3Storage


class SecureFileStorage(S3Boto3Storage):
    bucket_name = 'secure-evrak'
