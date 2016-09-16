import pymysql
from src import json_creator as jc

def frequency_of_use(room):
	'''This function queries the database for the number of hours that a room has been in use
	and not in use respectively.'''

	frequency_data = []
	conn = pymysql.connect(host='localhost', user='root', password='summer')
	c = conn.cursor()

	c.execute("""
	SELECT 
    SUM(CASE WHEN mod_code IS NOT NULL THEN 1 ELSE 0 END) As not_null_num, 
    SUM(CASE WHEN mod_code IS NULL THEN 1 ELSE 0 END) AS null_num
	FROM wifi_db.timetable
	WHERE room_id = %s;""", (room,))

	data = c.fetchall()
	for i in data[0]:
		frequency_data.append(str(i))
	
	#json_output = jc.return_json(frequency_data)
	return frequency_data

def getModuleList():
	'''This function queries the database for all the distince modules that are listed in the 'timetable' table'''

	module_list = []
	conn = pymysql.connect(host='localhost', user='root', password='summer')
	c = conn.cursor()

	c.execute("""SELECT module_code FROM wifi_db.module
	""")

	data = c.fetchall()
	for i in data:
		module_list.append(str(i[0]))
	
	#json_output = jc.return_json(frequency_data)
	return module_list

def getBuildingInfo(bid):
	'''Returns the stored information for a specific building in the database'''
	building_data = []
	conn = pymysql.connect(host='localhost', user='root', password='summer')
	c = conn.cursor()

	c.execute("""SELECT * FROM wifi_db.building WHERE code = %s""", (bid,))

	data = c.fetchall()
	for i in data:
		building_data.append((i))

	return building_data

def getBuildingRoomInfo(bid):
	'''Returns a list of all the rooms and capacities of the rooms that are listed to be associated with a 
	particular building'''

	building_room_data = []
	conn = pymysql.connect(host='localhost', user='root', password='summer')
	c = conn.cursor()

	c.execute("""SELECT code, room_cap FROM wifi_db.room WHERE building_code = %s""", (bid,))

	data = c.fetchall()
	for i in data:
		building_room_data.append((i))

	return building_room_data

def getModuleCapacity(mid):
	'''Returns the number of registered students for a particular model according to the 'timetable' table'''
	building_room_data = []
	conn = pymysql.connect(host='localhost', user='root', password='summer')
	c = conn.cursor()

	c.execute("""SELECT distinct(reg_stu) FROM wifi_db.timetable WHERE mod_code = %s""", (mid,))

	data = c.fetchall()

	return data[0][0]



def getDay(day):
	'''Returns the day of the week as it is represented in SQLite as a string that can be used for comparison'''
	days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
	return days.index(day)