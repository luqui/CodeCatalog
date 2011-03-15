import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

path = '/home/ubuntu/CodeCatalog/catalog'
os.chdir(path)
if path not in sys.path:
    sys.path.append(path)

upath = '/home/ubuntu/CodeCatalog'
if upath not in sys.path:
    sys.path.append(upath)
