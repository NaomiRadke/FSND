import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'fstutorial.eu.auth0.com' #'udacity-fsnd.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'coffee'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

# Valid Auth0 token from the login flow
#token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InNtY2dnem10ZTdHOWdoaDl5dS1qaCJ9.eyJpc3MiOiJodHRwczovL2ZzdHV0b3JpYWwuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYxYmM0YTVkOTE0ODhiMDA2OWYxMTlkYSIsImF1ZCI6ImNvZmZlZSIsImlhdCI6MTYzOTk5MzY1MiwiZXhwIjoxNjQwMDgwMDUyLCJhenAiOiJtT0Q3ajE2NEtKWVBnV1RsT2tMeEdrUGdhdzI4N25rTCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmRyaW5rcyIsImdldDpkcmlua3MtZGV0YWlsIl19.EX9FLiLAvDEYTtNJ5M_co3TMUP0C8DEquzVz1jDFp4tE_a4jsGwovUwoXHP_7-gUoMbmlajk_QAzCBOllkwDFGM2Pum0BU9kGqgGYAq7sLtevopYVyqwmog-p_PENkj4o1ET1PB_QJ5K4ZQ4TAnxNYTrjH08bdPZzdzDbvppOFobbmxVbFCj7fEavE3KtRLbAtZBDghxF_vPVnyv5kXn61_5OdJqcx-aLm50r4vqB_rvKFbYHWcPNEdTJ8zik2vD-YOYgYT29ITUdsFGcUzRLk3zfWXv6Q11qrey4u7zZNWlgDOtniOrQT_92MtM1YYldEJn9i8W43QVr1cMlD9csQ&expires_in=86400&token_type=Bearer'

## Auth Header
# def get_token_auth_header():
#     auth = request.headers.get('Authorization, None')
#     if not auth:
#         raise AuthError({
#             'code': 'authorization_header_missing',
#             'description': 'Authorization header is expected.'
#         }, abort(401))

#     parts = auth.split()
#     if parts[0].lower() != 'bearer':
#        raise AuthError({
#            'code': 'invalid_header',
#            'description': 'Authorization header must start with "Bearer".'
#        }, abort(401))

#     elif len(parts) == 1:
#        raise AuthError({
#            'code': 'invalid_header',
#            'description': 'Token not found.'
#        }, abort(401))

#     elif len(parts) > 2:
#        raise AuthError({
#            'code': 'invalid_header',
#            'description': 'Authorization header must be bearer token.'
#        }, abort(401))

#     token = parts[1]
#     return token

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

   
   
       # raise Exception('Not Implemented')


## Check permissions
# def check_permissions(permission, payload):
#     # Raise an AuthError if permissions are not included in the payload
#     if 'permissions' not in payload:
#         raise AuthError({
#             'code': 'invalid_claims',
#             'description': 'Permissions not included in JWT.'
#         }, 400)

#     # raise an AuthError if the requested permission string is not in the payload permissions array
#     if permission not in payload['permissions']:
#         raise AuthError({
#             'code': 'unauthorized',
#             'description': 'Permission not in payload.'
#         }, 401)
#     return True
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
def verify_decode_jwt(jwt):
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