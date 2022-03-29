# UREL VAN WILLIAM BERMUDO BSCS, 2ND YEAR, CCC151, SIS HOMEOWORK
# The purpose of this module is to manipulate csv file for the SIS project
# THIS IS NOT THE MAIN FILE, PLEASE EXECUTE MAIN_BermudoSISapp.py

from msilib import sequence
from operator import index
import os
import sys
import pandas as pd



defaultFile = f'{sys.path[0]}/Student Records(For Testing).csv'     # default file, can be romved
mainfile = ''      # file that will be manipulated
   

def addStudent(idnumber, fullname, course, year, gender, filename):
    data = [[idnumber,fullname,course,year,gender]]
    newRow = pd.DataFrame(data)
    newRow.to_csv(filename, mode='a',index=False, header = False)


def searchStudent(idnumber,filename, rowskip = None):
    str(idnumber)
    df = pd.read_csv(filename)
    for i in range(0, len(df.index)):
        if (rowskip != None and i == rowskip):
            continue
        elif (idnumber == df.loc[i].at['ID Number']):
            return i
    return -1
                

def editstudent(idnumber, fullname, course, year, gender, filename,row):
    df = pd.read_csv(filename)
    df.loc[row] = idnumber, fullname, course, year, gender
    df.to_csv(filename, index = False)


def deletestudent(row,filename):
    df = pd.read_csv(filename)
    df = df.drop([row], axis=0)
    df.to_csv(filename, index = False)
    return df

def makeDefaultFile():
    if (os.path.exists(defaultFile) == False):
        my_default = pd.DataFrame([['2020-1971','Urel Van William Bermudo', 'BSCS', '2','Male'],
                                ['2019-2000','This File Is For Testing', 'BSIT', '3','Male'],
                                ['2021-1971','Jean Angeles', 'BSCS', '1','Female']],    
                                columns=['ID Number','Full Name','Course','Year Level','Gender']) 
        my_default.to_csv(defaultFile, index = False) 

