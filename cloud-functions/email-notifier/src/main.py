import json
import base64

def main(event, context):
    message_data = base64.b64decode(event['data']).decode('utf-8')
    message = json.loads(message_data)

    print(f'Recognition finished for {message["name"]}')