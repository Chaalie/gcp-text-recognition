import os
import json
import base64
import datetime

import google.auth
from google.cloud import storage, firestore, secretmanager
import sendgrid

db = firestore.Client()
secret_client = secretmanager.SecretManagerServiceClient()
ORIGINAL_IMAGES_BUCKET_NAME = os.environ.get('ORIGINAL_IMAGES_BUCKET_NAME')
TRANSFORMED_IMAGES_BUCKET_NAME = os.environ.get('ORIGINAL_IMAGES_BUCKET_NAME')
SENDGRID_API_KEY_SECRET_NAME = os.environ.get('SENDGRID_API_KEY_SECRET_NAME')
SENDGRID_API_KEY = secret_client.access_secret_version(name=SENDGRID_API_KEY_SECRET_NAME).payload.data.decode('UTF-8')
sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
gcs = storage.Client()
credentials, _ = google.auth.default()

def main(event, context):
    # refresh to get service account and token
    credentials.refresh(google.auth.transport.requests.Request())

    message_data = base64.b64decode(event['data']).decode('utf-8')
    message = json.loads(message_data)

    file_id = message['id']
    data = db.collection('text-recognitions').document(file_id).get().to_dict()

    original_file = gcs.get_bucket(ORIGINAL_IMAGES_BUCKET_NAME).blob(file_id)
    original_file_url = original_file.generate_signed_url(
                access_token=credentials.token,
                service_account_email=credentials.service_account_email,
                expiration=datetime.timedelta(days=1),
                version='v4')
    transformed_file = gcs.get_bucket(TRANSFORMED_IMAGES_BUCKET_NAME).blob(file_id)
    transformed_file_url = transformed_file.generate_signed_url(
                access_token=credentials.token,
                service_account_email=credentials.service_account_email,
                expiration=datetime.timedelta(days=1),
                version='v4')

    mail_data = {
        'personalizations': [
            {
                'to': [
                    {
                        'email': data['sender_email']
                    }
                ],
                'subject': f'Results of text recognition - {file_id}',
                'substitutions': {
                    '-firstname-': data['sender_firstname'],
                    '-original_file-': original_file_url,
                    '-transformed_file-': transformed_file_url,
                    '-result-': data['result'],
                }
            }
        ],
        'from': {
            'email': 'k.waszczuk4@student.uw.edu.pl'
        },
        'content': [
            {
                'type': 'text/html',
                'value': f'''<p>Hello, -firstname-</p>

<p>Your requested text recognition is ready!</p>

<div>
    Original file: <a href="-original_file-">link</a>
</div>
<div>
    Transformed file: <a href="-transformed_file-"->link</a>
</div>
<div>
    Recognized text:
    <div>
        <pre style="font-size:20px">-result-</pre>
    </div>
</div>
'''
            }
        ]
    }
    sg.client.mail.send.post(request_body=mail_data)
