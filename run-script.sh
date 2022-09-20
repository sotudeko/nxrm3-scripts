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
payload=${4:-proxy-repo-config.json}

# add the context if you are not using the root context

curl -v -X POST -u $username:$password --header "Content-Type: text/plain" "$host/service/rest/v1/script/${scriptname}/run" -d@${payload}
