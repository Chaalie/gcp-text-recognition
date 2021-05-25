#!/bin/bash

ORIGINAL_IMAGES_BUCKET=${PROJECT_ID}-original-images
TRANSFORMED_IMAGES_BUCKET=${PROJECT_ID}-transformed-images

gsutil mb \
    -c standard \
    -b on \
    -l EU \
    gs://${ORIGINAL_IMAGES_BUCKET}

gsutil iam ch \
    serviceAccount:${APP_ENGINE_SVC}:objectCreator \
    serviceAccount:${IMAGE_TRANSFORMER_SVC}:objectViewer \
    serviceAccount:${EMAIL_NOTIFIER_SVC}:objectViewer \
    serviceAccount:${EMAIL_NOTIFIER_SVC}:legacyBucketReader \
    gs://${ORIGINAL_IMAGES_BUCKET}

gsutil mb \
    -c standard \
    -b on \
    -l EU \
    gs://${TRANSFORMED_IMAGES_BUCKET}

gsutil iam ch \
    serviceAccount:${IMAGE_TRANSFORMER_SVC}:objectCreator \
    serviceAccount:${TEXT_RECOGNIZER_SVC}:objectViewer \
    serviceAccount:${EMAIL_NOTIFIER_SVC}:objectViewer \
    serviceAccount:${EMAIL_NOTIFIER_SVC}:legacyBucketReader \
    gs://${TRANSFORMED_IMAGES_BUCKET}