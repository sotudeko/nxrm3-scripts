import sys
import json
import argparse
import requests
import os


base_url = 'service/rest/v1'
blobpath_api = 'blobstores/file'

endpoints = {}
endpoints['role'] = 'security/roles'
endpoints['user'] = 'security/users?source=default'
endpoints['priv'] = 'security/privileges'
endpoints['blob'] = 'blobstores'
endpoints['repo'] = 'repositorySettings'
endpoints['contentselector'] = 'security/content-selectors'
# endpoints['repo2'] = 'repositories'


output_dir = './output'

if not os.path.exists (output_dir):
        os.mkdir(output_dir)


def get_args():
    global nx_server, nx_user, nx_pwd, nx_type

    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--server', help='', default="http://localhost:8081", required=False)
    parser.add_argument('-a', '--user', help='', default="admin", required=False)
    parser.add_argument('-p', '--passwd', default="admin123", required=False)
    # parser.add_argument('-t', '--type', required=True)

    args = vars(parser.parse_args())
    
    nx_server = args["server"]
    nx_user = args["user"]
    nx_pwd = args["passwd"]
    # nx_type = args['type']

    return


def get_data(nx_type, nx_type_api):

    url = "{}/{}/{}" . format(nx_server, base_url, nx_type_api)

    print("* get data for : " + nx_type + " [" + url + "]")

    req = requests.get(url, auth=(nx_user, nx_pwd), verify=False)

    if req.status_code == 200:
        res = req.json()
        write_file(nx_type, res)
    else:
        res = "Error fetching data"

    if nx_type == 'blob':
        print('getting blob paths')
        get_blobpaths(res)

    return res


def get_blobpaths(json):
    for blob in json:
        name = blob['name']
        type = blob['type']

        if type == 'File' and not name == 'default':
            blob_url = "{}/{}" . format(blobpath_api, name)
            get_data("blob_" + name, blob_url)

    return


def write_file(type, json_data):
    output_file = "{}/{}{}".format(output_dir, type, ".json")
    json_formatted = json.dumps(json_data, indent=2)
    
    with open(output_file, 'w') as outfile:
        json.dump(json_data, outfile, indent=2)
    
    print("config saved to file: " + output_file)

    return


def main():
    get_args()

    for nx_type in endpoints:
        get_data(nx_type, endpoints[nx_type])



if __name__ == '__main__':
    main()
