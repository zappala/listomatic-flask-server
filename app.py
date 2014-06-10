from flask import request, abort
from flask.ext.restful import Resource, Api, reqparse

from config import *
from models.item import Item
from models.user import User

from functools import wraps
import re

api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True)
parser.add_argument('password', type=str, required=True)

class RegisterAPI(Resource):
    def post(self):
        args = parser.parse_args()
        print args
        username = args['username']
        password = args['password']
        # check if username already exists
        if User.get(username) is not None:
            abort(400)
        user = User(username,password)
        db.session.add(user)
        db.session.commit()
        token = user.generate_auth_token()
        return { 'token': token }

class LoginAPI(Resource):
    def post(self):
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        # get user
        args = parser.parse_args()
        user = User.get(username)
        if not user or not user.check_password(password):
            abort(400)
        # generate token
        token = user.generate_auth_token()
        return { 'token': token }

def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(400)
        if not User.verify_auth_token(request.headers['Authorization']):
            abort(400)
        return func(*args, **kwargs)
    return wrapper

class AuthResource(Resource):
    method_decorators = [authenticate]

class ItemAPI(AuthResource):
    def get(self, id):
        item = Item.get(id)
        if not item:
            return {'text': ''}
        return {'text': Item.get(id).text}

    def put(self, id):
        text = request.form['text']
        item = Item(text)
        db.session.add(item)
        db.session.commit()
        return {id: item.id}

api.add_resource(RegisterAPI, '/users/register')
api.add_resource(LoginAPI, '/users/login')
api.add_resource(ItemAPI, '/items/<string:id>')

if __name__ == '__main__':
    db.create_all()
    app.run()

