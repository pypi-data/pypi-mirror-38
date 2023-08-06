from datetime import datetime, timedelta
try:
    from urllib.parse import urlencode
except Exception:
    from urllib import urlencode
import jwt

from django.contrib.auth import get_user_model
try:
    from django.urls import reverse
except Exception:
    from django.core.urlresolvers import reverse

from url_auth.settings import url_auth_settings
from url_auth.views import login_by_url


USER_MODEL = get_user_model()


def is_typeof(obj, expected_type):
    return type(obj) == expected_type


def generate_login_url(user_instance, *args, **kwargs):
    '''
        Return Unique URL for a user which can be use to log in the user.
    '''
    redirect_url = kwargs.get('redirect_url', '/')
    expiry_time_delta = kwargs.get(
        'expiry_time_delta', url_auth_settings['EXPIRY_TIME_DELTA'])

    if not is_typeof(user_instance, USER_MODEL):
        raise TypeError('User should be of type {}'.format(str(USER_MODEL)))
    if not is_typeof(redirect_url, str):
        raise TypeError('Resirect url should be of type{}'.format('str'))
    if not is_typeof(expiry_time_delta, timedelta):
        raise TypeError('expiry_time_delta should be of type{}'.format(
            str(timedelta)))

    payload = {
        'url_expiry_datetime': str(datetime.now() + expiry_time_delta),
        'userid': user_instance.id,
        'redirect_url': redirect_url,
        'time_stamp': str(datetime.now()),
    }

    jwt_token = jwt.encode(
        payload, url_auth_settings['SECRET_KEY'],
        algorithm=url_auth_settings['ENCRYPTION_ALGORITHIM'])

    return '{}?{}'.format(
        reverse(login_by_url),
        urlencode({
            'enc': jwt_token.decode('utf-8'),
            'next': redirect_url
        })
    )
