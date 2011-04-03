import re

# CodeCatalog Snippet http://codecatalog.net/20/47/
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

# CodeCatalog Snippet http://codecatalog.net/43/127/
def wrap_fields(wrapper, dictionary):
    ret = {}
    for (k,v) in dictionary.items():
        if k in wrapper:
            ret[k] = wrapper[k](v)
        else:
            ret[k] = v
    return ret
# End CodeCatalog Snippet

# CodeCatalog Snippet http://codecatalog.net/24/61/
def initial_whitespace(line):
    return re.search(r'^\s*', line).group(0)
# End CodeCatalog Snippet

# CodeCatalog Snippet http://codecatalog.net/26/182/
def strip_indent(text):
    lines = text.splitlines()
    lengths = map(lambda l: len(initial_whitespace(l)), lines)
    if not lengths:
        return ("", "")
    initial = min(1000, *lengths) # indenting by 1000 characters?  yow!
    ret = ('\n'.join(map(lambda l: l[initial:], lines)), " " * initial)
    return ret
# End CodeCatalog Snippet

# CodeCatalog Snippet http://codecatalog.net/28/71/
def indent_by(indent, text):
    return '\n'.join(map(lambda s: indent + s, text.splitlines())) + '\n'
# End CodeCatalog Snippet

# CodeCatalog Snippet http://codecatalog.net/63/155/
def normalize_code(code):
    (s,indent) = strip_indent(code)
    return (s.strip() + "\n", indent)
# End CodeCatalog Snippet
