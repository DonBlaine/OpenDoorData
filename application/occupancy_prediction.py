from app import app
import pymysql
import pandas as pd
from model_functions import dataframe_epochtime_to_datetime
from linear_model import get_linear_coef
from models import wifi_log,room
import datetime


def getHistoricalData(rid, date, month, year):
    '''Takes in a specific room_id, date, month and year as parameters and returns
    the historical predicted occupancy data for each hour of that particular day'''

    #Connect to database
    configdb = app.config['DATABASE']
    
    conn = pymysql.connect(db = 'wifi_db',
                           host = configdb['host'],
                          user = configdb['user'],
                          password =configdb['password']
                          )

    wifi_logs = pd.read_sql('''
        SELECT logd.room_id, logd.event_time, auth_devices, assoc_devices, logd.building, occupancy, room_cap AS capacity 
        FROM wifi_db.room AS rooms, wifi_db.wifi_log AS logd, wifi_db.survey AS survey 
        WHERE logd.room_id = %s 
            AND logd.room_id = rooms.room_num
            AND logd.room_id = survey.room_id
            AND FROM_UNIXTIME(logd.event_time, "%%e") = %s 
            AND FROM_UNIXTIME(logd.event_time, "%%m") = %s
            AND FROM_UNIXTIME(logd.event_time, "%%Y") = %s
            AND FROM_UNIXTIME(logd.event_time, "%%e") = FROM_UNIXTIME(survey.event_time, "%%e")
            AND FROM_UNIXTIME(logd.event_time, "%%m") = FROM_UNIXTIME(survey.event_time, "%%m")
            AND FROM_UNIXTIME(logd.event_time, "%%H") = FROM_UNIXTIME(survey.event_time, "%%H");''', con=conn, params=[rid, date, month, year])

    wifi_logs = getHourlyPrediction(wifi_logs, conn)
    
    wifi_logs_merged = wifi_logs[['building', 
                           'room_id',         
                           'occupancy',
                           'capacity',            
                           'assoc_devices',
                           'event_day', 
                           'event_hour', 
                           'event_month', 
                           'event_year', 
                           'occupancy_category_5', 
                           'occupancy_category_3',
                           'binary_occupancy']]

    return returnPredictionJson(wifi_logs)

def getOccupancyRating(rid):
    '''Takes in a specific room_id, date, month and year as parameters and returns
    the historical predicted occupancy data for each hour of that particular day'''

    #Connect to database
    configdb = app.config['DATABASE']
    
    conn = pymysql.connect(db = 'wifi_db',
                           host = configdb['host'],
                          user = configdb['user'],
                          password =configdb['password']
                          )

    wifi_logs = pd.read_sql('''
        SELECT logd.room_id, logd.event_time, auth_devices, assoc_devices, logd.building, room_cap AS capacity 
        FROM wifi_db.room AS rooms, wifi_db.wifi_log AS logd, wifi_db.survey AS survey 
        WHERE logd.room_id = %s
            AND logd.room_id = rooms.room_num
            AND logd.room_id = survey.room_id
            AND FROM_UNIXTIME(logd.event_time, "%%e") = FROM_UNIXTIME(survey.event_time, "%%e")
            AND FROM_UNIXTIME(logd.event_time, "%%m") = FROM_UNIXTIME(survey.event_time, "%%m")
            AND FROM_UNIXTIME(logd.event_time, "%%H") = FROM_UNIXTIME(survey.event_time, "%%H");''', con=conn, params=[rid])

    wifi_logs = getHourlyPrediction(wifi_logs, conn)
    
    wifi_logs_merged = wifi_logs[['occupancy_pred', 'event_hour','capacity']]

    return calculateOccupancyRating(returnPredictionJson(wifi_logs_merged))

def calculateOccupancyRating(d):
    sum = 0

    for i in d:
        sum += (i['occupancy_pred'] / i['capacity']) * 100

    return round(sum/len(d))
        

