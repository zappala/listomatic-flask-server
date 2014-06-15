from config import db
from models.user import *

from flask.ext.restful import fields

from datetime import datetime

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    created = db.Column(db.DateTime)
    due = db.Column(db.Date)
    completed = db.Column(db.Boolean)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('items', lazy='dynamic'))

    def __init__(self,text):
        self.text = text
        self.completed = False

    @staticmethod
    def all():
        return Item.query.all()

    @staticmethod
    def get(id):
        return Item.query.get(id)

    @staticmethod
    def fields():
        return {
            'text': fields.String,
            'completed': fields.Boolean,
            'uri': fields.Url('item'),
        }
