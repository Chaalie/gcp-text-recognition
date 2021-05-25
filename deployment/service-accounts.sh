#!/bin/bash

APP_ENGINE_SVC=${PROJECT_ID}@appspot.gserviceaccount.com
IMAGE_TRANSFORMER_SVC=gcf-image-transformer@${PROJECT_ID}.iam.gserviceaccount.com
TEXT_RECOGNIZER_SVC=gcf-text-recognizer@${PROJECT_ID}.iam.gserviceaccount.com
EMAIL_NOTIFIER_SVC=gcf-email-notifier@${PROJECT_ID}.iam.gserviceaccount.com

gcloud iam service-accounts create gcf-email-notifier \
    --display-name="Email Notifier Cloud Function"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${EMAIL_NOTIFIER_SVC}" \
    --role="roles/datastore.owner"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${EMAIL_NOTIFIER_SVC}" \
    --role="roles/iam.serviceAccountTokenCreator"

gcloud iam service-accounts create gcf-image-transformer \
    --display-name="Image Transformer Cloud Function"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${IMAGE_TRANSFORMER_SVC}" \
    --role="roles/datastore.owner"

gcloud iam service-accounts create gcf-text-recognizer \
    --display-name="Text Recognizer Cloud Function"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${TEXT_RECOGNIZER_SVC}" \
    --role="roles/datastore.owner"