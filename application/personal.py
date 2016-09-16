import datetime

def stuff(rid, time_stamp):
    
    time_stamp = "02-11-2015"
    string = time_stamp.split("-")
    
    query = wifi_log.select().order_by(wifi_log.event_time).get()
    query1 = wifi_log.select().order_by(wifi_log.event_time.desc()).get()
    date_entered = (datetime.datetime(int(string[2]),int(string[1]),int(string[0]))- datetime.datetime(1970,1,1)).total_seconds()
    one_day = 86400
    week_later = date_entered + (one_day*5)
    
    begin = max(date_entered,query.event_time)
    end = min(week_later,query1.event_time)
    
    json_list = []
    date = datetime.datetime.fromtimestamp(begin)
    if int(date.strftime("%H"))>16:
        for i in range(8):
            data = {i:"No Data"}
            json_list.append(data)
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


[{"building": "schoolofcomputerscience", "event_month": 11,
   "occupancy_pred": 1.76904, "assoc_devices": 2.0, "occupancy": 0.0,
    "binary_occupancy": 1, "room_id": 2, "occupancy_category_5": 0.0,
    "auth_devices": 2.0, "event_year": 2015,
   "event_hour": 9, "event_day": 3, "capacity": 90.0, "occupancy_category_3": 0, "index": 0}
