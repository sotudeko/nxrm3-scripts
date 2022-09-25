#!/bin/bash

# usage: # sh add_export_import_script.sh

username=${1:-admin}
password=${2:-admin123}
host=${3:-http://localhost:8081}

# fail if anything errors
set -e

# add export/import repository script to the repository manager
script_name=export_import_script
script_file=0_export_import_script.groovy

printf "Provisioning Export/Import Repository API Script - starting \n\n" 

# using grape config that points to local Maven repo and Central Repository , default grape config fails on some downloads although artifacts are in Central
# change the grapeConfig file to point to your repository manager, if you are already running one in your organization
groovy -Dgroovy.grape.report.downloads=true -Dgrape.config=grapeConfig.xml 0_addUpdateScript.groovy -u "${username}" -p "${password}" -n "${script_name}" -f "${script_file}" -h "${host}"

printf "\nPublished ${script_file} as ${script_name}\n\n"

