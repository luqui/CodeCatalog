"""
CodeCatalog module.
"""
import httplib

cache = {}

def get(address):
    """
    Get a snippet from the CodeCatalog by address.
    """
    # Memory cache
    global cache
    code = cache.get(address)
    if code is not None:
        return code
    
    # TODO: Hard-drive cache
    
    # Get the data from CodeCatalog
    http_connection = httplib.HTTPConnection('127.0.0.1', 8000)
    http_connection.request("GET", "/" + address + "/raw/")
    contents = http_connection.getresponse()
    snippet_raw = contents.read(contents.length)
    snippet_compiled = compile(snippet_raw, '<string>', 'exec')
    exec(snippet_compiled)
    code = eval(snippet_compiled.co_names[0])
    cache[address] = code
    return code