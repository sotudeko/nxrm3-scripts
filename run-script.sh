#!/bin/bash

# A simple example script that executes a Nexus Repository Manager API script

# fail if anything errors
set -e
# fail if a function call is missing an argument
set -u

scriptname=${1}
username=${2:-admin}
password=${3:-admin123}
host=${4:-http://localhost:8081}

# add the context if you are not using the root context

# curl -v -X POST -u $username:$password --header "Content-Type: text/plain" "$host/service/rest/v1/script/${scriptname}/run" -d '{"publicId": "MyApplicationID","name": "MyFirstApplication","organizationId":"f48b5344fa204a4c88df96b2d455d521","contactUserName":"AppContact","applicationTags": [{"tagId":"cd8fd2f4f289445b8975092e7d3045ba"}]}'

curl -v -X POST -u $username:$password --header "Content-Type: text/plain" "$host/service/rest/v1/script/${scriptname}/run" -d '{"reponame": "the-proxy-repo","url": "http://www.bbc.co.uk"}'

