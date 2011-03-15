"""
The CodeCatalog module provides access to the CodeCatalog's vast index of functions.
Code is cached both on your local hard-drive and in memory for better performance.
"""
import os
import os.path
import httplib
import re

_cache_directory = os.path.expanduser("~/_codecatalog/")
cache = {}

def _text_to_code(text):
    """
    Convert a block of text into the code it represents.
    It is assumed that the code is a single python function.
    """
    text = re.sub('\r', '', text)
    snippet_compiled = compile(text, '<string>', 'exec')
    exec(snippet_compiled)
    return eval(snippet_compiled.co_names[0])

def _filename(address):
    """
    Returns the expected local filename for a given CodeCatalog
    address.
    """
    return os.path.normpath("{0}{1}.cog".format(_cache_directory, address))

def _check_cache(address):
    """
    Check the cache for this snippet.
    """
    # Memory cache
    global cache
    code = cache.get(address)
    if code is not None:
        return code

    f = None
    try:
        f = open(_filename(address))
        return _text_to_code(f.read())
    except IOError:
        pass
    finally:
        if f is not None:
            f.close()
    return None

def _cache(address, code, snippet_raw):
    """
    Add the code for this snippet to the cache.
    """
    cache[address] = code
    if not os.path.exists(_cache_directory):
        os.mkdir(_cache_directory)
    f = open(_filename(address), 'w')
    f.write(snippet_raw)
    f.close()

def _get_from_catalog(address):
    """
    Get the snippet from CodeCatalog.
    """
    http_connection = httplib.HTTPConnection('codecatalog.net', 80)
    http_connection.request("GET", "/{0}/raw/".format(address))
    contents = http_connection.getresponse()
    snippet_raw = contents.read(contents.length)
    return snippet_raw, _text_to_code(snippet_raw)

def get(address):
    """
    Get a snippet from the CodeCatalog by address.
    """
    if isinstance(address, str):
        short_address = address.split("codecatalog.net/")
        if len(short_address) == 2:
            address = short_address[1].strip("/")
    code = _check_cache(address)
    if code is not None:
        return code
    
    snippet_raw, code = _get_from_catalog(address)
    _cache(address, code, snippet_raw)
    return code