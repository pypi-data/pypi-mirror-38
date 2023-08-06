from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


USER_MODEL = get_user_model()


class JWTPayloadvalidator(object):

    def __init__(self, payload):
        self.url_expiry_datetime = payload['url_expiry_datetime']
        self.userid = payload['userid']
        self.redirect_url = payload['redirect_url']

    def _validate_url_expiry_datetime(self):
        url_expiry_datetime = datetime.strptime(
            self.url_expiry_datetime, '%Y-%m-%d %H:%M:%S.%f')
        if url_expiry_datetime < datetime.now():
            raise ValidationError('Token Expired')

    def _validagte_userid(self):
        try:
            USER_MODEL.objects.get(id=self.userid, is_active=True)
        except USER_MODEL.DoesNotExist:
            raise ValidationError('Can not find user')

    def validate(self):
        self._validate_url_expiry_datetime()
        self._validagte_userid()

    def __call__(self):
        self.validate()
