from werkzeug.security import generate_password_hash, \
     check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from config import *

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    username = db.Column(db.String(255), unique=True, index=True)
    password_hash = db.Column(db.String(255))

    def __init__(self,username,password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        user = User.query.get(data['id'])
        return user

    @staticmethod
    def get(username):
        return User.query.filter_by(username = username).first()
