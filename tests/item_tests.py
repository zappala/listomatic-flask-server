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
        r = test_app.post('/api/users/register',data={'name':'Test','username':'test','password':'test'})
        eq_(r.status_code,200)
        assert 'token' in r.data
        authorization = {'Authorization':json.loads(r.data)['token']}

        # login
        r = test_app.post('/api/users/login',data={'username':'test','password':'test'},headers=authorization)
        eq_(r.status_code,200)

        # get all items
        r = test_app.get('/api/items',headers=authorization)
        eq_(r.status_code,200)
        assert 'items' in r.data
        eq_(json.loads(r.data)['items'],[])

        # create an item
        #r = test_app.post('/api/items',data={'text':'todo item 1'},headers=authorization)
        h = {'Content-Type':'application/json','Authorization':authorization['Authorization']}
        r = test_app.post('/api/items',data=json.dumps({'item':{'title':'todo item 1'}}),headers=h)
        eq_(r.status_code,200)

        # create an item
        #r = test_app.post('/api/items',data={'text':'todo item 2'},headers=authorization)
        r = test_app.post('/api/items',data=json.dumps({'item':{'title':'todo item 2'}}),headers=h)
        eq_(r.status_code,200)

        # get all items
        r = test_app.get('/api/items',headers=authorization)
        eq_(r.status_code,200)
        assert 'items' in r.data
        eq_(json.loads(r.data)['items'],[{'title':'todo item 1','completed':False,'id':1,'uri':'/api/items/1'},{'title':'todo item 2','completed':False,'id':2,'uri':'/api/items/2'}])

        # get one item
        r = test_app.get('/api/items/1',headers=authorization)
        eq_(r.status_code,200)
        eq_(json.loads(r.data),{'id':1,'title':'todo item 1','completed':False,'uri':'/api/items/1'})

        # get an item that doesn't exist
        r = test_app.get('/api/items/10',headers=authorization)
        eq_(r.status_code,403)

        # put new info for item
        r = test_app.put('/api/items/1',data=json.dumps({'item':{'title':'todo item changed','completed':True}}),headers=h)
        eq_(r.status_code,200)
        eq_(json.loads(r.data),{'id':1,'title':'todo item changed','completed':True,'uri':'/api/items/1'})

        # delete an item
        r = test_app.delete('/api/items/2',headers=authorization)
        eq_(r.status_code,200)

        # register a second user
        r = test_app.post('/api/users/register',data={'name':'Test2','username':'test2','password':'test'})
        eq_(r.status_code,200)
        assert 'token' in r.data
        authorization = {'Authorization':json.loads(r.data)['token']}

        # login
        r = test_app.post('/api/users/login',data={'username':'test2','password':'test'},headers=authorization)
        eq_(r.status_code,200)

        # get an item that doesn't belong to second user
        r = test_app.get('/api/items/1',headers=authorization)
        eq_(r.status_code,403)
