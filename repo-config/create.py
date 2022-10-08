# 1. blob paths must be same
# 2. update any http paths in the repo json files

import re
import sys
import json
import argparse
import requests
import os

base_url = 'service/rest/v1'

endpoints = {}
endpoints['role'] = 'security/roles'
endpoints['priv'] = 'security/privileges'
endpoints['blob'] = 'blobstores'
endpoints['repo'] = 'repositorySettings'
endpoints['repo2'] = 'repositories'

ootb_blobstore = 'default'
ootb_roles = ['nx-admin', 'nx-anonymous', 'replication-role']
ootb_priv = 'nx-'
ootb_repositories = ['nuget-group', 'nuget.org-proxy', 'nuget-hosted', 'maven-central', 'maven-public', 'maven-releases', 'maven-snapshots']
ootb_users = ['admin', 'anonymous']

def get_args():
    global nx_server, nx_user, nx_pwd, nx_type, nx_run, datafile

    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--server', help='', default="http://localhost:8081", required=False)
    parser.add_argument('-a', '--user', help='', default="admin", required=False)
    parser.add_argument('-p', '--passwd', default="admin123", required=False)
    parser.add_argument('-t', '--type', required=True)
    parser.add_argument('-f', '--datafile', required=True)
    parser.add_argument('-r', '--run', action='store_true', default=True, required=False)

    args = vars(parser.parse_args())
    
    nx_server = args["server"]
    nx_user = args["user"]
    nx_pwd = args["passwd"]
    nx_type = args['type']
    nx_run = args['run']
    datafile = args['datafile']

    return


def create_object(type_api, payload):

    url = "{}/{}/{}" . format(nx_server, base_url, type_api)
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}

    object_name = payload["name"]

    print ('create ' + nx_type + ': ' + object_name + " " + url)

    if nx_run:
        resp = requests.post(url, 
                            allow_redirects = False,
                            json=payload, 
                            auth=requests.auth.HTTPBasicAuth(nx_user, nx_pwd), 
                            verify=False)

        if resp.status_code == 200 or resp.status_code == 201:
            # res = resp.json()
            print('success creating ' + nx_type + ': ' + object_name + " " + str(resp))
        else:
            print('error creating ' + nx_type + ': ' + object_name + " " + str(resp))
            # print(payload)

    return
  

def get_endpoint(payload):
    type_api = ""

    if nx_type == "role":
        type_api = get_role_api(payload)
    elif nx_type == "repo":
        type_api = get_repo_api(payload)
    elif nx_type == "priv":
        type_api = get_priv_api(payload)
    elif nx_type == "blob":
        type_api = get_blob_api(payload)
    else:
        type_api = endpoints[nx_type]

    return type_api


def get_role_api(payload):
    type_api = ""

    role_name = payload["name"]

    if not role_name.startswith("nx-") and role_name.startswith("replication"):
        type_api = "/security/roles"

    return type_api


def get_priv_api(payload):
    type_api = ""
    priv_type = payload["type"]
    priv_name = payload["name"]

    if not priv_name.startswith("nx-"):
        if priv_type == "application":
            type_api = "security/privileges/application"
        elif priv_type == "repository-content-selector":
            type_api = "security/privileges/repository-content-selector"
        elif priv_type == "repository-view":
            type_api = "security/privileges/repository-view"
        elif priv_type == "repository-admin":
            type_api = "security/privileges/repository-admin"
        elif priv_type == "wildcard":
            type_api = "security/privileges/wildcard"
        elif priv_type == "script":
            type_api = "security/privileges/script"

    return type_api


def get_repo_api(payload):
    type_api = ""
    
    name = payload["name"]
    format = payload["format"]
    url = payload["url"]
    type = payload["type"]

    if format == "maven2":
        format = format[:-1]

    if type == "hosted":
        type_api = "repositories/" + format + "/" + type

    return type_api


def get_blob_api(payload):
    return ""


def main():
    get_args()

    f = open(datafile)
    data = json.load(f)

    for payload in data:
        type_api = get_endpoint(payload)

        if not type_api == "":
            create_object(type_api, payload)

    f.close()
                

if __name__ == '__main__':
    main()
