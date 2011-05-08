import sys
import os
from os import path
# CodeCatalog Snippet http://www.codecatalog.net/112/312/
import urllib
# End CodeCatalog Snippet

# CodeCatalog Snippet http://www.codecatalog.net/114/317/
import httplib
# End CodeCatalog Snippet

# CodeCatalog Snippet http://www.codecatalog.net/108/306/
import json
# End CodeCatalog Snippet

import catalog_utils
import re
import difflib

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

# CodeCatalog Snippet http://www.codecatalog.net/33/483/
language_to_line_comment_map = {
    'python': '#',
    'javascript': '//',
    'haskell': '--',
}
# End CodeCatalog Snippet

# CodeCatalog Snippet http://www.codecatalog.net/69/485/
language_to_file_extension_map = {
    "python": "py",
    "javascript": "js",
    "haskell": "hs",
}
# End CodeCatalog Snippet

# CodeCatalog Snippet http://www.codecatalog.net/102/496/
language_list = [ k for k in language_to_line_comment_map.keys() if k in language_to_file_extension_map ]
# End CodeCatalog Snippet

# CodeCatalog Snippet http://www.codecatalog.net/104/297/
def filename_to_language(filename):
    """
    Given a filename, use the extension to determine
    the code-language and return the string associated
    with that language.
    """
    for language, extension in language_to_file_extension_map:
        if filename.rsplit(".")[1] == extension:
            return language
    return None
# End CodeCatalog Snippet

# CodeCatalog Snippet http://www.codecatalog.net/106/341/
class Version:
    """
    The version of a snippet in the form versionptr/version.
    """
    def __init__(self, versionptr, version):
        self.versionptr = versionptr
        self.version = version
    
    def __str__(self):
        return "{0}/{1}".format(self.versionptr, self.version)
# End CodeCatalog Snippet

from collections import namedtuple

Spec = namedtuple('Spec', ('version', 'name', 'summary', 'description'))
Snippet = namedtuple('Snippet', ('version', 'code', 'language', 'dependencies', 'spec_versionptr'))

# CodeCatalog Snippet http://www.codecatalog.net/134/351/
def maximum_by(f, lst):
    (bestx,xs) = (lst[0],lst[1:])
    bestf = f(bestx)
    for x in xs:
        fx = f(x)
        if fx > bestf:
            (bestf,bestx)=(fx,x)
    return bestx
# End CodeCatalog Snippet

# CodeCatalog Snippet http://www.codecatalog.net/136/362/
def detect_by_pattern(text, patterns):
    scores = {}
    for k,pats in patterns.items():
        scores[k] = 0
        for p in pats:
            scores[k] += len(p.findall(text))
    
    return maximum_by(lambda (k,v): v, scores.items())[0]
# End CodeCatalog Snippet


# CodeCatalog Snippet http://www.codecatalog.net/138/481/
language_patterns = {
    'python': [
        re.compile(r'def\s+\w+\s*\(.*:\s*$', re.MULTILINE),
        re.compile(r'for\s+\w+\s+in\s+\w+\s*:\s*$', re.MULTILINE),
        re.compile(r'if\s+.*:\s*$', re.MULTILINE),
    ],
    'javascript': [
        re.compile(r'var\s+\w+\s*=', re.MULTILINE),
        re.compile(r'function\s+(?:\w+)?\s*\([\w\s,]*\)\s*{'),  #not multiline
        re.compile(r'for\s*\((?:\s*var\s)?\s*\w+\s+in\s+.*\)', re.MULTILINE),
    ],
    'haskell': [
        re.compile(r'^\w+\s*(?:,\s*\w+\s*)*::.*->.*', re.MULTILINE),
        re.compile(r'^\w+\s*=', re.MULTILINE),
        re.compile(r'^\s*where', re.MULTILINE),
        re.compile(r'where\s*$', re.MULTILINE),
    ],
}
# End CodeCatalog Snippet

# CodeCatalog Snippet http://www.codecatalog.net/140/373/
def detect_language(text):
    return detect_by_pattern(text, language_patterns)
