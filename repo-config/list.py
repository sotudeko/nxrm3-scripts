import sys
import json
import argparse
import requests
import os
import constants


def app_init():
    if not os.path.exists (constants.output_dir):
        os.mkdir(constants.output_dir)
    
    global nx_server, nx_user, nx_pwd, nx_type

    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--server', help='', default="http://localhost:8081", required=False)
    parser.add_argument('-a', '--user', help='', default="admin", required=False)
    parser.add_argument('-p', '--passwd', default="admin123", required=False)

    args = vars(parser.parse_args())
    
    nx_server = args["server"]
    nx_user = args["user"]
    nx_pwd = args["passwd"]

    return


def get_data(nx_type, nx_type_api):

    url = "{}/{}/{}" . format(nx_server, constants.base_url, nx_type_api)

    print("* get data for : " + nx_type + " [" + url + "]")

    req = requests.get(url, auth=(nx_user, nx_pwd), verify=False)

    if req.status_code == 200:
        res = req.json()
        write_file(nx_type, res)
    else:
        res = "Error fetching data"

    if nx_type == 'blob':
        get_blobpaths(res)

    return res


def get_blobpaths(json):
    for blob in json:
        name = blob['name']
        type = blob['type']

        if type == 'File' and not name == 'default':
            blob_url = "{}/{}" . format(constants.blobpath_api, name)
            get_data("blob_" + name, blob_url)

    return


def write_file(type, json_data):
    output_file = "{}/{}{}".format(constants.output_dir, type, ".json")
    json_formatted = json.dumps(json_data, indent=2)
    
    with open(output_file, 'w') as outfile:
        json.dump(json_data, outfile, indent=2)
    
    print("config saved to file: " + output_file)

    return


def main():
    app_init()

    for nx_type in constants.endpoints:
        get_data(nx_type, constants.endpoints[nx_type])



if __name__ == '__main__':
    main()
