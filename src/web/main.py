from flask import Flask, render_template, redirect, request, g, url_for
from werkzeug.wrappers import Request
from google.auth.transport import requests
from google.oauth2 import id_token

from functools import wraps

GOOGLE_AUTH_REQUEST_ADAPTER = requests.Request()
# ID of a GCP credential to be used
CLIENT_ID = '909823663-uv6ue3mcsie34qv0osnekql9045eebu6.apps.googleusercontent.com'
# CLIENT_ID = os.environ.get('CLIENT_ID')
# Name of a GCP bucket where uploaded files will be stored
# BUCKET_NAME = os.environ.get('BUCKET_NAME')

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
        'name'
    ]

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        req = Request(environ)
        auth_token = req.cookies.get('token')

        try:
            user_info = id_token.verify_oauth2_token(
                auth_token,
                GOOGLE_AUTH_REQUEST_ADAPTER,
                CLIENT_ID)
            environ['user'] = { k:v for k,v in user_info.items() if k in self.USER_INFO_FIELDS }
        except ValueError:
            environ['user'] = None

        return self.app(environ, start_response)

def require_authentication(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.environ['user'] is not None:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper

app = Flask(__name__)
app.wsgi_app = AuthMiddleware(app.wsgi_app)

@app.route('/login', methods=['GET'])
def login():
    if request.environ['user'] is not None:
        return redirect(url_for('home'))
    else:
        return render_template('login.html', CLIENT_ID=CLIENT_ID)


# Logout action, removes authentication token from cookies
@app.route('/logout', methods=['GET'])
def logout():
    res = redirect(url_for('home'))
    res.delete_cookie('token')
    return res


@app.route('/', methods=['GET'])
@require_authentication
def home():
    return render_template('index.html', user=request.environ['user'], CLIENT_ID=CLIENT_ID)

@app.route('/recognize', methods=['POST'])
@require_authentication
def recognize():
    f = request.files['file']
    f.save('tmp.png')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
