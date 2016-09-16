# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 12:09:03 2016

@author: Elayne Ruane

This file contains functions for use in model.py
"""


import pandas as pd
# import time and parse for cleaning data
import time
from dateutil.parser import parse

import re

def isempty_df(df):
    '''function that returns True if data was successfully loaded into a dataframe
    df: a dataframe to test
    
    '''
    rows = df.shape[0]
    cols = df.shape[1]
    
    if rows > 0 and cols > 0:
        return False
    else:
        return True


def convert_to_epoch(df, column):
    '''function that reads in a dataframe with a column containing values in timestamp format and converts those values to epoch forma
   
    requires module time and parse function from dateutil.parser
    
    paramaters
    ----------
    df: a dataframe containing 'column'
    column: a string that denotes the name of the column containing values in timestamp format
    '''  
    
    #for loop that iterates through each row in the dataframe
    for i in range(df.shape[0]):
        # variable 'x' is assigned the value from the column and row 'i'
        x = df[column][i]
        # replace GMT with UTC so function is os agnostic
        string = x.lower().replace('gmt', 'UTC')
        # variable 'y' is assigned the result of variable 'x' passed through the parse method
        string = parse(string)
        # variable 'epoch' is assigned 'y' value converted to epoch time
        epoch = int(time.mktime(string.timetuple()))
        # set column value to value of variable 'epoch'
        df.set_value(i, column, epoch)
    return df
    

def room_number(df, room_column):
    '''function that reads in a dataframe with a column containing room information in the format 'campus > building > roomcode-xxx' 
    and replaces the values in the column with just the room ID which is the last character of the string in that column.    
    '''
    # for loop that iterates through each row in the df
    for i in range(df.shape[0]):
        # selects last character of the string in the room_column which is the room ID
        df.set_value(i, room_column, re.findall('\\b\\d+\\b', df[room_column][i])[0])
    return df


def estimate_occ(df,room, occupancy_rate):
    '''function that caluclates the estimated number of room occupants
    This function is designed to only work for B002, B003, and B004
    
    parameters
    ----------
    df: a dataframe with columns 'room' and 'occupancy_rate'
    room: a string denoting a column in df that contains INT values representing room IDs
    occupancy_rate: a string denoting a column in df that contains DECIMAL values that represent the estimated room occupancy rate
    
    '''
    #for loop that iterates through each row of the df
    for i in range(df.shape[0]):
        
        #room two and three have capacity of 90
        if df[room][i] == 2 or df[room][i] == 3:
            # calculate estimated occupants for row, assign to variable 'est'
            est = df[occupancy_rate][i] * 90
            #set value in new column
            df.set_value(i, 'est_occupants', est)
        
        #room four has a capcity of 220
        elif df[room][i] == 4:
            est = df[occupancy_rate][i] * 220
            df.set_value(i, 'est_occupants', est)
        
        else:
            raise ValueError('Incorrect room number:', df[room][i])
            return
    return df


def dataframe_epochtime_to_datetime(df, epoch_time):
    '''Converts the epoch time data in the dataframe into human readable format (datetime)
    Year, Month, Day, Hour and Minute are each put in a new column in order to allow for data merging

    parameters
    ----------
    df: a dataframe
    epoch_time: the name of the column containing the time in epoch format.

    Returns
    ----------
    Returns the dataframe with normalized time information
    '''


    df[epoch_time] = pd.to_datetime(df.event_time, unit='s')
    df.set_index(epoch_time, inplace=True)

    df['event_year'] = df.index.year
    df['event_month'] = df.index.month
    df['event_day'] = df.index.day
    df['event_hour'] = df.index.hour

    return df