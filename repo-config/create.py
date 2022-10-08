# 1. blob paths must be same
# 2. update any http paths in the repo json files
# 3. create order is important: blob, repo, content selector, priv, role, , user

from asyncore import read
import re
import sys
import json
import argparse
import requests
import os
import constants


def app_init():
    global nx_server, nx_user, nx_pwd, nx_type, nx_run, datafile

    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--server', help='', default="http://localhost:8081", required=False)
    parser.add_argument('-a', '--user', help='', default="admin", required=False)
    parser.add_argument('-p', '--passwd', default="admin123", required=False)
    parser.add_argument('-t', '--type', required=False)
    parser.add_argument('-f', '--datafile', required=False)
    parser.add_argument('-r', '--run', action='store_true', default=True, required=False)

    args = vars(parser.parse_args())
    
    nx_server = args["server"]
    nx_user = args["user"]
    nx_pwd = args["passwd"]
    nx_type = args['type']
    nx_run = False
    datafile = args['datafile']

    return


def create_object(type_api, payload):
    object_name = payload['name']
    url = "{}/{}/{}" . format(nx_server, constants.base_url, type_api)
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    # print(type_api, payload)

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
        type_api = constants.endpoints[nx_type]

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


def read_json_file(datafile):
    f = open(datafile)
    data = json.load(f)
    return data


def create_blobs():
    f = constants.output_dir + '/blob.json'
    data = read_json_file(f)

    for blob in data:
        name = blob['name']
        type = blob['type']

        if type == 'File' and not name == constants.ootb_blobstore:

            blobpath_file = constants.output_dir + '/blob_' + name + '.json'
            pathconfig = read_json_file(blobpath_file)
            blob_path = pathconfig['path']

            blob_payload = {}
            blob_payload['softQuota'] = {}
            blob_payload['softQuota']['type'] = 'File'
            blob_payload['softQuota']['limt'] = 0
            blob_payload['path'] = blob_path
            blob_payload['name'] = name

            print ('create blob: ' + name + " " + type + " " + blob_path + " " + constants.blobpath_api)
            create_object(constants.blobpath_api, blob_payload)

    return


def create_repositories():
    f = constants.output_dir + '/repo.json'
    data = read_json_file(f)

    hosted_repos = get_repos_by_type(data, 'hosted')
    proxy_repos = get_repos_by_type(data, 'proxy')
    group_repo = get_repos_by_type(data, 'group')

    for repo in data:
        name = repo["name"]
        format = repo["format"]
        url = repo["url"]
        type = repo["type"]

        if format == "maven2":
            format = format[:-1]
            repo_api = "repositories/" + format + "/" + type

            print ('create repo: ' + name + " " + format + " " + repo_api)
            create_object(repo_api, repo)

    return


def get_repos_by_type(data, find_type):
    repos = []

    for repo in data:
        type = repo['type']
        if type == find_type:
            repos.append(repo)

    return repos


def main():
    app_init()

    create_blobs()
    create_repositories()


                

if __name__ == '__main__':
    main()
