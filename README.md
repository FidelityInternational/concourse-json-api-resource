# concourse-json-api-resource

A concourse resource for querying JSON based API over HTTP.

This resource implements `check`, `in` and `out` functions.

The 'check' step queries the API and will search for a `dpath` style dictionary path within the JSON response obtained from the API. The `json_path` parameter is used to select which value from the JSON response will be used as the resource `version` which is sent back to Concourse.

This resource only implements POST requests to an API. We didn't require GET functionality for the API we're talking to when we created this resource, so we never implemented it. (Pull requests are welcomed if you want to add the functionality)

This resource accepts the following inputs:
`source.url` : The URL to send queries to
`source.verify_ssl` : True or False (to skip SSL verification checks)
`source.auth_token` : Bearer token to be used when communicating with `source.url`
`source.post_data` : The data to be sent to the `source.url` as part of a POST request.
`source.content_type` : Set the content type to use in the headers (e.g. `application/json`)
`source.json_path` : A `dpath` style notation for where to find the `version` data within the json for the response to Concourse (e.g. '/data/0/version_id')

## development

Unit tests exist for all functions.
Run `pytest` to confirm that all tests pass before you make any changes, and run it again after changes to confirm that you've not broken anything.

To test things out on the command line (outside of a Concourse pipeline) when doing development work, you will need to supply a suitable `payload` on stdin.

e.g `echo '{"source": {"url": "https://some.url/some/path/to/use", "verify_ssl": "False", "auth_token":"<bearer_token>", "post_data":"{\"code\": \"CALL_TO_API_FUNCTION\"}", "content_type":"application/json", "json_path":"/path/to/key/in/json/dict"}}' | ./check.py`