def getGeneralData(rid):
    #Connect to database
    configdb = app.config['DATABASE']
    
    conn = pymysql.connect(db = 'wifi_db',
                           host = configdb['host'],
                          user = configdb['user'],
                          password =configdb['password']
                          )

    wifi_logs = pd.read_sql('''
        SELECT AVE.room_id, AVE.event_time, avg(AVE.assoc_devices) AS assoc_devices, avg(AVE.auth_devices) as auth_devices, AVE.time, AVE.building
        FROM(
            SELECT room_id, event_time, avg(assoc_devices) AS assoc_devices, avg(auth_devices) as auth_devices, time, building
                FROM wifi_db.wifi_log 
                WHERE room_id = %s 
                    AND FROM_UNIXTIME(event_time, "%%w") > 0 
                    AND FROM_UNIXTIME(event_time, "%%w") < 6 
                    AND FROM_UNIXTIME(event_time, "%%H") > 08 
                    AND FROM_UNIXTIME(event_time, "%%H") < 19
                GROUP BY FROM_UNIXTIME(event_time, "%%w"), FROM_UNIXTIME(event_time, "%%e"), FROM_UNIXTIME(event_time, "%%H")) AS AVE
            GROUP BY FROM_UNIXTIME(AVE.event_time, "%%H");''', con=conn, params=[rid])

    wifi_logs = getHourlyPrediction(wifi_logs, conn)
    
    wifi_logs_merged = wifi_logs[['building', 
                           'room_id',         
                           'occupancy_pred',         
                           'assoc_devices',
                           'event_day', 
                           'event_hour', 
                           'event_month', 
                           'event_year', 
                           'occupancy_category_5', 
                           'occupancy_category_3',
                           'binary_occupancy']]

    return returnPredictionJson(wifi_logs_merged)

def getModuleData(mid):
    #Connect to database
    configdb = app.config['DATABASE']
    
    conn = pymysql.connect(db = 'wifi_db',
                           host = configdb['host'],
                          user = configdb['user'],
                          password =configdb['password']
                          )

    wifi_logs = pd.read_sql('''SELECT wifilogs.building as building, wifilogs.assoc_devices as assoc_devices, wifilogs.auth_devices as auth_devices, wifilogs.time as Time, wifilogs.room_id as room_id, wifilogs.event_time as event_time, timetable.mod_code as module_code, timetable.reg_stu as reg_students, timetable.time as Date
        FROM wifi_db.wifi_log AS wifilogs, wifi_db.timetable AS timetable
        WHERE FROM_UNIXTIME(wifilogs.event_time, "%%H") = FROM_UNIXTIME(timetable.event_time, "%%H") AND
            FROM_UNIXTIME(wifilogs.event_time, "%%w") = FROM_UNIXTIME(timetable.event_time, "%%w") AND
            wifilogs.room_id = timetable.room_id AND
            timetable.mod_code = %s AND
            FROM_UNIXTIME(wifilogs.event_time, "%%e") = FROM_UNIXTIME(timetable.event_time, "%%e");
            ''', con=conn, params=[mid])

    wifi_logs = getHourlyPrediction(wifi_logs, conn)
    
    wifi_logs_merged = wifi_logs[['building', 
                           'room_id',         
                           'occupancy_pred',         
                           'assoc_devices',
                           'event_day', 
                           'event_hour', 
                           'event_month',
                           'event_year', 
                           'occupancy_category_5', 
                           'occupancy_category_3',
                           'binary_occupancy']]

    return returnPredictionJson(wifi_logs_merged)    

def getHourlyPrediction(wifi_logs, conn):

    prediction_table = pd.read_sql('select * from regressionmodel where date(end_date) >= curdate();', con=conn)

    if prediction_table.shape[0] > 1:
        raise KeyError("More than 1 coefficient selected for the current date; check database")
    
    predict_coef = prediction_table['weight'][0]
    predict_intercpt = prediction_table['offset'][0]

    room_data = pd.read_sql('select * from room;', con=conn)
    # Convert epoch to datetime in dataframe


    wifi_logs = dataframe_epochtime_to_datetime(wifi_logs, "event_time")

    wifi_logs = wifi_logs.groupby(['building','room_id', 'event_day', 'event_hour', 'event_month', 'event_year'], 
                                  as_index=False).median()


    #Calculate predicted occupancy
    wifi_logs['occupancy_pred'] = None
    for i in range(wifi_logs.shape[0]):
        wifi_logs.set_value(i, 'occupancy_pred', 
                            wifi_logs['auth_devices'][i] * predict_coef + predict_intercpt)
    
    #add categories
    wifi_logs['occupancy_category_5'] = None
    wifi_logs['occupancy_category_3'] = None
    wifi_logs['binary_occupancy'] = None

    for i in range(wifi_logs.shape[0]):
        room = wifi_logs['room_id'][i]
        building = wifi_logs['building'][i]

        capacity = room_data['room_cap'].loc[(room_data['room_num'] == room) & (room_data['building'] == building)].values[0]
        #print(wifi_logs['occupancy_pred'][i])
        prediction = set_occupancy_category(wifi_logs['occupancy_pred'][i], capacity)
        
        wifi_logs.set_value(i, 'occupancy_category_5', prediction[0])
        wifi_logs.set_value(i, 'occupancy_category_3', prediction[1])
        wifi_logs.set_value(i, 'binary_occupancy', prediction[2])

    return wifi_logs
    
