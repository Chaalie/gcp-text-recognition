#!/bin/bash
set -x

PROJECT_ID=$(gcloud config get-value project)
PROJECT_NUMBER=$(gcloud projects describe ${PROJECT_ID} | grep "projectNumber" | cut -d "'" -f 2)
USER_EMAIL=$(gcloud config get-value account)

. enable-apis.sh

. cloud-repository.sh

. oauth.sh

. service-accounts.sh

. cloud-storage.sh

. app-engine.sh

. cloud-functions.sh

. cloud-build.sh

# initially trigger builds to properly setup all services
gcloud beta builds triggers run --branch=main web-deploy-on-push
gcloud beta builds triggers run --branch=main image-transformer-deploy-on-push
gcloud beta builds triggers run --branch=main text-recognizer-deploy-on-push
gcloud beta builds triggers run --branch=main email-notifier-deploy-on-push