#!/bin/bash

# fail if anything errors
set -e
# fail if a function call is missing an argument
set -u

script_name=$1
payload=$2

username=${3:-admin}
password=${4:-admin123}
host=${5:-http://localhost:8081}
   
curl -v -X POST -u $username:$password --header "Content-Type: text/plain" "$host/service/rest/v1/script/${script_name}/run" -d@${payload}
 



