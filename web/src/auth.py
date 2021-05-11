from flask import redirect, request, url_for
from google.auth.transport import requests
from google.oauth2 import id_token
from werkzeug.wrappers import Request

from functools import wraps

GOOGLE_AUTH_REQUEST_ADAPTER = requests.Request()

class AuthMiddleware():
    '''
    Middleware responsible for authentication.
    OAuth2 is expect to be provided in @token cookie.
    If it's valid user informations are appended to request context, otherwise they are set to None.
    NOTE: Further, it can be validated whether user is authenticated by veryifing if environ['user'] is not None.
    '''

    '''
    List of fields to get from user's data
    '''
    USER_INFO_FIELDS = [
        'email',
        'picture',
        'name',
        'given_name'
    ]

    def __init__(self, app):
        self.app = app
        self.wsgi_app = app.wsgi_app

    def __call__(self, environ, start_response):
        req = Request(environ)
        auth_token = req.cookies.get('token')

        try:
            user_info = id_token.verify_oauth2_token(
                auth_token,
                GOOGLE_AUTH_REQUEST_ADAPTER,
                self.app.config['CLIENT_ID'])
            environ['user'] = { k:v for k,v in user_info.items() if k in self.USER_INFO_FIELDS }
        except ValueError:
            environ['user'] = None

        return self.wsgi_app(environ, start_response)

def require_authentication(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.environ['user'] is not None:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper