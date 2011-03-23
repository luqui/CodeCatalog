#!/usr/bin/python

import httplib
import urllib
import json
import sys
import re

host = 'localhost:8000'

def post_json(url, params):
    conn = httplib.HTTPConnection(host)
    params_enc = urllib.urlencode(params)
    headers = { "Content-type": "application/x-www-form-urlencoded",
                "Accept": "application/json" }
    conn.request('POST', url, params_enc, headers)
    response = conn.getresponse()
    if response.status != 200:
        raise IOError(str(response.status) + " " + response.reason + ":\n" + response.read())
    jsonstr = response.read()
    response.close()
    return json.loads(jsonstr)

def get_json(url):
    conn = httplib.HTTPConnection(host)
    conn.request("GET", url)
    response = conn.getresponse()
    if response.status != 200:
        raise IOError(str(response.status) + " " + response.reason + ":\n" + response.read())
    jsonstr = response.read()
    response.close()
    return json.loads(jsonstr)

def tag_snippet(id, code):
    return "# Begin CodeCatalog Snippet http://codecatalog.net/" + str(id) + "/\n" + \
           code + \
           "\n# End CodeCatalog Snippet"

def cmd_post(*args, **opts):
    name = opts.get('name') or 'unnamed'
    summary = opts.get('summary') or ''
    language = opts.get('language') or 'python'
    code = sys.stdin.read().strip()
    
    spec = post_json('/api/new/spec/', { 
        'name': name, 
        'summary': summary,
    })
    snip = post_json('/api/new/snippet/', { 
        'spec_versionptr': spec['versionptr'],
        'code': code,
        'language': language,
    })

    print tag_snippet(snip['version'], code)

def cmd_get(*args, **opts):
    ver = args[0]
    ver = re.sub(r'^http://codecatalog.net/', '', ver)
    ver = re.sub(r'/$', '', ver)
    snip = get_json('/api/snippet/' + ver + '/')
    print tag_snippet(snip['version'], snip['code'])

commands = {
    'post': cmd_post,
    'get': cmd_get,
}

def main():
    argv = sys.argv
    cmd = argv[1]
    args = []
    opts = {}
    for arg in argv[2:]:
        m = re.match(r'--(\w+)', arg)
        if m:
            opts[m.group(1)] = True
            continue
        m = re.match(r'--(\w+)=(.*)', arg)
        if m:
            opts[m.group(1)] = m.group(2)
            continue
        args.append(arg)
        
    commands[cmd](*args, **opts)

if __name__ == '__main__':
    main()
