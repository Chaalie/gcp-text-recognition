from flask import Flask, flash, render_template, redirect, request, url_for, Markup
from google.cloud import storage

import hashlib

from auth import AuthMiddleware, require_authentication

ALLOWED_UPLOADS_EXTENSIONS = {'.png', '.jpg', '.jpeg'}

app = Flask(__name__)
app.wsgi_app = AuthMiddleware(app)

@app.route('/login', methods=['GET'])
def login():
    if request.environ['user'] is not None:
        return redirect(url_for('home'))
    else:
        return render_template('login.html', CLIENT_ID=app.config['CLIENT_ID'])


# Logout action, removes authentication token from cookies
@app.route('/logout', methods=['GET'])
def logout():
    res = redirect(url_for('home'))
    res.delete_cookie('token')
    return res


@app.route('/', methods=['GET'])
@require_authentication
def home():
    return render_template('index.html', user=request.environ['user'], CLIENT_ID=app.config['CLIENT_ID'])

@app.route('/recognize', methods=['POST'])
@require_authentication
def recognize():
    file = request.files['file']
    file_extension = '.' + file.filename.split('.')[-1]

    if file_extension not in ALLOWED_UPLOADS_EXTENSIONS:
        flash(Markup(f'Files with the extension <strong>{file_extension}</strong>, are not supported.'), 'upload_error')
        return redirect(url_for('home'))

    file_content = file.read()
    file_hash = hashlib.md5(file_content).hexdigest()

    bucket = storage.Client().get_bucket(app.config['CLOUD_STORAGE_BUCKET'])
    blob = bucket.blob(file_hash)
    blob.upload_from_string(
        file_content,
        content_type=file.content_type
    )

    flash('', 'upload_success')
    return redirect(url_for('home'))


import config
if __name__ == '__main__':
    app.config.from_object(config.DevelopmentConfig())
    app.run(host='127.0.0.1', port=8000)
else:
    app.config.from_object(config.ProductionConfig())