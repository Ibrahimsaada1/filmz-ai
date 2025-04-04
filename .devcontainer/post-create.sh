#! /bin/sh

set -e

# Setup AWS cli
aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
aws configure set default.region $AWS_REGION
aws configure set default.output json

pip install -r requirements.txt
