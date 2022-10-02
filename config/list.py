import sys
import json
import argparse
import requests
import os


base_url = 'service/rest/v1'

endpoints = {}
endpoints['roles'] = 'security/roles'
endpoints['privs'] = 'security/privileges'
endpoints['blobs'] = 'blobstores'
endpoints['repos'] = 'repositories'
endpoints['reposettings'] = 'repositorySettings'


output_dir = './output'

if not os.path.exists (output_dir):
        os.mkdir(output_dir)


def get_args():
    global nx_server, nx_user, nx_pwd, nx_type

    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--server', help='', default="http://localhost:8081", required=False)
    parser.add_argument('-a', '--user', help='', default="admin", required=False)
    parser.add_argument('-p', '--passwd', default="admin123", required=False)
    parser.add_argument('-t', '--type', required=True)

    args = vars(parser.parse_args())
    
    nx_server = args["server"]
    nx_user = args["user"]
    nx_pwd = args["passwd"]
    nx_type = args['type']

    return


def get_data(api):
    type_api = endpoints[api]

    url = "{}/{}/{}" . format(nx_server, base_url, type_api)

    print("get_data: " + url)

    req = requests.get(url, auth=(nx_user, nx_pwd), verify=False)

    if req.status_code == 200:
        res = req.json()
        write_file(nx_type, res)
    else:
        res = "Error fetching data"

    return res


def write_file(type, json_data):
    output_file = "{}/{}{}".format(output_dir, type, ".json")
    json_formatted = json.dumps(json_data, indent=2)
    
    with open(output_file, 'w') as outfile:
        json.dump(json_data, outfile, indent=2)
    
    print(output_file)
    return


def main():
    get_args()

    data = get_data(nx_type)
    

                
if __name__ == '__main__':
    main()
