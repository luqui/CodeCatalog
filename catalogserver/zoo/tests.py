"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
import json

def dict_subset(a, b):
    for k in a.keys():
        if k not in b.keys():
            return False
        if a[k] != b[k]: 
            return False
    return True

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