# End CodeCatalog Snippet


def format_snippet(snippet, indent=""):
    leader = indent + language_to_line_comment_map[snippet.language]
    return "{0} CodeCatalog Snippet http://www.codecatalog.net/{1}/\n".format(
                 leader, snippet.version) + \
           snippet.code + \
           "{0} End CodeCatalog Snippet\n".format(leader);

# CodeCatalog Snippet http://www.codecatalog.net/142/418/
def partition(pattern, text):
    m = re.search(pattern, text)
    if m:
        return (text[0:m.start()], m.groups(), text[m.end():])
    else:
        return None
# End CodeCatalog Snippet


def partition_region(startre, stopre, text):
    p1 = partition(startre, text)
    if p1 is None: return None
    p2 = partition(stopre, p1[2])
    if p2 is None: return None
    return (p1[0], p1[1], p2[0], p2[1], p2[2])


def partition_snippet(text):
    open_pattern = re.compile(r'^.*CodeCatalog[ \t]+Snippet[ \t]+http://(?:www\.)?codecatalog.net/(\d+)(?:/(\d+))?/?[ \t]*\n', re.MULTILINE)
    close_pattern = re.compile(r'^.*End[ \t]+CodeCatalog[ \t]+Snippet[ \t]*\n', re.MULTILINE)

    r = partition_region(open_pattern, close_pattern, text)
    if r is None: return None
    
    (before, opendelim, code, closedelim, after) = r
    (code_norm, indent) = catalog_utils.normalize_code(code)

    if opendelim[1] is not None:
        version = Version(opendelim[0], opendelim[1])
    else:
        # old style
        version = Version(None, opendelim[0])

    snippet = Snippet(version  = version,
                      code     = code_norm,
                      language = detect_language(code_norm),
                      dependencies = [],
                      spec_versionptr = None)

    return (before, (snippet, indent), after)

# CodeCatalog Snippet http://www.codecatalog.net/144/381/
def case(proj, value, cases):
    return cases[proj(value)](value)
# End CodeCatalog Snippet


def check_changes(client, snippet):
    orig = client.get_snippet(snippet.version)
    new = client.get_snippet(Version(orig.version.versionptr, None))
    
    if orig.version.version == new.version.version:
        # we're at latest, see if we have changes
        if orig.code == snippet.code:
            # no changes
            return namedtuple('Unchanged', ('orig',))(orig)
        else:
            return namedtuple('Upload', ('orig', 'local'))(orig, snippet)
    else:
        # we're not at latest, see if we have changes
        if new.code == snippet.code:
            # fast forward
            return namedtuple('FastForward', ('orig', 'new'))(orig, new)
        elif orig.code == snippet.code:
            # no changes
            return namedtuple('Download', ('orig', 'new'))(orig, new)
        else:
            # uh oh
            return namedtuple('Conflict', ('orig', 'new', 'local'))(orig, new, snippet)

def process_file_contents(formatter, text):
    """A formatter is a function that takes a snippet and returns some text
    that it should be rendered as.  formatter is allowed to have side effects,
    to ask the user about things and consult the server.
    """
    result = ""
    while True:
        r = partition_snippet(text)
        if r is None: return result + text
        
        (before, (snippet,indent), after) = r
        result += before
        result += catalog_utils.indent_by(indent, formatter(snippet))
        text = after

def get_diff(old, new):
    return '\n'.join(difflib.unified_diff(old.code.splitlines(), new.code.splitlines(), lineterm="", n=10)) \
         + '\n'

def patchup_snippet(orig, local):
    newlocal = Snippet(**dict(local._asdict(), version=orig.version))
    assert(newlocal.version==orig.version)
    return newlocal

