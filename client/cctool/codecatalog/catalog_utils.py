import re

# CodeCatalog Snippet http://www.codecatalog.net/20/1/
def maximum_by(measure, xs):
    maxx = xs[0]
    maxm = measure(maxx)
    for x in xs[1:]:
        xm = measure(x)
        if xm > maxm:
            maxx = x
            maxm = xm
    return maxx
# End CodeCatalog Snippet

# CodeCatalog Snippet http://www.codecatalog.net/43/2/
def wrap_fields(wrapper, dictionary):
    ret = {}
    for (k,v) in dictionary.items():
        if k in wrapper:
            ret[k] = wrapper[k](v)
        else:
            ret[k] = v
    return ret
# End CodeCatalog Snippet

# CodeCatalog Snippet http://www.codecatalog.net/24/2/
def initial_whitespace(line):
    return re.search(r'^\s*', line).group(0)
# End CodeCatalog Snippet

# CodeCatalog Snippet http://www.codecatalog.net/26/10/
def strip_indent(text):
    lines = text.splitlines()
    all_ws = re.compile('^\s*$')
    lengths = [ len(initial_whitespace(l)) for l in lines if not all_ws.match(l) ]
    if not lengths:
        return ("", "")
    initial = min(lengths)
    ret = ('\n'.join(map(lambda l: l[initial:], lines)), " " * initial)
    return ret
# End CodeCatalog Snippet

# CodeCatalog Snippet http://www.codecatalog.net/28/1/
def indent_by(indent, text):
    return '\n'.join(map(lambda s: indent + s, text.splitlines())) + '\n'
# End CodeCatalog Snippet

# CodeCatalog Snippet http://www.codecatalog.net/63/2/
def normalize_code(code):
    (s,indent) = strip_indent(code)
    return (s.strip() + "\n", indent)
# End CodeCatalog Snippet
