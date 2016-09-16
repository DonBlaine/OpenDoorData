# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 17:41:41 2016

@author: Elayne Ruane
"""


import models
import data_entry_functions
import linear_model

def main():
    
    # insert tables into database
    tables = ['room', 'User', 'module', 'wifi_log', 'timetable', 'survey', 'regressionModel']
    data_entry_functions.createTables(models, tables)
    

    # insert room data into room table in db    
    data_entry_functions.roomCap(models, 'room', 'room_num', 'room_cap', 'building', 2, 90, 'school of computer science')
    data_entry_functions.roomCap(models, 'room', 'room_num', 'room_cap', 'building', 3, 90, 'school of computer science')    
    data_entry_functions.roomCap(models, 'room', 'room_num', 'room_cap', 'building', 4, 220, 'school of computer science')

    # create admin user
    data_entry_functions.createAdmin(models, 'User', 'username', 'password', 'email', 'first_name', 'last_name', 'admin', 'password', "donovanjblaine@gmail.com", 'Don', 'Blaine')

    # set user password    
    data_entry_functions.setPassword(models, 'User', 'username', 'admin', 'password')

    # insert data into database from csv file
    file = "cleaned_data/timetable.csv"
    data_entry_functions.insertModCode(file, models, 'module', 'module_code', 'instructor', 'user', 'username')
    
    # setting weight to be linear model coef - create function ?
    models.regressionModel.create(weight = linear_model.get_linear_coef())
    
    # insert timetable data
    data_entry_functions.insertTimetableData(file, models, 'timetable', 'room_id', 'building', 'mod_code', 'event_time', 'reg_stu', 'time')
    
    # insert wifi log data
    file = r"cleaned_data/full.csv"
    data_entry_functions.insertWifiData(file, models, 'wifi_log', 'room_id', 'event_time', 'assoc_devices', 'auth_devices', 'time')
    
    # insert survey data
    file = r"cleaned_data/survey_data.csv"
    data_entry_functions.insertSurveyData(file, models, 'survey', 'room_id', 'building', 'event_time', 'occupancy', 'reporter', 'time')
    

    models.db.close()
    print ("The database should now be available")

if __name__ == '__main__':
    main()