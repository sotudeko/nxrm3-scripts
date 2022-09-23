#!/bin/bash

# fail if anything errors
set -e
# fail if a function call is missing an argument
set -u

username=${1:-admin}
password=${2:-admin123}
host=${3:-http://localhost:8081}

function runScript {
    script_name=$1
    payload=$2
    curl -v -X POST -u $username:$password --header "Content-Type: text/plain" "$host/service/rest/v1/script/${script_name}/run" -d@${payload}
}

runScript basic_proxy basic-demo.json
runScript secure_proxy secure-demo.json



