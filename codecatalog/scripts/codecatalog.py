#!/usr/bin/python

import httplib
import urllib
import json
import sys
import webbrowser
# CodeCatalog Snippet http://codecatalog.net/22/52/
import re
# End CodeCatalog Snippet

def cmd_sync(*args, **opts):
    snipid = None
    code = ""
    for line in sys.stdin:
        m = re.search(r'CodeCatalog Snippet http://codecatalog.net/(\d+)/', line)
        if m:
            code = ""
            snipid = int(m.group(1))
        elif snipid is None:
            sys.stdout.write(line)
        elif re.search(r'End CodeCatalog Snippet', line):
            catalog_client = codecatalog.CodeCatalogClient()
            sys.stdout.write(catalog_client.check_and_update(snipid, code))
            code = ""
            snipid = None
        else:
            code += line

def cmd_post(*args, **opts):
    name = opts.get('name') or 'unnamed'
    summary = opts.get('summary') or ''
    language = opts.get('language') or 'python'
    spec_id = opts.get('specid')
    quiet = opts.get('quiet')
    code = sys.stdin.read()
    
    if spec_id is None:
        (spec_id, snip_id, formatted_code) = catalog_client.new(name, summary, code, language)
    else:
        (snip_id, formatted_code) = catalog_client.add(spec_id, code)

    if not quiet:
        webbrowser.open_new_tab('http://' + host + '/spec/' + str(spec_id) + '/')

    sys.stdout.write(tag_snippet(snip_id, formatted_code, language=language))

def cmd_get(*args, **opts):
    ver = args[0]
    ver = re.sub(r'^http://codecatalog.net/', '', ver)
    ver = re.sub(r'/$', '', ver)
    
    code = catalog_client.get(ver)
    sys.stdout.write(code)

def cmd_search(*args, **opts):
    for result in results:
        print "/" + str(result['versionptr']) + "/", result['name'], "-", result['summary']

commands = {
    'post': cmd_post,
    'get': cmd_get,
    'sync': cmd_sync,
    'search': cmd_search,
}

def main():
    argv = sys.argv
    cmd = argv[1]
    args = []
    opts = {}
    for arg in argv[2:]:
        m = re.match(r'^--(\w+)$', arg)
        if m:
            opts[m.group(1)] = True
            continue
        m = re.match(r'^--(\w+)=(.*)$', arg)
        if m:
            opts[m.group(1)] = m.group(2)
            continue
        args.append(arg)
        
    commands[cmd](*args, **opts)

if __name__ == '__main__':
    main()
