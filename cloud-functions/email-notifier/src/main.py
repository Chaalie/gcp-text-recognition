import base64

def main(event, context):
    message = base64.b64decode(event["data"]).decode("utf-8")

    print(f'Recognition finished for {message}')