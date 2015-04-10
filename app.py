from flask import request, abort, g
from flask.ext.restful import Resource, Api, reqparse, marshal

from config import *
from models.item import Item
from models.user import User

from functools import wraps
import json
import re

api = Api(app)

register_parser = reqparse.RequestParser()
register_parser.add_argument('username', type=str, required=True)
register_parser.add_argument('name', type=str, required=True)
register_parser.add_argument('password', type=str, required=True)

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', type=str, required=True)
login_parser.add_argument('password', type=str, required=True)

item_parser = reqparse.RequestParser()
item_parser.add_argument('title', type=str, required=True)
item_parser.add_argument('completed', type=bool, required=True)

class RegisterAPI(Resource):
    def post(self):
        args = register_parser.parse_args()
        username = args['username']
        name = args['name']
        password = args['password']
        # check if username already exists
        if User.get(username) is not None:
            abort(403)
        user = User(username,name,password)
        db.session.add(user)
        db.session.commit()
        token = user.generate_auth_token()
        return { 'name':user.name,'token': token }

class LoginAPI(Resource):
    def post(self):
        args = login_parser.parse_args()
        username = args['username']
        password = args['password']
        # get user
        user = User.get(username)
        if not user or not user.check_password(password):
            abort(403)
        # generate token
        token = user.generate_auth_token()
        return { 'name':user.name,'token': token }

def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(403);
        user = User.verify_auth_token(request.headers['Authorization'])
        if not user:
            abort(403);
        g.user = user
        return func(*args, **kwargs)
    return wrapper

def current_user():
    return g.user

class AuthResource(Resource):
    method_decorators = [authenticate]

class ItemsAPI(AuthResource):
    # @marshal_with(Item.fields())
    def get(self):
        # get the user
        user = g.user
        items = [i for i in user.items]
        if items:
            return {'items': marshal(items,Item.fields())}
        return {'items': []}

    def post(self):
        # get the user
        user = g.user
        r = json.loads(request.data)
        title = r['item']['title']
        item = Item(title)
        item.user = user
        db.session.add(item)
        db.session.commit()
        return {'item': marshal(item,Item.fields())}

class ItemAPI(AuthResource):
    def get(self, id):
        # get the user
        user = g.user
        item = Item.get(id)
        if not item:
            abort(403)
        if not item.user == user:
            abort(403)
        return marshal(item,Item.fields())

    def put(self, id):
        # get the user
        user = g.user
        item = Item.get(id)
        if not item:
            abort(403)
        if not item.user == user:
            abort(403)
        # load datax
        r = json.loads(request.data)
        title = r['item']['title']
        completed = r['item']['completed']
        # modify it
        item.title = title
        item.completed = completed
        db.session.add(item)
        db.session.commit()
        return marshal(item,Item.fields())

    def delete(self,id):
        user = g.user
        item = Item.get(id)
        if not item:
            abort(403)
        if not item.user == user:
            abort(403)
        db.session.delete(item)
        db.session.commit()
        return 200

api.add_resource(RegisterAPI, '/api/users/register')
api.add_resource(LoginAPI, '/api/users/login')
api.add_resource(ItemsAPI, '/api/items')
api.add_resource(ItemAPI, '/api/items/<string:id>',endpoint='item')

@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return app.send_static_file(path)

if __name__ == '__main__':
    db.create_all()
    app.run()

