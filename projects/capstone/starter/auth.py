import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'fstutorial.eu.auth0.com' 
ALGORITHMS = ['RS256']
API_AUDIENCE = 'capstone_image'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code



def get_token_auth_header():
    if "Authorization" in request.headers:
        auth_header = request.headers["Authorization"]
        if auth_header:
            bearer_token_array = auth_header.split(' ')
            if bearer_token_array[0] and bearer_token_array[0].lower() == "bearer" and bearer_token_array[1]:
                return bearer_token_array[1]
    raise AuthError({
        'success': False,
        'message': 'JWT not found',
        'error': 401
    }, 401)

   
   
def check_permissions(permission, payload):
    if "permissions" in payload:
        if permission in payload['permissions']:
            return True
    raise AuthError({
        'success': False,
        'message': 'Permission not found in JWT',
        'error': 401
    }, 401)

    
## Verify JWT
def verify_decode_jwt(token):
    # Get the publik key from authO
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.load(jsonurl.read())

    # Get the data in the header
    unverified_header = jwt.get_unverified_header(token)

    # Choose our key
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)
    
    for key in jwks['key']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    # Finally, verify
    if rsa_key:
        try:
            # Use the key t validate the jwt
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

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)



def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
    
            jwt = get_token_auth_header()
            try:
                # check if token is valid
                payload = verify_decode_jwt(jwt)
            except:
                raise AuthError({
                    'code': 'invalid token.'
                }, 401)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator