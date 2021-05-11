import os
import json
import base64

from google.cloud import firestore, secretmanager
from google.cloud import secretmanager
import sendgrid

db = firestore.Client()
secret_client = secretmanager.SecretManagerServiceClient()
SENDGRID_API_KEY_SECRET_NAME = os.environ.get('SENDGRID_API_KEY_SECRET_NAME')
SENDGRID_API_KEY = secret_client.access_secret_version(name=SENDGRID_API_KEY_SECRET_NAME).payload.data.decode('UTF-8')
sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)

def main(event, context):
    message_data = base64.b64decode(event['data']).decode('utf-8')
    message = json.loads(message_data)

    file_id = message['id']

    data = db.collection('text-recognitions').document(file_id).get().to_dict()
    print(f'Sending email to: {data["sender_email"]}')

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
                    '-original_file-': data['original_file'],
                    '-transformed_file-': data['transformed_file'],
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
