import json
import nose
from nose.tools import *
import unittest

from config import *
from models.user import User
from tests import test_app

class UserTests(unittest.TestCase):
    def setUp(self):
        self.token = ''
        db.drop_all()
        db.create_all()

    def test_registration(self):
        r = test_app.post('/users/register',data={'username':'test','password':'test'})
        eq_(r.status_code,200)
        assert 'token' in r.data
        self.token = json.loads(r.data)['token']

        # try again
        r = test_app.post('/users/register',data={'username':'test','password':'test'})
        eq_(r.status_code,400)

    def test_login(self):
        r = test_app.post('/users/register',data={'username':'test','password':'test'})
        eq_(r.status_code,200)
        r = test_app.post('/users/login',data={'username':'test','password':'test'},headers={'Authorization':self.token})
        eq_(r.status_code,200)
