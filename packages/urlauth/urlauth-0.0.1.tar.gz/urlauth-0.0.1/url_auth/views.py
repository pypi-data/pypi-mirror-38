from jwt import decode
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

from url_auth.settings import url_auth_settings
from url_auth.validators import JWTPayloadvalidator


def login_by_url(request):
    '''
        It will decode the jwt and redirect to
        corresponding redirect_url passed in payload
    '''
    User = get_user_model()
    encoded_jwt = request.GET.get('enc', None)
    next_url = request.GET.get('next', None)
    if callable(request.user.is_authenticated):
        is_user_authenticated = request.user.is_authenticated()
    else:
        is_user_authenticated = request.user.is_authenticated
    if not all([next_url, encoded_jwt]):
        return redirect(next_url)
    try:
        payload = decode(
            encoded_jwt,
            url_auth_settings['SECRET_KEY'],
            algorithms=url_auth_settings['ENCRYPTION_ALGORITHIM']
        )
    except Exception:
        return redirect(next_url)
    try:
        JWTPayloadvalidator(payload)()
    except Exception:
        return redirect(next_url)
    user = User.objects.get(id=payload['userid'], is_active=True)
    login(request, user)
    return redirect(payload['redirect_url'])
