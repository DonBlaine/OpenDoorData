# file that registeres models for admin interface
# NOTE: to make the admin db useable must change unicode in the admin flask peewee package to str

from flask_peewee.admin import Admin, ModelAdmin # ModelAdmin class determines how models are exposed in the admin interface
from app import app
from auth import auth # import authentication
from models import User, wifi_log,room,timetable,survey,module, regressionModel # import database models


# customize how models are displayed in admin area by creating ModelAdmin subclasses

class RoomAdmin(ModelAdmin):
    columns = ('room_num', 'room_cap', 'building',) # columns available to admin
    
   
class ModuleAdmin(ModelAdmin):
    columns = ('module_code','instructor')
    foreign_key_lookups = {'instructor': 'username'} # foreign_key_lookups is a paginated widget that supports type-ahead search
    filter_exclude = ('instructor__password','instructor__join_date','instructor__') # don't allow admin access to these columns
    filter_fields = ('module_code','instructor__username','instructor__email','instructor__id') # only allow filtering on these fields
     
   
class TimetableAdmin(ModelAdmin):
    columns = ('room_id', 'mod_code', 'time','reg_stu', 'building')
    foreign_key_lookups = {'mod_code': 'module_code','room_id':'room_num','building':'building'}
    filter_fields = ('room_id', 'time','mod_code',"reg_stu",'building')


class UserAdmin(ModelAdmin):
    columns = ('username', 'email','first_name','last_name', 'join_date','active','admin')
    filter_fields = ('username', 'email', 'join_date', 'active','admin','first_name','last_name')
    
    def save_model(self, instance, form, adding=True):
        '''function that is responsible for persisting user password changes to the database
        
        parameters
        ----------
        instance: an unsaved user model instance
        form: a validated form instance
        adding: boolean to indicate whether a new instance is being added or saving an existing instance
        '''
        orig_password = instance.password
     
        user = super(UserAdmin, self).save_model(instance, form, adding)
        
        if orig_password != form.password.data: # if user adds or edits password
            user.set_password(form.password.data) # set as new password
            user.save() # save new password
     
        return user


# instantiate Admin object
admin = Admin(app, auth)
auth.register_admin(admin)

# register models to expose them to the admin area
admin.register(room, RoomAdmin)  # pass model and subclass with display variables
admin.register(module, ModuleAdmin)
admin.register(timetable, TimetableAdmin)
admin.register(User, UserAdmin)
