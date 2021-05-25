#!/bin/bash

gcloud alpha iap oauth-brands create --application_title="Text recognition" --support_email=${USER_EMAIL}
OAUTH_CLIENT_ID=$(gcloud alpha iap oauth-clients create projects/${PROJECT_NUMBER}/brands/${PROJECT_NUMBER} --display_name="Text recognition" | grep "name:" | cut -d "/" -f 6)