def confirmation_formatter(client):
    def unchanged(orig):
        print "Snippet {0} unchanged.".format(orig.version)
        return format_snippet(orig)
    
    def upload(orig, local):
        print "Snippet {0} changed locally.".format(orig.version)
        print
        print get_diff(orig, local)
        print
        print "Upload changes?"
        print "  (y) Upload"
        print "  (n) Leave alone"
        print "  (r) Revert"
        answer = None
        while answer != 'y' and answer != 'n' and answer != 'r':
            answer = raw_input("?")

        if answer == 'y':
            print "Uploading changes."
            snip = client.new_snippet(orig.spec_versionptr, local.code, orig.language, orig.dependencies, source=orig)
            print "Done."
            return format_snippet(snip)
        elif answer == 'n':
            print "Kept local version."
            return format_snippet(patchup_snippet(orig, local))
        elif answer == 'r':
            print "Reverted to version {0}".format(orig.version)
            return format_snippet(orig)            

    def download(orig, new):
        print "Snippet {0} changed remotely.".format(orig.version)
        print
        print get_diff(orig, new)
        print
        print "Download changes?"
        print "  (y) Download"
        print "  (n) Leave alone"
        answer = None
        while answer != 'y' and answer != 'n':
            answer = raw_input("?")
        
        if answer == 'y':
            print "New version installed."
            return format_snippet(new)
        elif answer == 'n':
            print "Kept local version."
            return format_snippet(orig)
    
    def conflict(orig, new, local):
        print "Snippet {0} merge conflict.".format(orig.version)
        print
        print "******* LOCAL CHANGES ********"
        print get_diff(orig, local)
        print "******************************"
        print
        print "******* REMOTE CHANGES *******"
        print get_diff(orig, new)
        print "******************************"
        print
        print "What to do?"
        print "  (remote) DOWNLOAD remote changes, destroying local changes"
        print "  (local)  UPLOAD local changes, destroying remote changes"
        print "  (ignore) KEEP local changes, but do not upload or download anything"
        print "  (both)   KEEP them both, and let me work out the conflict"
        answer = None
        while answer != 'remote' and answer != 'local' and answer != 'ignore' and answer != 'both':
            answer = raw_input("?")
        
        if answer == 'remote':
            print "Local changes ignored, new version installed."
            return format_snippet(new)
        elif answer == 'local':
            print "Remote changes ignored, overwriting with local version."
            snip = client.new_snippet(orig.spec_versionptr, local.code, orig.language, orig.dependencies, source=orig)
            return format_snippet(snip)
        elif answer == 'ignore':
            print "Left it alone."
            return format_snippet(patchup_snippet(orig, local))
        elif answer == 'both':
            print "Both versions inserted, please resolve manually."
            return "<<<<<<<<<<< MERGE CONFLICT >>>>>>>>>>>\n" + \
                   format_snippet(new) + format_snippet(local) + \
                   "<<<<<<<<< END MERGE CONFLICT >>>>>>>>>\n"
    
    def fastforward(orig, new):
        print "Fast Forward from {0} to {1}".format(orig.version, new.version);
        print "The code didn't change, but the version did."
        print
        print new.code
        print
        print "OK to tag this snippet with the latest version number?"
        answer = None
        while answer != 'y' and answer != 'n':
            answer = raw_input("?")
        
        if answer == 'y':
            print "Code retagged with version {0}".format(new.version)
            return format_snippet(new)
        else:
            print "Left it as it was."
            return format_snippet(orig.version)

    def formatter(snippet):    
        changes = check_changes(client, snippet)
        return case(lambda x: x.__class__.__name__, changes, {
            'Unchanged': lambda t: unchanged(*t),
            'Upload': lambda t: upload(*t),
            'Download': lambda t: download(*t),
            'Conflict': lambda t: conflict(*t),
            'FastForward': lambda t: fastforward(*t),
        })
    return formatter

def update_file(formatter, filename):
    fh = open(filename, 'r')
    contents = fh.read()
    fh.close()
    processed = process_file_contents(formatter, contents)
    if processed != contents:
        backup = open(filename + "~", 'w')
        backup.write(contents)
        backup.close()
        fh = open(filename, 'w')
        fh.write(processed)
        fh.close()

