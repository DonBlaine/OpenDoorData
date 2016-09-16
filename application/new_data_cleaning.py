#This file takes new wifi log data and cleans it for database submission

import zipfile
import os
import csv
import shutil
import time

def main():
    os.chdir("..")
    while True:
        while os.path.isfile(r"Data\new_data\CSI WiFiLogs.zip"): 
               
            zip1 = zipfile.ZipFile(r"Data\new_data\CSI WiFiLogs.zip")  
            zip1.extractall(r'Data\new_data')
            
            path = r'Data\new_data'
            epoch_time = str(int(time.time()))
            shutil.move(r"Data\new_data\CSI WiFiLogs.zip", r"Data\archived_data\CSI WiFiLogs"+epoch_time+".zip")
            
            filelist = []
            for root, dirs, files in os.walk(path, topdown = True):
                for name in files:
                    filelist.append(os.path.join(root, name))
                
            for file in filelist:
                zip1 = zipfile.ZipFile(file)  
                zip1.extractall(r'Data\new_data')
                os.remove(file)
         
            
            filelist = []
            for root, dirs, files in os.walk(path, topdown = True):
                for name in files:
                    filelist.append(os.path.join(root, name))
            
            fc = open(r"Data\new_cleaned_data\full.csv", 'w', newline='')
            a = csv.writer(fc, delimiter=',')
            
        
            for file in filelist:
                 
                with open(file, 'r') as f:
                    mycsv= csv.reader(f)
                    mylist = list(mycsv)
                     
                for i in range(0,len(mylist)):
                    if mylist[i][0] == "Key":
                        startindex = i + 1
                        break
                     
                for i in range(startindex,len(mylist)):
                    a.writerows([mylist[i]])
                
                os.remove(file)
                         
            fc.close()

        time.sleep(300)
    
if __name__ == "__main__":
    main()


