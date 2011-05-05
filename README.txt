Repository for unnamed code catalog project.

To get started:

First, install Python 2.x (current version as of this document is 2.7).

For Linux:

Install django and the django package south.  Debian packages 
python-django, python-django-south.  Also get python-pip, the package manager.  Then

% sudo pip install haystack
% sudo pip install whoosh

For Windows:

Note: Make sure you have C:\Python27 or wherever you downloaded it in your path environment variable!

Download the following python packages:
setuptools (http://pypi.python.org/pypi/setuptools#downloads)

You can then download pip (http://pypi.python.org/pypi/pip#downloads) and then install the following packages (pip install <package>, after adding pip to your path):

(You can also install manually
After extracting each one, navigate to the extracted folder in a command prompt. Then
> python setup.py install)

django (http://www.djangoproject.com/download/)
django-south (http://www.aeracode.org/releases/south/)
django-haystack (https://github.com/toastdriven/django-haystack)
django whoosh (http://pypi.python.org/pypi/Whoosh/#downloads)

This should install each package into your python home directory.


Then

% cd catalog
% python manage.py syncdb
(creates a local sqlite database -- will ask you some questions)
% python manage.py migrate

(prepares database schema (we're doing this to make it easy to migrate schemas later))
% python manage.py runserver

You can also use the bat files:
sync.bat
migrate.bat
start.bat

Now the server will be running on port 8000.  So browse to:

http://localhost:8000/new/

And it will ask you for a new snippet.  Write a python function.  After you submit and
the description page comes up, click the little blue edit buttons to expand the description.

After you have some snippets,

% python manage.py rebuild_index

to build the search index, then search by browsing to:

http://localhost:8000/search/




To update the server to the most recent version of CodeCatalog from the repo:

Log into codecatalog.net through PuTTY/SSH
User: ubuntu

% cd CodeCatalog
% hg fetch

If you changed the database schema:

% cd catalogserver
% ./manage.py migrate

% sudo service apache2 reload

or

% ./update_latest.sh

This script does everything above automatically.