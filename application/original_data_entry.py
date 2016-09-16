import csv
import time as tm
import datetime
from dateutil.parser import parse
import models
from linear_model import get_linear_coef
import os
from app import app
import logging


#useful for viewing the specific sql queries to debug
if app.config['DEBUG']:
    logger = logging.getLogger('peewee')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())

def main():
    os.chdir("..")
    def epochtime(x): 
        string = parse(x)
        epoch = int(tm.mktime(string.timetuple()))
        return epoch
    
    def parseName(x):
        inst1 = x.find(">")+2
        inst2 = x.find(">", inst1)
        
        building = x[inst1:inst2-1].lower()
        room = x[inst2+6:]
        
        return (building,room)
    

    models.db.create_tables([models.room,
                              models.User,
                              models.module,
                              models.wifi_log,
                              models.timetable,
                              models.survey,
			                  models.regressionModel,
                              models.building
                              ], safe=True)
    
    models.regressionModel.create(weight = get_linear_coef("original_cleaned_data", "full.csv", "survey_data.csv"))


    models.building.create(name = "School of Computer Science", 
    code = "scs",
    phone = "+353 1 716 2483",
    email = "cs.secretary@ucd.ie",
    opening_hour_weekday = "09:00",
    closing_hour_weekday = "19:00",
    lat = 53.3092327,
    lon = -6.2239067,
    image_dir = "images/scs.jpg"
                )   
    models.room.create(room_num = 2,
                building = "school of computer science",
                room_cap = 90,
                building_code = "scs",
                code = "B002"
                )
    models.room.create(room_num = 3,
                building = "school of computer science",
                room_cap = 90,
                building_code = "scs",
                code = "B003"
                )
    models.room.create(room_num = 4,
                building = "school of computer science",
                room_cap = 220,
                building_code = "scs",
                code = "B004"
                )
    models.User.create(username = "admin",
                 password = "password",
                 email = "donovanjblaine@gmail.com",
                 first_name = 'Don',
                 last_name = "Blaine",
                 admin = True
                 )
    user = models.User.get(models.User.username == "admin")
    user.set_password ("password")
    user.save()
        
    file = r"Data/original_cleaned_data/timetable.csv"
    
    with open(file, 'r') as f:
        mycsv= csv.reader(f)
        mylist = list(mycsv)
    
    modlist = []
    for i in range (1, len(mylist)):
        
        if len(mylist[i][3])>1:
            modulecode = mylist[i][3]
            
            if modulecode in modlist:
                continue
            else:
                models.module.create(module_code = modulecode,
                                     instructor = user.username
                                     )
                           
            modlist.append(modulecode)
            
    for i in range (1, len(mylist)):
         
        roomid = mylist[i][1]
        build = mylist[i][5]
        time1 = int(mylist[i][2])
        reg_stu = mylist[i][4] if mylist[i][4]!= "" else 0
        modulecode = mylist[i][3] if len(mylist[i][3])>1 else None
        models.timetable.create(room_id = roomid,
                                building = build,
                         mod_code = modulecode,
                         event_time = time1,
                         reg_stu = int(float(reg_stu)),
                         time = datetime.datetime.fromtimestamp(time1)
                         )
                        
    f.close()
     
    file = r"Data/original_cleaned_data/full.csv"
     
    with open(file, 'r') as f:
        mycsv= csv.reader(f)
        mylist = list(mycsv)
     
    for i in range(len(mylist)):
        roomid = int(parseName(mylist[i][0])[1])
        build = "school of " + parseName(mylist[i][0])[0]
        etime = float(epochtime(mylist[i][1]))
        models.wifi_log.create(room_id = roomid,
                                building = build,
                            event_time = etime, 
                            assoc_devices = mylist[i][2], 
                            auth_devices = mylist[i][3],
                            time = datetime.datetime.fromtimestamp(etime)
                            )
      
    f.close()
     
    file = r"Data/original_cleaned_data/survey_data.csv"
     
    with open(file, 'r') as f:
        mycsv= csv.reader(f)
        mylist = list(mycsv)
     
    for i in range(1, len(mylist)):
        roomid = mylist[i][1]
        build = mylist[i][4]
        etime = int(mylist[i][2])
        models.survey.create(room_id = roomid,
                              building = build,
                        event_time = etime,
                        occupancy = mylist[i][3],
                        reporter = user.username,
                        time = datetime.datetime.fromtimestamp(etime)
                        )
         
    f.close()
    
    models.db.close()
    print ("The database should now be available")

if __name__ == '__main__':
    main()

