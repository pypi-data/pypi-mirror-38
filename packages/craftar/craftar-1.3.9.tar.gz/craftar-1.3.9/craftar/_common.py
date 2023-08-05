#  (C) Catchoom Technologies S.L.
#  Licensed under the MIT license.
#  https://github.com/catchoom/craftar-python/blob/master/LICENSE
#  All warranties and liabilities are disclaimed.

"Provides common internal utility fuctions for accessing CraftAR's API"

import json
import re
import requests
try:
    from urllib import urlencode
except ImportError:
    # Fallback to maintain backward compatibility with Python 2
    from urllib.parse import urlencode
from craftar import settings

HEADERS = {
    'User-Agent': settings.USER_AGENT,
    'content-type': 'application/json',
}


def _validate(object_type=None, data=None, uuid=None):
    "Validate the parameters before asking the API"

    if object_type:
        assert object_type in settings.ALLOWED_OBJECT_TYPES, \
            "Wrong object_type: %s" % object_type
    if data:
        assert type(data) is dict, "Wrong data"
        assert data is not {}, "Empty data"
    if uuid:
        if object_type == 'token':
            uuid4hex = re.compile('[0-9a-f]{16}\Z', re.I)
            assert uuid4hex.match(uuid), "Wrong token: %s" % str(uuid)
        else:
            uuid4hex = re.compile('[0-9a-f]{32}\Z', re.I)
            assert uuid4hex.match(uuid), "Wrong uuid: %s" % str(uuid)


def _validate_response(response):
    "Validate the response from the API. Raise API, HTTP and url errors"
    try:
        # if there is an error message
        json_resp = response.json()
        if "error_message" in json_resp:
            msg = json_resp["error_message"]
        else:
            msg = json_resp["error"]
        raise Exception("Error %s: %s" % (response.status_code, msg))
    except (ValueError, KeyError):
        # if there is not error message, but there is an error
        response.raise_for_status()


def _parse_object(_object):
    "Return a parsed object. Ugly API urls are replaced by UUIDs"
    # remove resource_uri
    if "resource_uri" in _object:
        del _object["resource_uri"]

    # parse collection, item, app and version: set uuid instead of api uri
    keys_to_parse = ["collection", "item", "version", "app", "tag"]
    for key in keys_to_parse:
        if key in _object:
            _object[key] = _object[key].split("/")[-2]

    # parse collections and tags
    keys_to_parse = ["collections", "tags"]
    for key in keys_to_parse:
        if key in _object:
            _object[key] = map(lambda uri: uri.split("/")[-2], _object[key])

    return _object


def _get_url(api_key, object_type, uuid=None, limit=None, offset=None,
             filter=None, filters_dict=None):
    "Return a valid API url, based on the parameters"
    _validate(object_type=object_type, uuid=uuid)
    resource_name = object_type
    if uuid:
        resource_name += "/%s" % uuid

    url = "%s/api/%s/%s/?api_key=%s" % (settings.MANAGEMENT_HOSTNAME,
                                        settings.MANAGEMENT_API_VERSION,
                                        resource_name, api_key)
    if limit:
        url += "&limit=%s" % limit
    if offset:
        url += "&offset=%s" % offset
    if filter:
        if object_type == 'item' or object_type == 'token':
            url += "&collection__uuid=%s" % filter
        elif object_type == 'image':
            url += "&item__uuid=%s" % filter
    if filters_dict and isinstance(filters_dict, dict):
        url += "&{}".format(urlencode(filters_dict))

    return url


def _get_object_list(api_key, object_type, limit=20, offset=0,
                     filter=None, filters_dict=None):
    "Get a list of objects"
    _validate(object_type=object_type)

    url = _get_url(api_key, object_type, None, limit, offset, filter,
                   filters_dict)
    response = requests.get(url)
    _validate_response(response)

    object_list = []
    for unparsed_object in response.json()["objects"]:
        parsed_object = _parse_object(unparsed_object)
        object_list.append(parsed_object)
    return object_list


def _get_object(api_key, object_type, uuid):
    "Get a single object"
    _validate(object_type=object_type, uuid=uuid)
    url = _get_url(api_key, object_type, uuid)
    response = requests.get(url)
    _validate_response(response)
    parsed_object = _parse_object(response.json())
    return parsed_object


def _create_object(api_key, object_type, data):
    "Create a single object without an attachment"
    _validate(object_type=object_type, data=data)
    response = requests.post(
        url=_get_url(api_key, object_type),
        data=json.dumps(data),
        headers=HEADERS,
    )
    _validate_response(response)
    parsed_object = _parse_object(response.json())
    if response.status_code == 201:
        return parsed_object


def _create_object_multipart(api_key, object_type, files, data):
    "Create a single object with an attachment (image file)"
    _validate(object_type=object_type, data=data)
    response = requests.post(
        url=_get_url(api_key, object_type),
        data=data,
        files=files,
    )
    _validate_response(response)
    parsed_object = _parse_object(response.json())
    if response.status_code == 201:
        return parsed_object


def _update_object(api_key, object_type, uuid, data):
    "Update a single object"
    _validate(object_type=object_type, data=data, uuid=uuid)
    response = requests.put(
        url=_get_url(api_key, object_type, uuid),
        data=json.dumps(data),
        headers=HEADERS,
    )
    _validate_response(response)
    return (response.status_code == 202)


def _update_object_multipart(api_key, object_type, uuid, files, data):
    "Update a single object with an attachment (image file)"
    _validate(object_type=object_type, data=data, uuid=uuid)
    response = requests.put(
        url=_get_url(api_key, object_type, uuid),
        data=data,
        files=files,
    )
    _validate_response(response)
    return (response.status_code == 202)


def _delete_object(api_key, object_type, uuid):
    "Update a single object"
    _validate(object_type=object_type, uuid=uuid)
    response = requests.delete(
        url=_get_url(api_key, object_type, uuid),
    )
    _validate_response(response)
    return (response.status_code == 204)
