# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 23:54:44 2016

@author: Elayne Ruane
"""

import csv
import time as tm
import datetime
from dateutil.parser import parse
#import models
#import linear_model

def epochtime(x):
    ''' function that reads in a date and converts it to epoch time format
    
    parameters
    ----------
    x: a string that represents a date and time
    
    output
    ------
    an integer that represents the epoch time of the input
    '''
    # replace GMT with UTC
    string = x.lower().replace('gmt', 'UTC')
    # convert string to datetime
    string = parse(x)
    # convert to epoch time
    epoch = int(tm.mktime(string.timetuple()))
    return epoch

def parseName(x):
    ''' function that reads in a string and returns the building name and room number
    
    parameters
    ----------
    x: a string in the format 'Campus > Building Name > Room-000'
    
    output
    ------
    building: a string, the name of the building in lowercase
    room: the int value that represents the room
    '''
    # variable that contains index of '>' character and adds 2     
    inst1 = x.find(">")+2 # finds beginning of building name
    #  variable that contains index of second '>' character
    inst2 = x.find(">", inst1) # begins searching at index inst1
    
    building = x[inst1:inst2-1].lower()
    room = x[inst2+6:]
    
    return (building,room)

def fileToList(file):
    ''' function that reads in a csv file and returns a list of each row of the file
    
    called by insertModCode, insertTimetableData, insertWifiData and insertSurveyData functions
    
    parameters
    ----------
    file: the name of a csv file or variable assigned the name of a csv file
    '''
    
    #open file as read only
    with open(file, 'r') as f:
        # reader object iterates over lines in the file, each element returned as a string
        mycsv = csv.reader(f)
        # create a list of lists
        mylist = list(mycsv)
    f.close()
    return mylist

def createModCode(database, mod_table, field1, field2, user_table, username, modcode):
    ''' function that reads in database parameters 
    
    called by insertModCode function
    
    parameters
    ----------
    database: a file containing database models
    mod_table: the name of the class which represents the table that stores module codes
    field1: the name of the data field in 'mod_table' that stores the module code
    field2: the name of the data field in 'mod_table' that stores the module instructor
    user_table: the name of the class which represents the table that stores user data
    username: the name of the datafield in 'user_table' that stores the username
    modcode: a variable that contains a module code
    '''
    #insert data into db
    database.mod_table.create(field1 = modcode,
                               field2 = user_table.username
                               )
    

def insertModCode(file, database, table, field1, field2, user_table, username):
    ''' function that reads in a file, checks for any unique module codes, and inserts them into a DB
    
    calls fileToList function and createtModCode function
    
    parameters
    ----------
    file: the name of a csv file or variable assigned the name of a csv file
    database: a file containing database models
    table: the name of the class which represents the table that stores module codes
    field1: the name of the data field in 'table' that stores the module code
    field2: the name of the data field in 'table' that stores the module instructor
    user_table: the name of the class which represents the table that stores user data
    username: the name of the datafield in 'user_table' that stores the username
    
    '''
    # create an empty list
    modlist = []
    # create mylist variable containing file data by calling fileToList function
    mylist = fileToList(file)
    # iterate trhough mylist, start from 1 to skip data field names
    for i in range (1, len(mylist)):
        # if module code exists
        if len(mylist[i][3])>1:
            # add to list
            modulecode = mylist[i][3]
            
            if modulecode in modlist:
                continue
            else:
                # call function to insert modcode into db
                insertModCode(database, table, field1, field2, user_table, username)
                # add modulecode to list 
                modlist.append(modulecode) 

    
def insertTimetableData(file, database, table, room_id, building, mod_code, event_time, reg_stu, time):
    '''function that inserts data from a csv file into a table in a database
    
    parameters
    ----------
    file: the name of a csv file or variable assigned the name of a csv file
    database: a file containing database models
    table: the name of the class which represents the table that stores
    room_id: name of the data field in the table containing room_id data
    building: name of the data field in the table containing building data
    mod_code: name of the data field in the table containing module code data
    event_time: name of the data field in the table containing event time data
    reg_stu: name of the data field in the table containing registered student data
    time: name of the data field in the table containing time data
    '''
    # create mylist variable containing file data by calling fileToList function
    mylist = fileToList(file)
    # iterate trhough mylist, start from 1 to skip data field names
    for i in range(1, len(mylist)):         
        room = mylist[i][1]
        build = mylist[i][5]
        time1 = int(mylist[i][2])
        reg_stu = mylist[i][4] if mylist[i][4]!= "" else 0
        code = mylist[i][3] if len(mylist[i][3])>1 else None
        database.table.create(room_id = room,
                              building = build,
                              mod_code = code,
                              event_time = time1,
                              reg_stu = int(float(reg_stu)),
                              time = datetime.datetime.fromtimestamp(time1)
                              )
                              

def insertWifiData(file, database, table, room_id, event_time, assoc_devices, auth_devices, time):
    '''function that inserts data from a csv file into a table in a database
    
    parameters
    ----------
    file: the name of a csv file or variable assigned the name of a csv file
    database: a file containing database models
    table: the name of the class which represents the table that stores
    room_id: name of the data field in the table containing room_id data
    event_time: name of the data field in the table containing event time data
    assoc_devices: name of the data field in the table containing associated device log data
    auth_devices: name of the data field in the table containing authenticated device log data
    time: name of the data field in the table containing time data
    '''
    # create mylist variable containing file data by calling fileToList function
    mylist = fileToList(file)
    # iterate trhough mylist
    for i in range(len(mylist)):
        room = int(parseName(mylist[i][0])[1])
        build = "school of " + parseName(mylist[i][0])[0]
        etime = float(epochtime(mylist[i][1]))
        database.table.create(room_id = room,
                              building = build,
                              event_time = etime, 
                              assoc_devices = mylist[i][2], 
                              auth_devices = mylist[i][3],
                              time = datetime.datetime.fromtimestamp(etime)
                              )

def insertSurveyData(file, database, table, room_id, building, event_time, occupancy, reporter, time, user):
    '''function that inserts data from a csv file into a table in a database
    
    parameters
    ----------
    file: the name of a csv file or variable assigned the name of a csv file
    database: a file containing database models
    table: the name of the class which represents the table that stores
    room_id: name of the data field in the table containing room_id data
    building: name of the data field in the table containing building data
    event_time: name of the data field in the table containing event time data
    occupancy: name of the data field in the table containing occupancy data
    reporter: name of the data field in the table containing user data
    time: name of the data field in the table containing time data
    user: name of user table in database
    '''
    # create mylist variable containing file data by calling fileToList function
    mylist = fileToList(file)
    # iterate trhough mylist, start at 1 to skip data field names
    for i in range(1, len(mylist)):
        room = mylist[i][1]
        build = mylist[i][4]
        etime = int(mylist[i][2])
        database.table.create(room_id = room,
                              building = build,
                              event_time = etime,
                              occupancy = mylist[i][3],
                              reporter = user.username,
                              time = datetime.datetime.fromtimestamp(etime)
                              )


def createTables(database, table_list):
    ''' function that creates tables in a database
    
    parameters
    ----------
    database: the name of a file containing the class representations of the database tables
    table_list: a list containing the names of the tables in the db
    '''
    for i in table_list:
        database.db.create_tables([database.i])



def roomCap(database, table, room_num, capacity, building, num, cap, build):
    '''function that sets room number, room capacity and bilding in a room table in a database
    parameters
    ----------
    database: the name of a file containing the class representations of the database tables
    table: name of the room table in the database
    room_num: name of the data field in the table containing the room number data
    capacity: name of the data field in the table containing the room capacity data
    building: name of the data field in the table containing the building data
    num: the number of the room to be inserted into the database
    cap: the room capacity to be inserted into the database
    build: the building to be inserted into the database
    '''
    database.table.create(room_num = num,
                          building = build,
                          room_cap = cap
                          )


def createAdmin(database, table, username, password, email, first_name, last_name, user, passw, name, mail, sur):
    '''function that creates an admin by inserting user data into the user table of a database
    
    parameters
    ----------
    database: the name of a file containing the class representations of the database tables
    table: name of the room table in the database
    username: name of the data field in the table containing username data
    password: name of the data field in the table containing password data
    email: name of the data field in the table containing email data
    first_name: name of the data field in the table containing first name data
    last_name: name of the data field in the table containing last name data
    user: the type of user
    passw: user password
    mail: user email address
    name: user first name
    sur: user surname
    '''
    database.table.create(username = user,
                          password = passw,
                          email = mail,
                          first_name = name,
                          last_name = sur,
                          admin = True
                          )

def setPassword(database, table, field, utype, password):
    '''function that sets a user's password in a database table
    
    parameters
    ----------
    database: the name of a file containing the class representations of the database tables
    table: name of the room table in the database
    field: name of the field containing password data in the table
    utype: the type of user 
    password: the password to set
    '''
    user = database.table.get(database.table.field == utype)
    user.set_passworrd(password)
    user.save()