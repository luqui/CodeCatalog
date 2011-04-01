import sys
import os
from os import path
import urllib
import httplib
import json
import catalog_utils
import re
import difflib

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

# CodeCatalog Snippet http://codecatalog.net/189/
line_comment_map = {
    'python': '#',
    'javascript': '//',
}
# End CodeCatalog Snippet

# CodeCatalog Snippet http://codecatalog.net/171/
file_extension_map = {
    "python": "py",
    "javascript": "js"
}
# End CodeCatalog Snippet


class CodeCatalogClient:
    
    HOST_ADDRESS = 'www.codecatalog.net'
    def __init__(self):
        self._conn = None

    @property
    def _connection(self):
        if self._conn is None:
            self._conn = JSONClient(self.HOST_ADDRESS)
        return self._conn

    @staticmethod
    def _tag_snippet(id, code, indent="", language="python"):
        return indent + line_comment_map[language] + " CodeCatalog Snippet http://codecatalog.net/" + str(id) + "/\n" + \
               code + \
               indent + line_comment_map[language] + " End CodeCatalog Snippet\n"

    def new(self, name, summary, code, language="python"):
        """
        Create a new spec and add it and a new snippet for that spec to the CodeCatalog.
        
        name: the name of the spec.
        summary: the spec summary.
        code: the raw code for the snippet.
        language: a string representing the language of the snippet. "python" is the default.
        """
        spec_info = self._connection.post('/api/new/spec/', 
        {
            'name': name,
            'summary': summary,
        })
        spec_id = spec_info['versionptr']
        
        (snip_id, code_formatted) = self.update(spec_id, code, language=language)
        return (spec_id, snip_id, code_formatted)
    
    def add(self, spec_id, code, language="python"):
        """
        Add a new snippet to an existing spec.
        
        spec_id: the id of the spec (int).
        code: the raw code for the snippet
        language = the language of the snippet ("python" is the default).
        """
        (code_normalized,_) = catalog_utils.normalize_code(code)
        
        snip_info = self._connection.post('/api/new/snippet/', { 
            'spec_versionptr': spec_id,
            'code': normalized,
            'language': language,
        })
        snip_id = snip_info['version']
        
        return (snip_id, code_normalized)

    def get(self, snip_id):
        """
        Get the snippet associated with a given spec id.
        """
        snip_info = self._connection.get('/api/snippet/' + str(snip_id) + '/')
        tagged_snip = self._tag_snippet(snip_info['version'], snip_info['code'], language=snip_info['language'])
        return tagged_snip

    def check_and_update(self, snip_id, newcode):
        """
        Check a snippet code-block against the CodeCatalog database and return the latest
        version.  This will update the catalog version to the given code if it was at tip
        when modified.
        """
        (newcode_norm, indent) = catalog_utils.normalize_code(newcode)
    
        snip = self._connection.get('/api/snippet/' + str(snip_id) + '/')
        latest = self._connection.get('/api/snippets/' + str(snip['versionptr']) + '/active/')
        
        up_to_date = latest['version'] <= snip['version']
        changes = newcode_norm != snip['code']
    
        if up_to_date:
            if changes:
                sys.stderr.write("*** Uploading changes to " + str(snip_id) + "\n")
                newsnip = self._connection.post('/api/new/snippet/', {
                    'spec_versionptr': snip['spec_versionptr'],
                    'code': newcode_norm,
                    'language': snip['language'],
                    'versionptr': snip['versionptr'],
                    'dependencies': ','.join(map(str, snip['dependencies'])),
                })
                return self._tag_snippet(newsnip['version'], newcode, indent=indent, language=snip['language'])
            else:
                # Completely unchanged.  Don't even move your lips.
                return self._tag_snippet(snip_id, newcode, indent=indent, language=snip['language'])
        else:
            if not changes or re.match(r'^\s*$', newcode):
                sys.stderr.write("*** Downloading changes to " + str(snip_id) + "\n")
                return self._tag_snippet(latest['version'], catalog_utils.indent_by(indent,latest['code']), indent=indent, language=latest['language'])
            else:
                sys.stderr.write("*** Snippet " + str(snip_id) + " is not up-to-date but has changes.  Leaving be.\n")
                return self._tag_snippet(snip_id, newcode, indent=indent, language=snip['language'])
            
    def search(self, *args):
        """
        Search the database for a sequence of strings.  Returns a list of result specs.
        """
        text = ' '.join(args)
        results = self._connection.get('/api/search/', { 'q': text })
        return results

