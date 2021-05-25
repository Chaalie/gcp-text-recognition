# Setting up an application in new project

Using `create.sh` it is possible to set up the whole application in the brand new project. The script setups all required resources like service accounts, buckets, secrets, cloud functions, app engine and cloud build triggers, together with Cloud Source Repository.

The script is using default Google Cloud project from `gcloud`, so in order to make it run in the new project first set it as a default one with `gcloud config set project PROJECT_ID`, replacing `PROJECT_ID` with name of the project.

After script got run, some manual work, that cannot be done automatically, needs to be made in order to make an application running properly, namely:
1. create an [SendGrid](https://sendgrid.com/) account, create an authorized sender and copy it's API key
2. go to Google Cloud Console -> Security -> Secret Manager and create a new version of `sendgrid-api-key` secret using an API key from previous step
3. go to Google Cloud Console -> APIs & Services -> Credentials and click `CREATE CREDENTIALS` and `OAuth client ID`
    - choose `Web application` as application type
    - if you want change a default name
    - add `https://PROJECT_ID.appspot.com` (replace `PROJECT_ID` with your project name) as an uri to both `Authorized JavaScript origins` and `Authorized redirect URIs`
    - click `CREATE`
4. copy a `Client ID` of a newly created entity
5. go to Google Cloud Console -> Cloud Build -> Triggers and edit `web-deploy-on-push` trigger by replacing its value of `_OAUTH_CLIENT_ID` substition variable with an id copied in previous step, save the changes
6. go to Google Cloud Console -> Cloud Build -> Triggers and manually trigger `web-deploy-on-push` by clicking `RUN` and then `RUN TRIGGER` in order to propagate a change OAauth Client

After finishing all of these stops application should be running correctly. If application authorization logic seems to not work properly (impossible to login thorugh Google account), wait about 5 minutes as it can take some times to OAuth changes to be correctly propagated in GCP.
