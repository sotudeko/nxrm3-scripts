#!/bin/bash

repoUrl=${1:-http://localhost:8081}
username=${2:-admin}
passwd=${3:-admin123}

endPoint='service/rest/v1/repositories'

curl -s -u ${username}:${passwd} -X GET ${repoUrl}/${endPoint} | jq '.[] | select(.type=="hosted") | .name' | tr -d '"'

exit 0





