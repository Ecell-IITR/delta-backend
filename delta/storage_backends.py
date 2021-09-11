from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    location = 'delta/media'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False