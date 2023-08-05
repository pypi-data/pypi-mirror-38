from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from python_database_rest_logging.config import *
from python_database_rest_logging.model import *
from python_database_rest_logging.utils import *
from flask_security import Security
from flask_injector import FlaskInjector,singleton
from python_database_rest_logging.services import SERVICES
from python_database_rest_logging.api import API_OPERATIONS

import os
LOGGING_API_PREFIX = os.environ.get('LOGGING_API_PREFIX', API_PREFIX)
LOGGING_DATABASE_TYPE = os.environ.get('LOGGING_DATABASE_TYPE', None)
LOGGING_DATABASE_URL = os.environ.get('LOGGING_DATABASE_URL', DATABASE_URL)
LOGGING_DATABASE_HOST = os.environ.get('LOGGING_DATABASE_HOST', None)
LOGGING_DATABASE_USER = os.environ.get('LOGGING_DATABASE_USER', None)
LOGGING_DATABASE_PASSWD = os.environ.get('LOGGING_DATABASE_PASSWD', None)
LOGGING_DATABASE_NAME = os.environ.get('LOGGING_DATABASE_NAME', None)

#Init Flash
app = Flask(__name__, static_url_path="")
CORS(app)
api = Api(app)

try:
    if LOGGING_DATABASE_TYPE is None:
        dbop.bind("sqlite", LOGGING_DATABASE_URL, create_db=True)
    elif LOGGING_DATABASE_TYPE == "sqlite":
        dbop.bind("sqlite", LOGGING_DATABASE_URL, create_db=True)
    elif LOGGING_DATABASE_TYPE == "mysql":
        dbop.bind('mysql', host=LOGGING_DATABASE_HOST, user=LOGGING_DATABASE_USER, passwd=LOGGING_DATABASE_PASSWD, db=LOGGING_DATABASE_NAME)
except TypeError:
    pass
else:
    dbop.generate_mapping(check_tables=False)
dbop.create_tables()

#Security Config
app.config['SECURITY_PASSWORD_HASH'] = SECURITY_PASSWORD_HASH
app.config['SECURITY_PASSWORD_SALT'] = SECURITY_PASSWORD_SALT
app.config['SECURITY_TRACKABLE'] = SECURITY_TRACKABLE
app.config['SECRET_KEY'] = SECRET_KEY
app.config['WTF_CSRF_ENABLED'] = WTF_CSRF_ENABLED
app.config['SECURITY_URL_PREFIX'] = SECURITY_URL_PREFIX

# db.init_app(app)

# Setup Flask-Security
user_datastore = PonyUserDatastore(User, Role)
security = Security(app, user_datastore)

for handler in API_OPERATIONS:
    handler.decorators = handler.DECORATORS
    api.add_resource(handler, API_PREFIX+handler.ENDPOINT)


def configure(binder):

    for service in SERVICES:
        binder.bind(service,scope=singleton)

# Initialize Flask-Injector. This needs to be run *after* you attached all
# views, handlers, context processors and template globals.

FlaskInjector(app=app, modules=[configure])
