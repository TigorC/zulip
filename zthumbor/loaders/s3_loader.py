from six.moves import urllib
from tornado.concurrent import return_future
from thumbor.loaders import LoaderResult
from tc_aws.loaders import s3_loader
from . import helpers


@return_future
def load(context, url, callback):
    url = urllib.parse.unquote(url)
    if not helpers.sign_is_valid(url):
        result = LoaderResult()
        result.error = LoaderResult.ERROR_NOT_FOUND
        result.successful = False
        callback(result)
        return
    if not helpers.is_external_url(url):
        url = urllib.parse.urlsplit(url).path
    s3_loader.load(context, url, callback)
