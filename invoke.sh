#!/bin/bash


export CT_URL=https://cz-hro-test.church.tools/index.php
export CT_CAL_ID=2
export CT_USER=jorg@bolay.org
export CT_PASSWORD=pNlKukogySl0MhsOebot
export CT_BUCKET=cz-cal.bolay.org
export CT_FILENAME=cal.pdf
export CT_AWS_KEY_ID=AKIAIGVLPEG3VD7IXHGA
export CT_AWS_ACCESS_KEY=tN4v9CKnhrkiEnDBYNQXV5izwPDfmFd1gld7t5D5
export CT_AWS_REGION=eu-west-1



serverless invoke local -f generate --data '{"resource": "/{month-cal+}", "path": "/", "httpMethod": "GET", "headers": None, "queryStringParameters": None, "pathParameters": None, "stageVariables": None, "requestContext": {"path": "/{month-cal+}", "accountId": "451585377584", "resourceId": "dvzz30", "stage": "test-invoke-stage", "requestId": "test-invoke-request", "identity": {"cognitoIdentityPoolId": None, "accountId": "451585377584", "cognitoIdentityId": None, "caller": "451585377584", "apiKey": "test-invoke-api-key", "sourceIp": "test-invoke-source-ip", "accessKey": "ASIAIUIWLYUAPBY37QVQ", "cognitoAuthenticationType": None, "cognitoAuthenticationProvider": None, "userArn": "arn:aws:iam::451585377584:root", "userAgent": "Apache-HttpClient/4.5.x (Java/1.8.0_131)", "user": "451585377584"}, "resourcePath": "/{month-cal+}", "httpMethod": "GET", "apiId": "gstxkgkc65"}, "body": None, "isBase64Encoded": False}'
