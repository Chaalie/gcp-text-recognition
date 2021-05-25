#!/bin/bash

CLOUD_BUILD_SVC=${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com

# Set proper permission for Cloud Build service account
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${CLOUD_BUILD_SVC}" \
    --role="roles/cloudfunctions.developer"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${CLOUD_BUILD_SVC}" \
    --role="roles/appengine.appAdmin"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${CLOUD_BUILD_SVC}" \
    --role="roles/iam.serviceAccountUser"

# Setup Cloud Build to trigger and deploy code when source chnages
gcloud beta builds triggers create cloud-source-repositories \
    --name="web-deploy-on-push" \
    --description="Deploys web App Engine app when its sources get updated." \
    --repo="gcp-text-recognition" \
    --branch-pattern="^main$" \
    --build-config="web/cloudbuild.yaml" \
    --included-files="web/src**" \
    --substitutions=_OAUTH_CLIENT_ID=${OAUTH_CLIENT_ID},_SECRET_KEY_RESOURCE_ID=${WEB_SECRET_KEY_RESOURCE_ID},_IMAGES_BUCKET_NAME=${ORIGINAL_IMAGES_BUCKET}

gcloud beta builds triggers create cloud-source-repositories \
    --name="image-transformer-deploy-on-push" \
    --description="Deploys image-transformer cloud function when its sources get updated." \
    --repo="gcp-text-recognition" \
    --branch-pattern="^main$" \
    --build-config="cloud-functions/image-transformer/cloudbuild.yaml" \
    --included-files="cloud-functions/image-transformer/src/**" \
    --substitutions=_DESTINATION_BUCKET=${TRANSFORMED_IMAGES_BUCKET},_TRIGGER_BUCKET=${ORIGINAL_IMAGES_BUCKET}

gcloud beta builds triggers create cloud-source-repositories \
    --name="text-recognizer-deploy-on-push" \
    --description="Deploys text-recognizer cloud function when its sources get updated." \
    --repo="gcp-text-recognition" \
    --branch-pattern="^main$" \
    --build-config="cloud-functions/text-recognizer/cloudbuild.yaml" \
    --included-files="cloud-functions/text-recognizer/src/**" \
    --substitutions=_TOPIC_NAME=${TOPIC_NAME},_TRIGGER_BUCKET=${TRANSFORMED_IMAGES_BUCKET}

gcloud beta builds triggers create cloud-source-repositories \
    --name="email-notifier-deploy-on-push" \
    --description="Deploys image-transformer cloud function when its sources get updated." \
    --repo="gcp-text-recognition" \
    --branch-pattern="^main$" \
    --build-config="cloud-functions/email-notifier/cloudbuild.yaml" \
    --included-files="cloud-functions/email-notifier/src/**" \
    --substitutions=_ORIGINAL_IMAGES_BUCKET_NAME=${ORIGINAL_IMAGES_BUCKET},_SENDGRID_API_KEY_SECRET_NAME=${SENDGRID_API_KEY_RESOURCE_ID},_TRANSFORMED_IMAGES_BUCKET_NAME=${TRANSFORMED_IMAGES_BUCKET},_TRIGGER_TOPIC=${TOPIC_NAME}