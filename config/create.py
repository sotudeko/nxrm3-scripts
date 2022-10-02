import sys
import json
import argparse
import requests
import os

base_url = 'service/rest/v1'

endpoints = {}
endpoints['role'] = 'security/roles'
endpoints['privilege'] = 'security/privileges'
endpoints['blobstore'] = 'blobstores'
endpoints['repository'] = 'repositories'
endpoints['repositorySetting'] = 'repositorySettings'


def get_args():
    global nx_server, nx_user, nx_pwd, nx_type, nx_auth, nx_session, datafile

    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--server', help='', default="http://localhost:8081", required=False)
    parser.add_argument('-a', '--user', help='', default="admin", required=False)
    parser.add_argument('-p', '--passwd', default="admin123", required=False)
    parser.add_argument('-t', '--type', required=True)
    parser.add_argument('-f', '--datafile', required=True)

    args = vars(parser.parse_args())
    
    nx_server = args["server"]
    nx_user = args["user"]
    nx_pwd = args["passwd"]
    nx_type = args['type']
    datafile = args['datafile']

    return


def create_object(nx_type, payload):
    type_api = endpoints[nx_type]

    url = "{}/{}/{}" . format(nx_server, base_url, type_api)
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}

    print ('Creating ' + nx_type + ' ' + payload['id'] + ' at ' + url)

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

    return res
  

def main():
    get_args()

    f = open(datafile)
    data = json.load(f)
  
    for o in data:
        create_object(nx_type, o)
  
    f.close()
                

if __name__ == '__main__':
    main()
