#!/usr/bin/env python

import os
import requests
import sys
import json
import dpath.util

def extract_vars_from_payload(payload):
    try:
        url=payload['source']['url']
        verify_ssl=payload['source']['verify_ssl']
        auth_token=payload['source']['auth_token']
        post_data=payload['source']['post_data']
        content_type=payload['source']['content_type']
        json_path=payload['source']['json_path']
        json_key=payload['source']['version_key']
        file_name=payload['source']['file_name']
    except (KeyError, TypeError) as e:
        print("Error processing payload from concourse")
        print("Required source parameters are url, verify_ssl, auth_token, post_data and content_type")
        print(e)
        sys.exit(1)
    return(url, verify_ssl, auth_token, post_data, content_type, json_path, json_key, file_name)

def get_response_from_api(url, verify_ssl, auth_token, post_data, content_type):
    # pylint: disable=no-member
    requests.packages.urllib3.disable_warnings() # Don't display python's warning about using a certificate manager module
    try:
        api_response=requests.post(url, post_data, verify=False, headers={'Authorization': auth_token, 'Content-Type': content_type}, timeout=5.0)
    except Exception as e:
        print(f"Failed to get response from API {url}")
        print(e)
        sys.exit(1)
    if api_response.status_code == 200:
        return(api_response.text)
    else:
        print(f"Non-200 response code ({api_response.status_code}) received from {url}")
        print(api_response.text)
        sys.exit(1)

def get_ref(response,json_path, json_key):
    try:
        data=json.loads(response)
        for obj in data[json_path]:
            return (obj[json_key])
        return 0

    except Exception as e:
        print("Error while searching key " + json + " in JSON response")
        print(e)
        sys.exit(1)

def get_data(response, json_path):
    try:
        data=json.loads(response)
        for obj in data[json_path]:
            return(obj)
    except Exception as e:
        print("Unable to find the `json_path` within decoded JSON response")
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    try:
        payload=sys.stdin.read()
        url, verify_ssl, auth_token, post_data, content_type, json_path, json_key, file_name = extract_vars_from_payload(json.loads(payload))
        response=get_response_from_api(url, verify_ssl, auth_token, post_data, content_type)
        version=str(get_ref(response, json_path, json_key))
        data=get_data(response, json_path)
        metadata=[]
        if data:
            with open(sys.argv[1]+'/'+file_name, 'w') as outfile:
                outfile.write(json.dumps(data))
                outfile.close()
            for key in data.keys():
                metadata.append({"name": key, "value": str(data[key])})
        else:
            metadata.append({"name": "message", "value": "No data received from API"})

        print(json.dumps({"version":{"ref":version}, "metadata":metadata}))

    except Exception as e:
        print("Unexpected error encountered in `main`")
        print(e)
        sys.exit(1)
