from distutils.core import setup

setup(
    name='CodeCatalog',
    version='0.1',
    description='A library and command line tool for interacting with the CodeCatalog site',
    packages=['codecatalog'],
    scripts=['scripts/codecatalog.py'],
)
