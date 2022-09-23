#!/bin/bash

# A simple example script that publishes a number of scripts to the Nexus Repository Manager
# and executes them.

# fail if anything errors
set -e
# fail if a function call is missing an argument
set -u

# add a script to the repository manager and run it
name=$1
file=$2

username=${3:-admin}
password=${4:-admin123}
host=${5:-http://localhost:8081}


printf "Provisioning HTTP/S proxy - starting \n\n" 

# using grape config that points to local Maven repo and Central Repository , default grape config fails on some downloads although artifacts are in Central
# change the grapeConfig file to point to your repository manager, if you are already running one in your organization
groovy -Dgroovy.grape.report.downloads=true -Dgrape.config=grapeConfig.xml addUpdateScript.groovy -u "$username" -p "$password" -n "$name" -f "$file" -h "$host"
printf "\nPublished $file as $name\n\n"


# Runtime
# sh add-script.sh ei_task create-task.groovy
# sh run-script.sh ei_task staging-development.json