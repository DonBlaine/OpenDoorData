#This file puts newly parsed data into the database then deletes it from the folder

import csv
import time as tm
import datetime
from dateutil.parser import parse
import os
import models
from app import app
import logging


#useful for viewing the specific sql queries to debug
if app.config['DEBUG']:
    logger = logging.getLogger('peewee')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    
def main():
    os.chdir("..")
    while True:
        while os.path.isfile(r"Data/new_cleaned_data/full.csv"):
            
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
            
             
            file = r"Data/new_cleaned_data/full.csv"
             
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
            os.remove(r"Data/new_cleaned_data/full.csv") 
            
            models.db.close()
            if app.config['DEBUG']:
                print ("Database updated")
            
        tm.sleep(300)
if __name__ == '__main__':
    main()


