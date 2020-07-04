import json
from functools import wraps
from flask import request, _request_ctx_stack
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'coffee-shop-api.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'warehouse_shipment_website'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization Header is missing.'
            }, 401)
    auth_sections = auth.split()

    if len(auth_sections) != 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header does not contain all required parts'
        }, 401)

    if auth_sections[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    jwt_token = auth_sections[1]
    return jwt_token


def check_permissions(permission, payload):
    if "permissions" not in payload:
        raise AuthError({
            'code': 'missing_permissions',
            'description': 'permissions is not included in payload'
        }, 401)
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'permission_denied',
            'description': 'given permission is not included in permissions'
        }, 401)
    return True



def verify_decode_jwt(token):
    authorize_token = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    json_header = json.loads(authorize_token.read())
    unverified_header = jwt.get_unverified_header(token)

    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    rsa_key = {}
    for key in json_header['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)


    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
                }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
    