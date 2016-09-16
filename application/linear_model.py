# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 11:36:54 2016

@author: Elayne Ruane

"""

# ---------- IMPORT NECESSARY LIBRARIES

import os
import pandas as pd
import statsmodels.formula.api as sm
from model_functions import isempty_df
from model_functions import convert_to_epoch
from model_functions import room_number
from model_functions import estimate_occ
from model_functions import dataframe_epochtime_to_datetime
import numpy as np
import models


def get_linear_coef(folder, file_1, file_2):
    '''This function contains a linear regression model that predicts the number of
    people in a room based on the number of devices connected to wifi access points
    in that room.

    The accuracy of the model can be tested by occupancy data collected via survey.

    Wifi logs contain readings at five minute intervals. We use the median number
    of devices connected per hour.

    The model was originally prepared in iPython notebooks.
    
    Parameters
    ----------
    folder: the folder containing file_1 and file_2
    file_1: file containing wifi log data with data fields 'room', 'event_time', 'ass', and 'auth'
    file_2: file containing survey data

    Returns
    ----------
    coef (float): the linear coefficient'''

    # ---------- READ DATA FROM CSV FILES INTO DATAFRAME

    # Read file
    # OS agnostic -- should work on Mac / Windows / Linux
    folder = folder
    file_full_data = file_1
    file_survey_data = file_2

    print(os.getcwd())
    pathw = os.path.join('Data', folder, file_full_data)
    paths = os.path.join('Data', folder, file_survey_data)
    print(pathw)
    print(paths)

    wifi_df = pd.read_csv(pathw, names=['room', 'event_time', 'ass', 'auth'])
    occupancy_df = pd.read_csv(paths)


    # Test if files were read correctly
    # If the program was not able to read the files, the dataframes are empty
    # The below statement would return an exception and terminate the execution of the code
    if isempty_df(wifi_df) or isempty_df(occupancy_df):
        print("Error: data was not loaded on the dataframe")
        print("Calculation of the coefficient impossible: missing data")
        if isempty_df(wifi_df):
            print("empty dataframe: wifi_df")
        if isempty_df(occupancy_df):
            print("empty dataframe: occupancy_df")
        return KeyError

    # ---------- CLEAN DATA FOR MODEL

    del occupancy_df['Unnamed: 0'] # delete unwanted column


    # convert 'event_time' values from timestamp to epoch so can convert to DATETIME
    convert_to_epoch(wifi_df, 'event_time')
    # Clean room number (convert to integer)
    room_number(wifi_df, 'room')

    # convert 'event_time' values from EPOCH to DATETIME in both dataframes
    wifi_df = dataframe_epochtime_to_datetime(wifi_df, "event_time")
    occupancy_df = dataframe_epochtime_to_datetime(occupancy_df, "event_time")

    # get median hourly values for each day for each room and put in 'median_df' dataframe
    median_df = wifi_df.groupby(['room', 'event_day', 'event_hour'], as_index=False).median()

    # merge median data and occupancy data into single dataframe, 'df'
    median_df['room'] = median_df['room'].astype(int)
    df = pd.merge(median_df, occupancy_df, on=['room', 'event_day', 'event_hour'], how='inner')


    # ---------- DATA ANALYSIS

    # estimate the number of occupancts from the survey data to assess model accuracy
    estimate_occ(df, 'room', 'occupancy')


    # ---------- CREATE AND TRAIN THE MODEL

    # can also use associated but higher correlation with authenticated
    lm = sm.ols(formula='est_occupants ~ auth', data=df).fit()

    coef = lm.params.auth

    #convert the coefficient from dtype numpy.float64 to native python float type
    #if left as numpy.float64, creates an error when trying to input it to the database using peewee
    coef = np.asscalar(np.float64(coef))

    return coef


if __name__ == "__main__":
    os.chdir("..")
    coef = get_linear_coef(r'Data/original_cleaned_data', r'full.csv', r'survey_data.csv')
    #setting weight to be linear model coef
    models.regressionModel.create(weight = coef)
    print("Linear coefficient:", coef)