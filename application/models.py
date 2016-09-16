##models.py - Database models for use with your ORM/ business logic, etc.

import peewee
import datetime
from flask_peewee.auth import BaseUser
import pymysql
from app import app

if __name__ == "__main__":
    configdb = app.config['DATABASE']
    
    conn = pymysql.connect(host = configdb['host'],
                          user = configdb['user'],
                          password =configdb['password']
                          )
    c = conn.cursor()
    c.execute("CREATE DATABASE IF NOT EXISTS wifi_db")
    conn.close()
configdb = app.config['DATABASE']
db = peewee.MySQLDatabase("wifi_db",
                          host = configdb['host'],
                          user = configdb['user'],
                          password =configdb['password']
                          )

db.connect()
  
    
class BaseModel(peewee.Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = db
        
class room(BaseModel):
    id_field = peewee.PrimaryKeyField()
    room_num = peewee.IntegerField()
    room_cap = peewee.IntegerField()
    building = peewee.CharField()
    building_code = peewee.CharField()
    code = peewee.CharField()
    
    class Meta:
        indexes = (
                   (('room_num', 'building'), True),
                   )

    def __str__(self):
        return str(self.id_field)

class building(BaseModel):
    id_field = peewee.PrimaryKeyField()
    code = peewee.CharField()
    name = peewee.CharField()
    phone = peewee.CharField()
    email = peewee.CharField()
    opening_hour_weekday = peewee.CharField()
    closing_hour_weekday = peewee.CharField()
    opening_hour_weekend = peewee.CharField(default="Closed")
    closing_hour_weekend = peewee.CharField(default="Closed")
    lat = peewee.DoubleField()
    lon = peewee.DoubleField()
    image_dir = peewee.CharField()

    def __str__(self):
        return str(self.id_field)

class wifi_log(BaseModel):
    id_field = peewee.PrimaryKeyField()
    room_id = peewee.IntegerField()
    event_time = peewee.IntegerField()
    assoc_devices = peewee.IntegerField()
    auth_devices = peewee.IntegerField()
    time = peewee.DateTimeField()
    building = peewee.CharField()
  
    class Meta:
        indexes = ((('room_id','event_time','building'), True),)
        constraints = [peewee.SQL('FOREIGN KEY(room_id, building)'
                           'REFERENCES room(room_num, building)ON DELETE CASCADE ON UPDATE CASCADE')]
    def __str__(self):
        return str(self.id_field)
    
class User(BaseModel, BaseUser):
    #need to have auto id for sessions to work
    username = peewee.CharField(unique=True)
    password = peewee.CharField()
    first_name = peewee.CharField()
    last_name=peewee.CharField()
    email = peewee.CharField()
    join_date = peewee.DateTimeField(default=datetime.datetime.now)
    active = peewee.BooleanField(default=True)
    admin = peewee.BooleanField(default=False)

       
    def __str__(self):
        return str(self.username)
               
class module(BaseModel):
    id_field = peewee.PrimaryKeyField()
    module_code = peewee.CharField()
    instructor = peewee.ForeignKeyField(User,
                                        to_field='username', 
                                        db_column = 'instructor', 
                                        null=True, 
                                        on_delete='SET NULL',
                                        on_update='CASCADE')
    
    class Meta:
        indexes = ((('module_code','instructor'), True),)
         
    def __str__(self):
        return str(self.module_code)

class timetable(BaseModel):
    id_field = peewee.PrimaryKeyField()
    room_id = peewee.IntegerField()
    mod_code = peewee.ForeignKeyField(module, 
                                      to_field='module_code', 
                                      db_column='mod_code',
                                      null=True, 
                                      on_delete='SET NULL')
    event_time = peewee.IntegerField()
    reg_stu = peewee.IntegerField()
    time = peewee.DateTimeField()
    building = peewee.CharField()
    
    class Meta:
        indexes = ((('room_id','event_time','building'), True),)
        constraints = [peewee.SQL('FOREIGN KEY(room_id, building)'
                           'REFERENCES room(room_num, building)')]   
    def __str__(self):
        return str(self.id_field)

class survey(BaseModel):
    id_field = peewee.PrimaryKeyField()
    room_id = peewee.IntegerField()
    event_time = peewee.IntegerField()
    occupancy = peewee.FloatField(constraints=[peewee.Check('occupancy <= 1 AND occupancy >=0')])
    time = peewee.DateTimeField()
    module_code = peewee.CharField(null = True)
    reporter = peewee.ForeignKeyField(User,
                                to_field='username', 
                                db_column = 'reporter', 
                                null=True, 
                                on_delete='SET NULL',
                                on_update='CASCADE')
    building = peewee.CharField()
    
    class Meta:
        indexes = ((('room_id','event_time','building'), True),)
        constraints = [peewee.SQL('FOREIGN KEY(room_id, building)'
                                  'REFERENCES room(room_num, building)'
                                  'ON DELETE CASCADE ON UPDATE CASCADE')]
        
class regressionModel(BaseModel):
    id_field = peewee.PrimaryKeyField()
    offset = peewee.DecimalField(default= 0.0)
    weight = peewee.DecimalField(default = 0.0)
    end_date = peewee.DateTimeField(default = "9999-12-31 23:59:59")
    
db.close()



