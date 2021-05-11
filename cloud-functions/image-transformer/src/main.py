import os
import tempfile

from google.cloud import storage
from wand.image import Image

storage_client = storage.Client()

MIN_WIDTH = 1024
MIN_HEIGHT = 768

def main(file_data, context):
    src_file_name = file_data['name']
    src_bucket_name = file_data['bucket']

    print(f'processing: gs://{src_bucket_name}/{src_file_name}')

    src_blob = storage_client.bucket(src_bucket_name).get_blob(src_file_name)
    _, tmp_filename = tempfile.mkstemp()
    src_blob.download_to_filename(tmp_filename)

    with Image(filename=tmp_filename) as image:
        ratio = image.width / image.height
        scaled_width = max(image.width, MIN_WIDTH)
        scaled_height = max(image.height, MIN_HEIGHT)
        if scaled_height * ratio > scaled_width:
            scaled_width = round(scaled_height * ratio)
        else:
            scaled_height = round(scaled_width / ratio)

        print(f'transforming {image.width}x{image.height},{image.format} -> {scaled_width}x{scaled_height},jpeg')

        image.format = 'jpeg'
        image.resize(scaled_width, scaled_height)
        image.save(filename=tmp_filename)

    dest_file_name = src_file_name
    dest_bucket_name = os.getenv('DESTINATION_BUCKET')

    print(f'saving result to: gs://{dest_bucket_name}/{dest_file_name}')

    dest_bucket = storage_client.bucket(dest_bucket_name)
    dest_blob = dest_bucket.blob(dest_file_name)
    dest_blob.upload_from_filename(tmp_filename, content_type='jpeg')

    os.remove(tmp_filename)
    