def returnPredictionJson(wifi_logs_merged):
    #Select only day hours to avoid useless (night / closing hour) data
    #In the future every building's row should be cross checked to ensure that the hours removed are its own opening/closing hours
    #Since we have only 1 building we took its own opening/closing hours
    wifi_logs_merged = wifi_logs_merged[(wifi_logs_merged.event_hour > 8) & (wifi_logs_merged.event_hour < 18)]
    wifi_logs_merged = wifi_logs_merged.reset_index()

    #orient='index' will create 1 json object for each row as opposed to for each column.
    wifi_logs_merged = wifi_logs_merged.to_dict(orient='records')
    #print(wifi_logs_merged)
    return wifi_logs_merged
       

def set_occupancy_category(occupants, capacity):
    '''function that converts linear predictions to a defined category.
    
    Parameters
    ----------
    occupants: the number of occupants (real or predicted)
    capacity: the room capacity
    
    Returns
    ---------
    list with 3 values:
        at position 0, the occupancy with 5 cateories
        at position 1, the occupancy with 3 categories
        at position 2, the binary occupancy
    
    '''
    
    ratio = occupants/capacity
    
    # assign category based on ratio
    if ratio < 0.125:
        cat5 = 0.0
    elif ratio < 0.375:
        cat5 =  0.25
    elif ratio < 0.625:
        cat5 =  0.5
    elif ratio < 0.875:
        cat5 =  0.75
    else:
        cat5 =  1.0
    
    cat3 = 0 if cat5 < 0.25 else 0.5 if cat5 < 0.75 else 1 if cat5>= 0.75 else "ERROR"
    
    cat2 = 0 if cat3 == "empty" else 1
    
    return cat5, cat3, cat2 #This will return a tuple

def full_room_json(rid):
    
    query1 = wifi_log.select().order_by(wifi_log.event_time.desc()).get()
    query = wifi_log.select().order_by(wifi_log.event_time).get()
    begin = query.event_time
    end = query1.event_time
    one_day = 86400
    json_list = []
    date = datetime.datetime.fromtimestamp(begin)
    if int(date.strftime("%H"))>16:
            begin += one_day
    
    while begin<=end:

        date = datetime.datetime.fromtimestamp(begin)
        try:
            cur_data = getHistoricalData(rid, date.day, date.month, date.year)
        except:
            break
        json_list.append(cur_data)
        if date.strftime("%a") != "Fri":
            begin += one_day
        else:
            begin += (one_day*3)

    
    return json_list



def total_full_json():
    
    rooms = room.select()
    room_list = []
    for item in rooms:
        room_list.append(item.room_num)
    json_list = []
    
    for item in room_list:
        cur_data = full_room_json(item)
        json_list.append(cur_data)
    
    return json_list

def getWeeks():
    query = wifi_log.select().order_by(wifi_log.event_time).get()
    query1 = wifi_log.select().order_by(wifi_log.event_time.desc()).get()
    begin = query.event_time
    one_day = 86400
    end = query1.event_time - (one_day*4)
    week_list = []
    
    while begin <=end:
        date = datetime.datetime.fromtimestamp(begin).strftime('%d-%m-%Y')
        week_list.append(str(date))
        begin += (one_day*7)
        
    return week_list

def week_room_json(rid,time_stamp):
    
    string = time_stamp.split("-")
    
    query = wifi_log.select().order_by(wifi_log.event_time).get()
    query1 = wifi_log.select().order_by(wifi_log.event_time.desc()).get()
    date_entered = (datetime.datetime(int(string[2]),int(string[1]),int(string[0]))- datetime.datetime(1970,1,1)).total_seconds()
    one_day = 86400
    week_later = date_entered + (one_day*5)
    
    begin = max(date_entered,query.event_time)
    end = min(week_later,query1.event_time)
    
    json_list = []
    data_list = []
    date = datetime.datetime.fromtimestamp(begin)
    if int(date.strftime("%H"))>16:
        for i in range(8):
            data = {i:"No Data"}
            data_list.append(data)
        json_list.append(data_list)
            
        begin += one_day
    
    while begin<=end:

        date = datetime.datetime.fromtimestamp(begin)
        try:
            cur_data = getHistoricalData(rid, date.day, date.month, date.year)
        except:
            break
        json_list.append(cur_data)
        if date.strftime("%a") != "Fri":
            begin += one_day
        else:
            begin += (one_day*3)

    
    return json_list
    
    