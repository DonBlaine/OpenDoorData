# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 15:31:15 2016

@author: Elayne Ruane
"""

import zipfile
import os
import csv

def create_path(path):
    ''' function that creates a path if it does not already exist
    
    parameters
    ----------
    path: a string that represents the path to be created
    '''
    path = path
    if not os.path.exists(path):
        os.makedirs(path)

def extract_zip(zipa, path):
    '''function that extracts files from a zip file
    
    parameters
    ----------
    zipa: a string that represents the path to a zip file
    path: a string that represents the directory to extract the files to
    '''
    zipa = zipfile.ZipFile(zipa)
    zipa.extractall(path)
    
def filelist(path):
    '''function that adds all files in a path to a list
    
    parameters
    ----------
    path: a string that represents the directory where the files are located
    '''
    # create empty list
    filelist = []
    for root, dirs, files in os.walk(path, topdown = True):
        for name in files:
            filelist.append(os.path.join(root, name))
    return filelist

def delimiter(file):
    '''function that XXX
    
    parameters
    ----------
    file: string representing a file that contains data to be delimited
    '''
    file = open(file, 'w', newline='')
    # Return a writer object responsible for converting the user’s data into delimited strings
    file = csv.writer(file, delimiter=',')
    return file
    
def create_csvlist(filelist):
    '''function that creates a list of data from a list of csv files
    
    parameters
    ----------
    filelist: list of csv files containing data to be put in list
    '''
    for file in filelist:
        with open(file, 'r') as f:
            mycsv= csv.reader(f)
            mylist = list(mycsv)
    return mylist
    
def write_to_file(file, lista):
    '''function that XXX
    
    parameters
    ---------
    file: XXX
    lista: XXX
    '''
    for i in range(0,len(lista)):
        if lista[i][0] == "Key":
            startindex = i + 1
            break
        
    for i in range(startindex,len(lista)):
        file.writerows([lista[i]])
    return file
  
