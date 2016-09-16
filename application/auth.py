# file that contains the authentication system used to provide security to the admin interface

from flask_peewee.auth import Auth  # Login/logout views, etc.
from app import app
from models import User, db

# instantiate an Auth object for use with flask app and database wrapper
auth = Auth(app, db, user_model = User)