def update_directory(formatter, directory, language=None):
    import glob
    def _do_scan(language):
        for filename in glob.glob1(directory, "*." + language_to_file_extension_map[language]):
            fullpath = os.path.join(directory, filename)
            print "Scanning " + fullpath
            update_file(formatter, fullpath)
    
    if language is None:
        for language in language_list:
            _do_scan(language)
    else:
        _do_scan(language)

def update_project(formatter, directory, language=None):
    import os.path
    os.path.walk(directory, 
        lambda arg,dirname,names: update_directory(formatter, dirname, language),
        None)
    
def update_project_interactive(directory="."):
    formatter = confirmation_formatter(Client())
    update_project(formatter, directory)

# CodeCatalog Snippet http://www.codecatalog.net/154/423/
def merge(dict1, dict2):
    return dict(dict1, **dict2)
# End CodeCatalog Snippet

class Client:
    """
    An object that manages requests to the online catalog.
    """
    def __init__(self, user, api_key, host='www.codecatalog.net'):
        self._connection = JSONClient(host)
        self.host = host
        self.user = user
        self.api_key = api_key

    def _spec_info_to_spec(self, spec_info):
        return Spec(version     = Version(spec_info['versionptr'], spec_info['version']),
                    name        = spec_info['name'],
                    summary     = spec_info['summary'],
                    description = spec_info['description'])

    def _snip_info_to_snippet(self, snip_info):
        return Snippet(version = Version(snip_info['versionptr'], snip_info['version']),
                       code            = snip_info['code'],
                       language        = snip_info['language'],
                       dependencies    = snip_info['dependencies'],
                       spec_versionptr = snip_info['spec_versionptr'])

    def new_spec(self, name, summary, description, source=None):
        """
        Creates a new spec with the given fields. If source is given,
        then the new spec is assumed to be an edit of source (which is
        itself a Spec)
        """

        q = {
            'name': name,
            'summary': summary,
            'description': description,
            'user': self.user,
            'api_key': self.api_key,
        }
        if source is not None:
            q['versionptr'] = source.version.versionptr
        
        spec_info = self._connection.post('/api/new/spec/', q)
        if 'error' in spec_info:
            raise RuntimeError(spec_info.error)
        
        return self._spec_info_to_spec(merge(q,spec_info))

    def get_spec(self, version):
        if version.version is not None:
            spec_info = self._connection.get('/api/spec/' + str(version.version) + '/')
        else:
            spec_info = self._connection.get('/api/specs/' + str(version.versionptr) + '/active/')

        return self._spec_info_to_spec(spec_info)
    
    def new_snippet(self, spec_versionptr, code, language, dependencies=[], source=None):
        (code_norm, indent) = catalog_utils.normalize_code(code)
        q = {
            'spec_versionptr': spec_versionptr,
            'code': code_norm,
            'language': language,
            'dependencies': ','.join(map(str, dependencies)),
            'user': self.user,
            'api_key': self.api_key,
        }
        if source is not None:
            q['versionptr'] = source.version.versionptr
        
        snip_info = self._connection.post('/api/new/snippet/', q)
        if 'error' in snip_info:
            raise RuntimeError(snip_info['error'])
        
        return self._snip_info_to_snippet(merge(q,snip_info))

    def get_snippet(self, version):
        if version.version is not None:
            snip_info = self._connection.get('/api/snippet/' + str(version.version) + '/')
        else:
            snip_info = self._connection.get('/api/snippets/' + str(version.versionptr) + '/active/')
        
        return self._snip_info_to_snippet(snip_info)
    
    def assemble_spec(self, versionptr):
        snips = self._connection.get('/api/specs/' + str(versionptr) + '/assemble/')
        return map(self._snip_info_to_snippet, snips)

    def search(self, text):
        """
        Search the database for a string.  Returns a list of spec "skeletons"; they only have 
        a version, name, and summary.
        """
        results = self._connection.get('/api/search/', { 'q': text })
        for r in results:
            r['version'] = Version(r['versionptr'], None)
        return results
