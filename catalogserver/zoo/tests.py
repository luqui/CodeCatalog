"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
import json
from pprint import pprint
from zoo import models
from django.contrib.auth.models import User
import time

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

    def makeuser(self, username, password):
        user = User.objects.create_user(username, 'yourmom@example.com', password=password)
        user.save()

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
        impl2_dict = { 'spec_versionptr': spec_versionptr, 'code': 'quicksort=sort', 'language': 'haskell' }
        impl3_dict = { 'spec_versionptr': spec_versionptr, 'code': 'def quicksort(s): s.sort()', 'language': 'python' }
        dicts = [impl1_dict, impl2_dict, impl3_dict]

        impl1 = self.postjson('/api/new/snippet/', **impl1_dict)
        versionptr = impl1['versionptr']
        impl2 = self.postjson('/api/new/snippet/', versionptr=versionptr, **impl2_dict)
        impl3 = self.postjson('/api/new/snippet/', **impl3_dict)
        impls = [impl1, impl2, impl3]

        rets = self.getjson('/api/specs/' + str(spec_versionptr) + '/snippets/')
        self.assertTrue(forall(rets, lambda r: exists(dicts, lambda d: dict_subset(d,r))))

        activesnip = self.getjson('/api/snippets/' + str(versionptr) + '/active/')
        self.assertTrue(dict_subset(impl2_dict, activesnip))

        rets = self.getjson('/api/specs/' + str(spec_versionptr) + '/snippets/active/')
        if rets[0]['language'] != 'haskell': (rets[0],rets[1]) = (rets[1],rets[0])
        self.assertTrue(dict_subset(impl2_dict, rets[0]))
        self.assertTrue(dict_subset(impl3_dict, rets[1]))

    def test_votes(self):
        self.makeuser('foo', 'bar')
        self.makeuser('baz', 'quux')

        quicksort = self.postjson('/api/new/spec/', name='quicksort', summary='sorts quickly', spec='quicksort spec')
        versionptr = quicksort['versionptr']

        def vote(val, expected):
            self.postjson('/api/vote/', versionptr=versionptr, value=val)
            self.assertEqual(self.getjson('/api/specs/' + str(versionptr) + '/active/')['votes'], expected)

        self.client.login(username='foo', password='bar')
        
        vote(1, 1)
        # can't vote more than once (new vote cancels out old)
        vote(1,1)

        self.client.login(username='baz', password='quux')

        # votes from different users add
        vote(1,2)

        # and cancel
        vote(-1,0)

        # and can be cancelled
        vote(0,1)

        self.client.login(username='foo', password='bar')
        
        # by both users
        vote(0,0)

        # votes can be negative
        vote(-1,-1)
