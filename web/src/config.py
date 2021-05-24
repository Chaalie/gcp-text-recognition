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
    def OAUTH_CLIENT_ID(self):
        return self._OAUTH_CLIENT_ID

    # Name of a GCP bucket where uploaded files will be stored
    @property
    def IMAGES_BUCKET_NAME(self):
        return self._IMAGES_BUCKET_NAME

class DevelopmentConfig(Config):
    ENV = 'development'
    TESTING = True

    def __init__(self):
        load_dotenv('.env')

        self._SECRET_KEY = os.environ.get('SECRET_KEY')
        self._OAUTH_CLIENT_ID = os.environ.get('OAUTH_CLIENT_ID')
        self._IMAGES_BUCKET_NAME = os.environ.get('IMAGES_BUCKET_NAME')

class DebugConfig(DevelopmentConfig):
    DEBUG = True

class ProductionConfig(Config):
    ENV = 'production'

    def __init__(self):
        client = secretmanager.SecretManagerServiceClient()
        name = os.environ.get('SECRET_KEY_RESOURCE_ID')
        response = client.access_secret_version(name=name)
        payload = response.payload.data.decode("UTF-8")

        self._SECRET_KEY = payload
        self._OAUTH_CLIENT_ID = os.environ.get('OAUTH_CLIENT_ID')
        self._IMAGES_BUCKET_NAME = os.environ.get('IMAGES_BUCKET_NAME')