# CodeCatalog Snippet http://www.codecatalog.net/112/312/
import urllib
# End CodeCatalog Snippet

# CodeCatalog Snippet http://www.codecatalog.net/114/317/
import httplib
# End CodeCatalog Snippet

# CodeCatalog Snippet http://www.codecatalog.net/110/323/
class JSONClient:
    def __init__(self, host):
        self._host = host

    def post(self, url, params):
        params_enc = urllib.urlencode(params)
        conn = httplib.HTTPConnection(self._host)
        headers = { "Content-type": "application/x-www-form-urlencoded",
                    "Accept": "application/json" }
        conn.request('POST', url, params_enc, headers)
        response = conn.getresponse()
        if response.status != 200:
            raise IOError(str(response.status) + " " + response.reason + ":\n" + response.read())
        jsonstr = response.read()
        response.close()
        return json.loads(jsonstr)

    def get(self, url, params={}):
        params_enc = urllib.urlencode(params)
        if params_enc: params_enc = '?' + params_enc
        conn = httplib.HTTPConnection(self._host)
        conn.request("GET", url + params_enc)
        response = conn.getresponse()
        if response.status != 200:
            raise IOError(str(response.status) + " " + response.reason + ":\n" + response.read())
        jsonstr = response.read()
        response.close()
        return json.loads(jsonstr)
# End CodeCatalog Snippet

import re
import sys
import json

client = JSONClient('www.codecatalog.net')

def subber(match):
    resp = client.get('/api/orm/', { 
        'request': json.dumps({
            'model': 'Snippet',
            'query': {
                'type': 'relation',
                'field': [ 'version', 'id' ],
                'relation': 'exact',
                'value': match.group(2),
            },
        }),
    })
    if len(resp) == 1:
        return "http://www.codecatalog.net/" + match.group(1) + "/" + str(resp[0]['serial']) + "/"
    else:
        url = "http://www.codecatalog.net/" + match.group(1) + "/" + match.group(2) + "/"
        sys.stderr.write("Couldn't find serial id for " + url)
        return url

for filename in sys.argv[1:]:
    sys.stderr.write("Processing " + filename)
    fh = open(filename, 'r')
    contents = fh.read()
    fh.close()

    processed = re.sub(r'http://www.codecatalog.net/(\d+)/(\d+)/', subber, contents)
    fh = open(filename, 'w')
    fh.write(processed)
    fh.close()
