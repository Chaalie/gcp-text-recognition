import os
import json

from google.cloud import storage, vision, pubsub_v1, firestore

storage_client = storage.Client()
vision_client = vision.ImageAnnotatorClient()
publisher = pubsub_v1.PublisherClient()
db = firestore.Client()

PROJECT_ID = os.environ.get('PROJECT_ID')
TOPIC_NAME = os.environ.get('TOPIC_NAME')

def main(file_data, context):
    src_file_id = file_data['name']
    src_bucket_name = file_data['bucket']

    print(f'processing: gs://{src_bucket_name}/{src_file_id}')

    image = vision.Image(
        source=vision.ImageSource(gcs_image_uri=f'gs://{src_bucket_name}/{src_file_id}')
    )
    text_detection = vision_client.text_detection(image=image)
    annotations = text_detection.text_annotations

    if len(annotations) > 0:
        found_text = annotations[0].description
        print('Text detected:', found_text)
    else:
        found_text = None
        print('No text detected')

    db.collection('text-recognitions').document(src_file_id).update({
        'result': found_text
    })

    message = {
        'id': src_file_id
    }
    message_data = json.dumps(message).encode('utf-8')
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_NAME)
    publisher.publish(topic_path, data=message_data).result()