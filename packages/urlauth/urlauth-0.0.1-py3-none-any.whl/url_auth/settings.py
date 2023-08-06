from datetime import timedelta
from django.conf import settings


USER_SETTINGS = getattr(settings, 'URL_AUTH_CONFIG', None)

DEFAULTS = {
    'SECRET_KEY': settings.SECRET_KEY,
    'EXPIRY_TIME_DELTA': timedelta(days=7),
    'ENCRYPTION_ALGORITHIM': 'HS256'
}

url_auth_settings = dict(
    DEFAULTS, **USER_SETTINGS) if USER_SETTINGS else DEFAULTS
