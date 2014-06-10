from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# generate with os.urandom(24) in a Python shell
SECRET_KEY = ''

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///list.db'
db = SQLAlchemy(app)
