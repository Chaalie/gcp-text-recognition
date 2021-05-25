#!/bin/bash

TOPIC_NAME=text-recognition.finished

# IMAGE TRANSFORMER
gcloud functions deploy image-transformer \
    --region="europe-central2" \
    --runtime="python39" \
    --trigger-bucket="${ORIGINAL_IMAGES_BUCKET}" \
    --service-account="${IMAGE_TRANSFORMER_SVC}" \
    --ingress-settings="internal-only"

# TEXT RECOGNIZER
gcloud functions deploy text-recognizer \
    --region="europe-central2" \
    --runtime="python39" \
    --trigger-bucket="${TRANSFORMED_IMAGES_BUCKET}" \
    --service-account="${TEXT_RECOGNIZER_SVC}" \
    --ingress-settings="internal-only"

# EMAIL NOTIFIER
# create Sendgrid API key secret
echo "CHANGE THIS SECRET" | gcloud secrets create sendgrid-api-key --data-file=-
gcloud secrets add-iam-policy-binding sendgrid-api-key \
    --member="serviceAccount:${EMAIL_NOTIFIER_SVC}" \
    --role="roles/secretmanager.secretAccessor"
SENDGRID_API_KEY_RESOURCE_ID=projects/${PROJECT_NUMBER}/secrets/sendgrid-api-key/versions/latest

# create a pubsub topic that will be subscribed by Email Notifier
gcloud beta pubsub topics create ${TOPIC_NAME}
gcloud beta pubsub topics add-iam-policy-binding ${TOPIC_NAME} \
    --member="serviceAccount:${TEXT_RECOGNIZER_SVC}" \
    --role="roles/pubsub.publisher"

gcloud functions deploy email-notifier \
    --region="europe-central2" \
    --runtime="python39" \
    --trigger-topic="${TOPIC_NAME}" \
    --service-account="${EMAIL_NOTIFIER_SVC}" \
    --ingress-settings="internal-only"