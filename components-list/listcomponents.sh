#!/bin/bash

#  *** WARNING: PLEASE DO NOT RUN THIS SCRIPT ON YOUR PRODUCTION INSTANCE DATABASE
#  *** YOU MUST A COPY OF YOUR LATEST BACKUP

# Usage
# 1. get a copy of the component database from your last backup and locatr it to the directory containing this file
# 2. make sure Java 8 is set in your enironment
# 3. you also need python3 in your environment
# 4. run the script: "sh listcomponents.sh <name of component db file_.bak> <name of repository>"

# e.g. sh ./listcomponents.sh /tmp/dbbbackup-mon10oct/component-2022-10-10-12-27-21-3.41.0-01.bak maven-releases


componentDB=$1
repositoryName=$2

rm -rf ${repositoryName}-extract

echo "SELECT bucket.repository_name as repository, \
 name, format, size, created_by, last_downloaded, last_updated, \
 blob_created, blob_updated FROM asset \
 where bucket.repository_name = \"${repositoryName}\" \
 order by last_downloaded desc "\
 | java -Xmx4g -DextractDir=./${repositoryName}-extract -DexportPath=./${repositoryName}.json \
 -jar ./orient-console.jar ${componentDB}

python3 json2csv.py ${repositoryName}.json

awk -F',' '{sum+=$7} END {print sum/1024000 "Mb"}' ${repositoryName}.json.csv

