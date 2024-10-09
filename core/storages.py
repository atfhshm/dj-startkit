from storages.backends.s3boto3 import S3Boto3Storage


class StaticS3Storage(S3Boto3Storage):
    location = "static"


class UploadS3Storage(S3Boto3Storage):
    location = "uploads"
