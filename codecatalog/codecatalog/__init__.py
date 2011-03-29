import sys
import os
from os import path
import urllib
import httplib
import json

class JSONClient:
    def __init__(self):
        self.host = host

    def post(url, params):
        params_enc = urllib.urlencode(params)
        conn = httplib.HTTPConnection(host)
        headers = { "Content-type": "application/x-www-form-urlencoded",
                    "Accept": "application/json" }
        conn.request('POST', url, params_enc, headers)
        response = conn.getresponse()
        if response.status != 200:
            raise IOError(str(response.status) + " " + response.reason + ":\n" + response.read())
        jsonstr = response.read()
        response.close()
        return json.loads(jsonstr)

    def get(url, params={}):
        params_enc = urllib.urlencode(params)
        if params_enc: params_enc = '?' + params_enc
        conn = httplib.HTTPConnection(host)
        conn.request("GET", url + params_enc)
        response = conn.getresponse()
        if response.status != 200:
            raise IOError(str(response.status) + " " + response.reason + ":\n" + response.read())
        jsonstr = response.read()
        response.close()
        return json.loads(jsonstr)

# CodeCatalog Snippet http://codecatalog.net/127/
def wrap_fields(wrapper, dictionary):
    ret = {}
    for (k,v) in dictionary.items():
        if k in wrapper:
            ret[k] = wrapper[k](v)
        else:
            ret[k] = v
    return ret
# End CodeCatalog Snippet