def _partition_around_catalog_block(code, tag_start, tag_end):
    """
    Parse a block of code and return a tuple of (code, (snip_id, snippet), next).
    """
    (last_section, _, cursor) = code.partition(tag_start)
    if not cursor:
        return (last_section, (None, ""), "")
    (snip_id_str, _, cursor) = cursor.partition("/")
    snip_id = int(snip_id_str)
    cursor = cursor.lstrip()
    (snippet, _, cursor) = cursor.partition(tag_end)
    (_,_,next_section) = cursor.partition("\n")
    return (last_section, (snip_id, snippet), next_section)

def _update_file(catalog_client, language, fqn):
    """
    Update a source file to keep it synced with the CodeCatalog.
    """
    tag_start = line_comment_map[language] + " CodeCatalog Snippet http://codecatalog.net/"
    tag_end = line_comment_map[language] + " End CodeCatalog Snippet"
    
    new_code = None
    f = None
    f_copy = None
    print "Checking: {0}...".format(fqn)
    try:
        f = open(fqn, 'r')
        code = f.read()
        new_code = ""
        cursor = code
        update_required = False
        while True:
            if not cursor:
                break
            (last_section, (snippet_id, snippet), cursor) = _partition_around_catalog_block(cursor, tag_start, tag_end)
            new_code += last_section
            if not snippet:
                break
            print("Found www.codecatalog.net/{0}.".format(snippet_id))
            
            new_snippet = catalog_client.check_and_update(snippet_id, snippet)
            new_code += new_snippet
            (_, (new_snippet_id, new_snippet), _) = _partition_around_catalog_block(new_snippet, tag_start, tag_end)
            
            if new_snippet != snippet:
                new_version = True
            else:
                new_version = False
            if new_version or new_snippet_id != snippet_id:
                update_required = True
                differ = difflib.Differ()
                if new_version:
                    diff = differ.compare(new_snippet.split("\n"), snippet.split("\n"))
                else:
                    old_version = catalog_client.get(snippet_id)
                    (_,(_,old_version),_) = _partition_around_catalog_block(old_version)
                    diff = differ.compare(new_snippet.split("\n"), old_snippet.split("\n"))
    
                print "Updated snippet {0}...".format(new_snippet_id)
                print "Diff:\n ********************************************\n"
                for item in diff:
                    print item + "\n"
                print "*******************************************\n"
            else:
                print "--->Already at tip."
        
        if update_required:
            f.close()
            f = open(fqn, "w")
            f.write(new_code)
        f.close()
        f = None
        if update_required:
            f_copy = open(fqn + "~", 'w')
            f_copy.write(code)
            f_copy.close()
            f_copy = None
    finally:
        if f is not None:
            f.close()
        if f_copy is not None:
            f_copy.close()
    return new_code

def _scan_directory(data, directory, _):
    """
    Scan a directory for files and use CodeCatalog to update any source 
    files of the given language type.
    data: a tuple of (CatalogClient, language), where language is a str.
    directory: the directory to search.
    """
    import glob
    (catalog_client, language) = data
    for file_name in glob.glob1(directory, "*." + file_extension_map[language]):
        _update_file(catalog_client, language, os.path.join(directory, file_name))

def update_directory(code_directory, language="python"):
    """
    Scan a directory for changes to CodeCatalog snippets in source files of
    the type specified by the language str. Updates will be pulled from the server if there
    are new versions of any code you haven't changed.  Your changes will also
    be posted to the Code Catalog if you are still at tip. 
    """
    cc = CodeCatalogClient()
    _scan_directory_file((cc, language), code_directory, None)

def update_project(code_directory, language="python"):
    """
    Scan all the directories under a root "project" directory for updates to
    CodeCatalog snippets.  Updates will be pulled from the server if there
    are new versions of any code you haven't changed.  Your changes will also
    be posted to the Code Catalog if you are still at tip.
    """
    import os.path
    cc = CodeCatalogClient()
    os.path.walk(code_directory, _scan_directory, (cc, language))