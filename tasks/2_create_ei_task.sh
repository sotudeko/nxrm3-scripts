#!/bin/bash

# usage: sh create_task.sh [export|import] [repository_name]

# fail if anything errors
set -e
# fail if a function call is missing an argument
set -u


ei_type=${1}
repository_name=${2}
ei_rootdir=${3:-/var/tmp}
username=${4:-admin}
password=${5:-admin123}
host=${6:-http://localhost:8081}

script_name="export_import_script"
alert_emailaddr="alert@myorg.com"

task_payload_dir="./task_payload"
task_name="${ei_type}_${repository_name}"
payload_filename="${task_payload_dir}/${task_name}.json"

[[ ! -d "${task_payload_dir}" ]] && mkdir "${task_payload_dir}"


function create_task_payload {
    datadir="${ei_rootdir}/${task_name}"

    case ${ei_type} in
        export) datadir_key="targetDir";;
        import) datadir_key="sourceDir";;
        *) exit -1;;
    esac

    printf "creating task ${task_name} for repository ${ei_type}\n"
    printf "task definition file ${payload_filename}\n"

cat <<EOF > ${payload_filename}
{
    "name" : "${task_name}", 
    "typeId" : "repository.${ei_type}", 
    "task_alert_email" : "${alert_emailaddr}", 
    "enabled" : "true",
    "taskProperties" : {
        "repositoryName" : "${repository_name}",
        "${datadir_key}": "${datadir}",
        "notificationCondition": "SUCCESS_FAILURE"
    },
    "booleanTaskProperties" : ""
}
EOF

    printf "created payload file: ${payload_filename}\n"

}


create_task_payload

curl -v -X POST -u ${username}:${password} --header "Content-Type: text/plain" "${host}/service/rest/v1/script/${script_name}/run" -d@${payload_filename}
 



