"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
import json
from pprint import pprint

def dict_subset(a, b):
    for k in a.keys():
        if k not in b.keys():
            return False
        if a[k] != b[k]: 
            return False
    return True

def forall(xs, p):
    for k in xs:
        if not p(k):    
            return False
    return True

def exists(xs, p):
    for k in xs:
        if p(k): 
            return True
    return False

class APITest(TestCase):
    client = Client()

    def postjson(self, url, **kwargs):
        response = self.client.post(url, kwargs)
        return json.loads(response.content)

    def getjson(self, url):
        response = self.client.get(url);
        return json.loads(response.content)

    def test_spec_versions(self):
        quicksort_dict = { 'name': 'quicksort', 'summary': 'sorts quickly', 'spec': 'quicksrt spec' }
        quicksort2_dict = { 'name': 'quicksort', 'summary': 'sorts quickly', 'spec': 'quicksort spec' }
        quicksort = self.postjson('/api/new/spec/', **quicksort_dict)
        versionptr = quicksort['versionptr']
        quicksort2 = self.postjson('/api/new/spec/', 
                        versionptr=versionptr,
                        **quicksort2_dict)

        self.assertEqual(quicksort['versionptr'], quicksort2['versionptr'])
        self.assertNotEqual(quicksort['version'], quicksort2['version'])

        [qs1,qs2] = self.getjson('/api/specs/' + str(versionptr) + '/all/')
        if qs1['version'] != quicksort['version']:
            (qs1,qs2) = (qs2,qs1)
        self.assertTrue(dict_subset(quicksort_dict, qs1))
        self.assertTrue(dict_subset(quicksort2_dict, qs2))

        qs = self.getjson('/api/specs/' + str(versionptr) + '/active/')
        self.assertEqual(qs, qs2)

    def test_snippet_versions(self):
        quicksort = self.postjson('/api/new/spec/', name='quicksort', summary='sorts quickly', spec='quicksort spec')
        spec_versionptr = quicksort['versionptr']
        
        impl1_dict = { 'spec_versionptr': spec_versionptr, 'code': 'quicksort=sqrt', 'language': 'haskell' }
        impl2_dict = { 'spec_versionptr': spec_versionptr, 'code': 'qucksort=sort', 'language': 'haskell' }
        impl3_dict = { 'spec_versionptr': spec_versionptr, 'code': 'def quicksort(s): s.sort()', 'language': 'python' }
        dicts = [impl1_dict, impl2_dict, impl3_dict]

        impl1 = self.postjson('/api/new/snippet/', **impl1_dict)
        versionptr = impl1['versionptr']
        impl2 = self.postjson('/api/new/snippet/', verisonptr=versionptr, **impl2_dict)
        impl3 = self.postjson('/api/new/snippet/', **impl3_dict)
        impls = [impl1, impl2, impl3]

        rets = self.getjson('/api/specs/' + str(spec_versionptr) + '/snippets/')
        
        pprint(dicts)
        pprint(impls)
        pprint(rets)
        self.assertTrue(forall(rets, lambda r: exists(dicts, lambda d: dict_subset(d,r))))
