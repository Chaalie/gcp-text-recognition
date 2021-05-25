#!/bin/bash

# create a secret storing application secret (session) key
echo "CHANGE THIS SECRET" | gcloud secrets create web-secret-key --data-file=-
gcloud secrets add-iam-policy-binding web-secret-key \
    --member="serviceAccount:${APP_ENGINE_SVC}" \
    --role="roles/secretmanager.secretAccessor"
WEB_SECRET_KEY_RESOURCE_ID=projects/${PROJECT_NUMBER}/secrets/web-secret-key/versions/latest

gcloud app create --region=europe-central2
gcloud firestore databases create --region=europe-central2