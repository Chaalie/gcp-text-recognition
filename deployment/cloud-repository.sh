#!/bin/bash

mkdir tmp
cd tmp

git config --global credential.https://source.developers.google.com.helper gcloud.sh
git clone https://github.com/Chaalie/gcp-text-recognition.git 
cd gcp-text-recognition

gcloud source repos create gcp-text-recognition
git remote add google https://source.developers.google.com/p/${PROJECT_ID}/r/gcp-text-recognition
git push --all google

cd ..
rm -rf gcp-text-recognition

cd ..
rm -rf tmp