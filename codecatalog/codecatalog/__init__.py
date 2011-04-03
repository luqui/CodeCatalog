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

# CodeCatalog Snippet http://codecatalog.net/102/294/
language_list = ["python", "javascript"]
# End CodeCatalog Snippet

# CodeCatalog Snippet http://codecatalog.net/33/299/
language_to_line_comment_map = {
    'python': '#',
    'javascript': '//',
}
# End CodeCatalog Snippet

# CodeCatalog Snippet http://codecatalog.net/69/298/
language_to_file_extension_map = {
    "python": "py",
    "javascript": "js"
}
# End CodeCatalog Snippet

# CodeCatalog Snippet http://codecatalog.net/104/297/
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


class Version:
    """
    The version of a snippet in the form versionptr/version.
    """
    def __init__(self, versionptr, version):
        self.versionptr = versionptr
        self.version = version
    
    def __str__(self):
        return "{0}/{1}/".format(self.versionptr, self.version)

class CodeCatalogClient:
    """
    An object that manages requests to the code catalog.
    """
    HOST_ADDRESS = 'www.codecatalog.net'
    def __init__(self):
        self._conn = None

    @property
    def _connection(self):
        if self._conn is None:
            self._conn = JSONClient(self.HOST_ADDRESS)
        return self._conn

    @staticmethod
    def _tag_snippet(versionptr, version, code, indent="", language="python"):
        line_comment = language_to_line_comment_map[language]
        return "{0}{1} CodeCatalog Snippet http://codecatalog.net/{2}/{3}/\n".format(
                indent, line_comment, str(versionptr), str(version)) + \
               code + \
               "{0}{1} End CodeCatalog Snippet\n".format(
                indent, line_comment)

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
        
        (version, code_formatted) = self.add(spec_id, code, language=language)
        return (spec_id, version, code_formatted)
    
    def add(self, spec_id, code, language="python"):
        """
        Add a new snippet to an existing spec.
        
        spec_id: the id of the spec (int).
        code: the raw code for the snippet
        language = the language of the snippet ("python" is the default).
        """
        (code_normalized, indent) = catalog_utils.normalize_code(code)
        
        snip_info = self._connection.post('/api/new/snippet/', { 
            'spec_versionptr': spec_id,
            'code': normalized,
            'language': language,
        })
        version = Version(snip_info['versionptr'], snip_info['version'])
        
        return (version, catalog_utils.indent_by(indent, code_normalized))

    def get(self, version):
        """
        Get the snippet associated with a given spec id.
        """
        snip_info = self._connection.get('/api/snippet/' + str(version.version) + '/')
        tagged_snip = self._tag_snippet(snip_info['versionptr'], snip_info['version'], snip_info['code'], language=snip_info['language'])
        return tagged_snip

    def check_and_update(self, version, code):
        """
        Check a snippet code-block against the CodeCatalog database and return the latest
        version.  This will update the catalog version to the given code if it was at tip
        when modified.
        """
        (code_norm, indent) = catalog_utils.normalize_code(code)
    
        snip = self._connection.get('/api/snippet/' + str(version.version) + '/')
        new_code = snip['code']
        latest = self._connection.get('/api/snippets/' + str(version.versionptr) + '/active/')
        
        latest_version = Version(latest['versionptr'], latest['version'])
        latest_code = latest['code']
        
        up_to_date = latest_version.version <= version.version
        changes = code_norm != new_code
    
        if up_to_date:
            if changes:
                sys.stderr.write("*** Uploading changes to {0}\n".format(version))
                new_snip = self._connection.post('/api/new/snippet/', {
                    'spec_versionptr': snip['spec_versionptr'],
                    'code': code_norm,
                    'language': snip['language'],
                    'versionptr': snip['versionptr'],
                    'dependencies': ','.join(map(str, snip['dependencies'])),
                })
                return self._tag_snippet(new_snip['versionptr'], new_snip['version'], 
                                         code, indent=indent, language=new_snip['language'])
            else:
                # Completely unchanged.
                return self._tag_snippet(latest_version.versionptr, latest_version.version, 
                                         code, indent=indent, language=snip['language'])
        else:
            if not changes or re.match(r'^\s*$', code):
                sys.stderr.write("*** Downloading changes: {0}->{1}\n".format(version, latest_version))
                return self._tag_snippet(latest_version.versionptr, latest_version.version, 
                                         catalog_utils.indent_by(indent, latest['code']), 
                                         indent=indent, language=latest['language'])
            else:
                sys.stderr.write("*** Snippet {0} is not up-to-date but has changes (New version: {1}).  Leaving be.\n".format(version, latest_version))
                return self._tag_snippet(version.versionptr, version.version, code, indent=indent, language=snip['language'])
            
    def search(self, *args):
        """
        Search the database for a sequence of strings.  Returns a list of result specs.
        """
        text = ' '.join(args)
        results = self._connection.get('/api/search/', { 'q': text })
        return results

    @staticmethod
    def _partition_around_catalog_block(code, tag_start, tag_end):
        """
        Parse a block of code and return a tuple of (code, (version, snippet), next).
        """
        (last_section, _, cursor) = code.partition(tag_start)
        if not cursor:
            return (last_section, (None, ""), "")
        (version_ptr_str, _, cursor) = cursor.partition("/")
        if cursor.startswith("\n"):
            # Old version where /version is the tag
            version_str = version_ptr_str
            version_ptr_str = "-1"
        else:
            # New version where /versionptr/version is the tag
            (version_str, _, cursor) = cursor.partition("/")
        version = Version(int(version_ptr_str), int(version_str))
        cursor = cursor.lstrip()
        (snippet, _, cursor) = cursor.partition(tag_end)
        (_,_,next_section) = cursor.partition("\n")
        return (last_section, (version, snippet), next_section)
    
    def update_file(self, filename, language=None):
        """
        Update a source file to keep it synced with the CodeCatalog.
        file_name: the fully-qualified filename to update.
        language: a string representing the language of the code file.
        """
        if language is None:
            language = filename_to_language(filename)
        
        line_comment = language_to_line_comment_map[language]
        tag_start = line_comment + " CodeCatalog Snippet http://codecatalog.net/"
        tag_end = line_comment + " End CodeCatalog Snippet"
        
        new_code = None
        f = None
        f_copy = None
        print "Checking: {0}...".format(filename)
        try:
            f = open(filename, 'r')
            code = f.read()
            new_code = ""
            cursor = code
            update_required = False
            while True:
                if not cursor:
                    break
                (last_section, (version, snippet), cursor) = self._partition_around_catalog_block(cursor, tag_start, tag_end)
                new_code += last_section
                if not snippet:
                    break
                print("Found www.codecatalog.net/{0}.".format(version))
                
                new_snippet = self.check_and_update(version, snippet)
                if new_snippet:
                    new_code += new_snippet
                else:
                    # In case we Failed to get from the server
                    new_code += snippet
                (_, (new_version, new_snippet), _) = self._partition_around_catalog_block(new_snippet, tag_start, tag_end)
                
                if new_snippet != snippet or new_version.version != version.version or version.versionptr < 0:
                    update_required = True
                    differ = difflib.Differ()
                    if new_version:
                        diff = differ.compare(new_snippet.split("\n"), snippet.split("\n"))
                    else:
                        old_version = catalog_client.get(snippet_id)
                        (_,(_,old_version),_) = _partition_around_catalog_block(old_version, tag_start, tag_end)
                        diff = differ.compare(new_snippet.split("\n"), old_snippet.split("\n"))
        
                    print "Updated snippet {0}...".format(new_version)
                    print "Diff:\n ********************************************\n"
                    for item in diff:
                        print item + "\n"
                    print "*******************************************\n"
                else:
                    print "--->Already at tip."
            
            if update_required:
                f.close()
                f = open(filename, "w")
                f.write(new_code)
            f.close()
            f = None
            if update_required:
                f_copy = open(filename + "~", 'w')
                f_copy.write(code)
                f_copy.close()
                f_copy = None
        finally:
            if f is not None:
                f.close()
            if f_copy is not None:
                f_copy.close()
        print("Done checking.")
        return new_code
    
    def _scan_directory(self, language, directory, _):
        """
        Scan a directory for files and use CodeCatalog to update any source 
        files of the given language type.
        data: a tuple of (CatalogClient, language), where language is a str.
        directory: the directory to search.
        """
        import glob
        def _do_scan(language):
            for filename in glob.glob1(directory, "*." + language_to_file_extension_map[language]):
                self.update_file(os.path.join(directory, filename), language=language)
        if language is None:
            for language in language_list:
                _do_scan(language)
        else:
            _do_scan(language)
    
    def update_directory(self, code_directory, language=None):
        """
        Scan a directory for changes to CodeCatalog snippets in source files of
        the type specified by the language str. Updates will be pulled from the server if there
        are new versions of any code you haven't changed.  Your changes will also
        be posted to the Code Catalog if you are still at tip.
        """
        self._scan_directory(language, code_directory, None)
    
    def update_project(self, code_directory, language=None):
        """
        Scan all the directories under a root "project" directory for updates to
        CodeCatalog snippets.  Updates will be pulled from the server if there
        are new versions of any code you haven't changed.  Your changes will also
        be posted to the Code Catalog if you are still at tip.
        """
        import os.path
        cc = CodeCatalogClient()
        os.path.walk(code_directory, self._scan_directory, language)