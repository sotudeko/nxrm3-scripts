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
endpoints['reposummary'] = 'repositories'

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
    parser.add_argument('-r', '--run', action='store_false', default=False, required=False)

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

    print ('create ' + nx_type + ': ' + url)
    print (payload)

    if nx_run:
        print ("creating " + nx_type)

        resp = requests.post(url, 
                            allow_redirects = False,
                            json=payload, 
                            auth=requests.auth.HTTPBasicAuth(nx_user, nx_pwd), 
                            verify=False)
        print(resp)

        if resp.status_code == 200:
            res = resp.json()
            print (res)
        else:
            res = "Create error"

    return 
  

def get_endpoint(payload):
    # print (payload)
    type_api = ""

    if nx_type == "repo":
        type_api = get_repo_api(payload)
    elif nx_type == "priv":
        type_api = get_privs_api(payload)
    elif nx_type == "blob":
        type_api = get_blobs_api(payload)
    else:
        type_api = endpoints[nx_type]

    return type_api


def get_privs_api(payload):
    return ""


def get_repo_api(payload):
    name = payload["name"]
    format = payload["format"]
    url = payload["url"]
    type = payload["type"]

    if format == "maven2":
        format = format[:-1]

    type_api = "repositories/" + format + "/" + type

    return type_api


def get_blobs_api(payload):
    return ""


def main():
    get_args()

    print (nx_run)

    f = open(datafile)
    data = json.load(f)

  
    for payload in data:
        type_api = get_endpoint(payload)

        if not type_api == "":
            create_object(type_api, payload)
        
        break

    f.close()
                

if __name__ == '__main__':
    main()
