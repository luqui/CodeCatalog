import json
from django import template

register = template.Library()

def dump_json(x):
    return json.dumps(x)

register.filter('json', dump_json)
