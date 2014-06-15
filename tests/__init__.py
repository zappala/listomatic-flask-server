import app
from config import *

# setup database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# setup test app
test_app = app.test_client()

def teardown():
    db.session.remove()
