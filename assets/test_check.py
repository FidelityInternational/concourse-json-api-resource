#!/usr/bin/env python

import pytest
import requests
import requests_mock
import check

class TestPayloadVars:
    def test_incomlete_payload(self):
        with pytest.raises(SystemExit):
            check.extract_vars_from_payload('{"source": {"url": "https://some.url/", "verify_ssl": "true", "auth_token":"bearer_token", "post_data":"{\"code\": \"GET_SOME_DATA\"}", "json_path": "/some/json/path"}')

    def test_good_payload(self):
            url, verify_ssl, auth_token, post_data, content_type, json_path = check.extract_vars_from_payload({"source": {"url": "https://some.url", "verify_ssl": "true", "auth_token":"some_auth_token", "post_data":"{\"code\": \"GET_SOME_DATA\"}", "content_type":"application/json", "json_path":"/some/json/path"}})
            assert url == "https://some.url"
            assert verify_ssl == "true"
            assert auth_token == "some_auth_token"
            assert post_data == "{\"code\": \"GET_SOME_DATA\"}"
            assert content_type == "application/json"
            assert json_path == "/some/json/path"

class TestAPIResponse:
    def test_request_sent(self, requests_mock):
        requests_mock.post('http://some.url', text='response_data', request_headers={'Authorization': 'bearer_token', 'Content-Type': 'application/json'})
        assert 'response_data' == check.get_response_from_api("http://some.url", "False", "bearer_token", "{\"code\": \"GET_SOME_DATA\"}", "application/json")

    def test_non_200_status(self, requests_mock):
        with pytest.raises(SystemExit):
            requests_mock.post('http://some.url', text='things_broke', status_code="404", request_headers={'Authorization': 'bearer_token', 'Content-Type': 'application/json'})
            check.get_response_from_api("http://some.url", "False", "bearer_token", "{\"code\": \"GET_SOME_DATA\"}", "application/json")

