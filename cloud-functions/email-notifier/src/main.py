import json
import base64

from google.cloud import firestore

db = firestore.Client()

def main(event, context):
    message_data = base64.b64decode(event['data']).decode('utf-8')
    message = json.loads(message_data)

    file_id = message['id']
    print(f'Recognition finished for {file_id}')

    data = db.collection('text-recognitions').document(file_id).get()
    print(f'Sending email to: {data["sender_email"]}')