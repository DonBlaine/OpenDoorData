import zipfile
import os
import csv

def main():
    os.chdir("..")
    newpath = r'Data\original_dirty_data\WiFiLogs'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        
    zip1 = zipfile.ZipFile(r"Data\original_dirty_data\CSI WiFiLogs.zip")  
    zip1.extractall(r'Data\original_dirty_data\WiFiLogs')
    
    path = r'Data\original_dirty_data\WiFiLogs'
    
    filelist = []
    for root, dirs, files in os.walk(path, topdown = True):
        for name in files:
            filelist.append(os.path.join(root, name))
            
    newpath = r'Data\original_dirty_data\unzipLogs' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        
    for file in filelist:
        zip1 = zipfile.ZipFile(file)  
        zip1.extractall(r'Data\original_dirty_data\unzipLogs')
        
    
    path = r'Data\original_dirty_data\unzipLogs' 
    
    filelist = []
    for root, dirs, files in os.walk(path, topdown = True):
        for name in files:
            filelist.append(os.path.join(root, name))
    
    fc = open(r"Data\original_cleaned_data\full.csv", 'w', newline='')
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
                 
    fc.close()
    
# To parse individual rooms use the following:     
#     f2 = open(r"cleaned_data\b002.csv", 'w', newline='')
#     a2 = csv.writer(f2, delimiter=',')
#      
#     f3 = open(r"cleaned_data\b003.csv", 'w', newline='')
#     a3 = csv.writer(f3, delimiter=',')
#      
#     f4 = open(r"cleaned_data\b004.csv", 'w', newline='')
#     a4 = csv.writer(f4, delimiter=',')
#      
#     file = r"cleaned_data\full.csv"
#      
#     with open(file, 'r') as f:
#         mycsv= csv.reader(f)
#         mylist = list(mycsv)
#          
#     third = int(len(mylist)/3)
#      
#     for i in range(third):
#         a2.writerows([mylist[i]])
#      
#     for i in range(third,(third*2)):
#         a3.writerows([mylist[i]])
#          
#     for i in range((third*2),len(mylist)):
#         a4.writerows([mylist[i]])
#          
#     f2.close()
#     f3.close()
#     f4.close()
    
if __name__ == "__main__":
    main()
