#!/bin/bash

componentDB=$1
repositoryName=$2

rm -rf ${repositoryName}-extract

echo "SELECT bucket.repository_name as repository, \
 name, format, size, created_by, last_downloaded, last_updated, \
 blob_created, blob_updated FROM asset \
 where bucket.repository_name = \"${repositoryName}\" \
 AND (name like '%.jar' or name like '%.war')" \
 | java -Xmx4g -DextractDir=./${repositoryName}-extract -DexportPath=./${repositoryName}.json \
 -jar ./orient-console.jar ${componentDB}

 python3 json2csv.py ${repositoryName}.json