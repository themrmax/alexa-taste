#!/bin/bash
rm index.zip 
zip -r -j index lambda/
aws lambda update-function-code --function-name taste --zip-file fileb://index.zip

