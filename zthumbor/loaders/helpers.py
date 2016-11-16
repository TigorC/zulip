import os
import hmac
import time
from hashlib import sha1
from urlparse import urlparse, parse_qs
import six.moves.configparser

config_file = six.moves.configparser.RawConfigParser()
config_file.read("/etc/zulip/zulip.conf")

PRODUCTION = config_file.has_option('machine', 'deploy_type')
DEPLOY_ROOT = os.path.join(os.path.realpath(os.path.dirname(__file__)), '..', '..')

secrets_file = six.moves.configparser.RawConfigParser()
if PRODUCTION:
    secrets_file.read("/etc/zulip/zulip-secrets.conf")
else:
    secrets_file.read(os.path.join(DEPLOY_ROOT, "zproject/dev-secrets.conf"))


def get_secret(key):
    if secrets_file.has_option('secrets', key):
        return secrets_file.get('secrets', key)
    return None


def get_sign_hash(raw, key):
    hashed = hmac.new(key, raw, sha1)
    return hashed.digest().encode("base64").rstrip('\n')


def get_param_value(data, param_name):
    value = data.get(param_name, [])
    if value:
        value = value[0]
    return value or None


def sign_is_valid(url):
    data = parse_qs(urlparse(url).query)
    expired = get_param_value(data, 'expired')
    sign = get_param_value(data, 'sign')
    if not expired or not sign:
        return False
    url_path = url.rsplit('?', 1)[0]
    raw = u'{0}_{1}'.format(url_path, expired)
    if sign == get_sign_hash(raw, get_secret('thumbor_sign_key')):
        if int(expired) > time.time() or int(expired) == 0:
            return True
    return False
