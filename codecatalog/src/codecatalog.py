#!/usr/bin/python

import httplib
import urllib
import json
import sys
import re
import webbrowser

host = 'localhost:8000'

def post_json(url, params):
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

def get_json(url, params={}):
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

def tag_snippet(id, code):
    return "# Begin CodeCatalog Snippet http://codecatalog.net/" + str(id) + "/\n" + \
           code + \
           "\n# End CodeCatalog Snippet"

def cmd_post(*args, **opts):
    name = opts.get('name') or 'unnamed'
    summary = opts.get('summary') or ''
    language = opts.get('language') or 'python'
    quiet = opts.get('quiet')
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

    if not quiet:
        webbrowser.open_new_tab('http://' + host + '/spec/' + str(spec['versionptr']) + '/')

    print tag_snippet(snip['version'], code)

def cmd_get(*args, **opts):
    ver = args[0]
    ver = re.sub(r'^http://codecatalog.net/', '', ver)
    ver = re.sub(r'/$', '', ver)
    snip = get_json('/api/snippet/' + ver + '/')
    print tag_snippet(snip['version'], snip['code'])

def cmd_search(*args, **opts):
    text = ' '.join(args)
    results = get_json('/api/search/', { 'q': text })
    for result in results:
        print "/" + str(result['versionptr']) + "/", result['name'], "-", result['summary']

commands = {
    'post': cmd_post,
    'get': cmd_get,
    'search': cmd_search,
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
