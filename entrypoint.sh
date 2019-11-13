#!/bin/sh -l

# remove dupes in the case where we are deploying to amazon from our local machines
rm -f lambda-deploy.zip
zip -r ./lambda-deploy.zip *

#sam build
sam package --output-template-file \
    packaged.yaml --s3-bucket "$BUCKET_NAME"

if sam deploy --template-file packaged.yaml \
    --region us-east-1 --capabilities \
    CAPABILITY_IAM --stack-name "$STACK_NAME"
    then 
        exit 0
    else
        exit 1
fi

exit 0 

# export command sets environment variable for Bash
# export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
# export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
# export AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION
# export AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN

# pwd, ls -ls. used for debugging purposes
# pwd
