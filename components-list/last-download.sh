#!/bin/bash

componentDB=$1

repolist=${2:-repositories.lst}

function get_last_download {
  repositoryName=$1
  echo "repository: ${repositoryName}"

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
}

for repo in `cat ${repolist}`
do
  get_last_download ${repo}
  break
done
