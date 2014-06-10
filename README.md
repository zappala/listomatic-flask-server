### Listomatic Flask Server

A simple list server to demonstrate a REST API that can be called from
a front end or a third-party application. Uses the Flask web
development framework, with username/password for login and SQLAlchemy
as an ORM. Based on Flask-Restful.

## Dependencies

- [Flask](http://flask.pocoo.org/)
- [Flask-Restfull](http://flask-restful.readthedocs.org/en/latest/)
- [Flask-SqlAlchemy](http://pythonhosted.org/Flask-SQLAlchemy/)
- [SqlAlchemy](http://www.sqlalchemy.org/)
- [itsdangerous](https://pypi.python.org/pypi/itsdangerous)

## Installation

First install a few things through apt:

```
sudo apt-get install python-pip
sudo pip install virtualenv
```

Createa virtual environment:

```
mkdir ~/virtualenvs
virtualenv ~/virtualenvs/listomatic-flask-server
source ~/virtualenvs/listomatic-flask-server/bin/activate
```

Install Python requirements:

```
pip install -r requirements.txt
```

## Configuration

Copy the configuration file and setup a few important variables:

```
cp doc/config.py .
```

The `SECRET_KEY` is used for securing session state. Generate one
using a Python shell:

```
python
>>> import os
>>> os.urandom(24)
```

Copy this value into the SECRET KEY as a string. Next, create a new
application for Twitter sign-ons using their [developer
page](https://dev.twitter.com/apps).

## Run the app

```
python app.py
```
