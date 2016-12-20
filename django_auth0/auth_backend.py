# -*- coding: utf-8 -*-
import jwt
import base64
import json
from functools import wraps

from django.http import HttpResponse
from django.utils.decorators import available_attrs

from .utils import get_config

# UserModel = get_user_model()

# user profile keys that are always present as specified by
# https://auth0.com/docs/user-profile/normalized#normalized-user-profile-schema
AUTH0_USER_INFO_KEYS = [
    'name',
    'nickname',
    'picture',
    'user_id',
]

class AuthError(Exception):
    def __init__(self, payload, status_code):
        payload = json.dumps(payload)
        super().__init__("Authentication error. Details: {}".format(payload))
        self.payload = payload
        self.status_code = status_code

    def to_http_response(self):
        return HttpResponse(self.payload, status=self.status_code)


def login_required(function=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            try:
                request.user = authenticate(request)
                return view_func(request, *args, **kwargs)
            except AuthError as error_respose:
                print("###error! {}".format(error_respose))
                return error_respose.to_http_response()
        return _wrapped_view
    return decorator(function)


def authenticate(request):
    """
    Auth0 return a dict which contains the following fields
    :param kwargs: user information provided by auth0
    :return: user
    """
    is_auth0 = True


    auth = request.META.get('HTTP_AUTHORIZATION', None)
    if not auth:
        print("THIS IS AUTH: {}".format(auth))
        raise authentication_error({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'})
    parts = auth.split()
    config = get_config()

    if parts[0].lower() != 'bearer':
        raise authentication_error({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'})
    elif len(parts) == 1:
        raise authentication_error({'code': 'invalid_header', 'description': 'Token not found'})
    elif len(parts) > 2:
        raise authentication_error({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'})

    token = parts[1]

    try:
        user = jwt.decode(
            token,
            base64.b64decode(config['AUTH0_SECRET'].replace("_","/").replace("-","+")),
            audience=config['AUTH0_CLIENT_ID']
        )
    except jwt.ExpiredSignature:
        raise authentication_error({'code': 'token_expired', 'description': 'token is expired'})
    except jwt.InvalidAudienceError:
        raise authentication_error(
            {'code': 'invalid_audience', 'description': 'incorrect audience, expected:'+config['AUTH0_CLIENT_ID']})
    except jwt.DecodeError:
        raise authentication_error({'code': 'token_invalid_s signature', 'description': 'token signature is invalid'})
    """
    # check that each auth0 key is present in kwargs
    for key in AUTH0_USER_INFO_KEYS:
        if key not in kwargs:
            is_auth0 = False
            break

    # End the authentication attempt if this is not an auth0 payload
    if is_auth0 is False:
        return None

    user_id = kwargs.get('user_id')

    if user_id is None:
        raise ValueError(_('user_id can\'t be blank!'))

    # The format of user_id is
    #    {identity provider id}|{unique id in the provider}
    # The pipe character is invalid for the django username field
    # The solution is to replace the pipe with a dash
    username = user_id.replace('|', '-')

    try:
        user = UserModel.objects.get(username__iexact=username)
    except UserModel.DoesNotExist:
        user = UserModel.objects.create(username=username)
    """
    return user

# Authentication attribute/annotation
def authentication_error(error):
    return AuthError(payload=error, status_code=401)
