import json
import nose
from nose.tools import *
import unittest

from config import *
from models.user import User
from tests import test_app

class ItemTests(unittest.TestCase):
    def setUp(self):
        db.drop_all()
        db.create_all()

    def test_items(self):
        # register
        r = test_app.post('/users/register',data={'username':'test','password':'test'})
        eq_(r.status_code,200)
        assert 'token' in r.data
        authorization = {'Authorization':json.loads(r.data)['token']}

        # login
        r = test_app.post('/users/login',data={'username':'test','password':'test'},headers=authorization)
        eq_(r.status_code,200)

        # get all items
        r = test_app.get('/items',headers=authorization)
        eq_(r.status_code,200)
        assert 'items' in r.data
        eq_(json.loads(r.data)['items'],[])

        # create an item
        r = test_app.post('/items',data={'text':'todo item 1'},headers=authorization)
        eq_(r.status_code,200)

        # create an item
        r = test_app.post('/items',data={'text':'todo item 2'},headers=authorization)
        eq_(r.status_code,200)

        # get all items
        r = test_app.get('/items',headers=authorization)
        eq_(r.status_code,200)
        assert 'items' in r.data
        eq_(json.loads(r.data)['items'],[{'text':'todo item 1','completed':False,'uri':'/items/1'},{'text':'todo item 2','completed':False,'uri':'/items/2'}])

        # get one item
        r = test_app.get('/items/1',headers=authorization)
        eq_(r.status_code,200)
        eq_(json.loads(r.data),{'text':'todo item 1','completed':False,'uri':'/items/1'})

        # get an item that doesn't exist
        r = test_app.get('/items/10',headers=authorization)
        eq_(r.status_code,403)

        # put new info for item
        r = test_app.put('/items/1',data={'text':'todo item changed','completed':True},headers=authorization)
        eq_(r.status_code,200)
        eq_(json.loads(r.data),{'text':'todo item changed','completed':True,'uri':'/items/1'})

        # register a second user
        r = test_app.post('/users/register',data={'username':'test2','password':'test'})
        eq_(r.status_code,200)
        assert 'token' in r.data
        authorization = {'Authorization':json.loads(r.data)['token']}

        # login
        r = test_app.post('/users/login',data={'username':'test2','password':'test'},headers=authorization)
        eq_(r.status_code,200)

        # get an item that doesn't belong to second user
        r = test_app.get('/items/1',headers=authorization)
        eq_(r.status_code,403)