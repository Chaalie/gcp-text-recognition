import os
import json
from dotenv import load_dotenv
from google.cloud import secretmanager

class Config():
    ENV = ''
    TESTING = False
    DEBUG = False

    @property
    def SECRET_KEY(self):
        return self._SECRET_KEY

    # ID of a GCP credential to be used
    @property
    def CLIENT_ID(self):
        return self._CLIENT_ID

    # Name of a GCP bucket where uploaded files will be stored
    @property
    def CLOUD_STORAGE_BUCKET(self):
        return self._CLOUD_STORAGE_BUCKET

class DevelopmentConfig(Config):
    ENV = 'development'
    TESTING = True

    def __init__(self):
        load_dotenv('.env')

        self._SECRET_KEY = os.environ.get('SECRET_KEY')
        self._CLIENT_ID = os.environ.get('CLIENT_ID')
        self._CLOUD_STORAGE_BUCKET = os.environ.get('CLOUD_STORAGE_BUCKET')

class DebugConfig(DevelopmentConfig):
    DEBUG = True

class ProductionConfig(Config):
    ENV = 'production'

    def __init__(self):
        client = secretmanager.SecretManagerServiceClient()
        name = os.environ.get('CONFIG_SECRET_ID')
        response = client.access_secret_version(name=name)
        payload = response.payload.data.decode("UTF-8")

        secrets = json.loads(payload)

        self._SECRET_KEY = secrets['SECRET_KEY']
        self._CLIENT_ID = secrets['CLIENT_ID']
        self._CLOUD_STORAGE_BUCKET = secrets['CLOUD_STORAGE_BUCKET']