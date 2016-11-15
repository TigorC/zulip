from tornado.concurrent import return_future
from tc_aws.loaders import s3_loader


@return_future
def load(context, url, callback):
    s3_loader.load(context, url, callback)
