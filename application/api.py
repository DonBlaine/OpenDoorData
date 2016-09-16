# file that contains db models to be exposed via a REST API

from models import room, survey, wifi_log, timetable, module # import db models
from app import app # import Flask app
from auth import auth # import Auth app to provide user authentificaiton
from flask import request # import request object to parse json request data

from flask_peewee.rest import RestAPI,UserAuthentication, RestrictOwnerResource, AdminAuthentication

# create RestrictOwnerResource subclass which prevents users modifying another user's content
class SurveyResource(RestrictOwnerResource):
    owner_field = 'reporter'
    
    def check_post(self):

        '''fucntion that checks users are associated with the module they are submitting a POST request to '''

        obj = request.get_json() # parse and return incoming json request data
        user = obj["reporter"]
        mod= obj["module_code"]

        modules = module.select().where(module.module_code == mod) # select module data from module table in db using module_code posted by user 
        authorized = False # initialise authorized variable as False

        for item in modules:
            instructor = str(item.instructor) # select instructor associated with item
            if instructor == user:
                authorized = True
                

        return authorized

    
# instantiate UserAuthentication
user_auth = UserAuthentication(auth)

# instantiate admin-only auth
admin_auth = AdminAuthentication(auth)

# instantiate our api wrapper, specifying user_auth as the default
api = RestAPI(app, default_auth=user_auth)

# register models so they are exposed via /api/<model>/
api.register(room, auth=admin_auth, allowed_methods=['GET'])
api.register(survey,SurveyResource,allowed_methods=['GET','POST'])
api.register(wifi_log, auth=admin_auth,allowed_methods=['GET'])
api.register(timetable, auth=admin_auth, allowed_methods=['GET'])
api.register(module, auth=admin_auth, allowed_methods=['GET'])

