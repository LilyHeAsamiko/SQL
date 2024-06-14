# -*- coding: utf-8 -*-
"""
Created on Fri May 17 10:16:18 2024

@author: Admin
"""
import sqlite3
import pandas as pd
import numpy as np 

with open(r'E:\SQL\meteorites\meteorites.csv') as f:
        #lines = csv.reader(f)
#        data = list(f.lines)
        meteoritesTBL = pd.read_csv(f)
        data = pd.DataFrame(meteoritesTBL).copy()
        

#pre-process
#generally missing only happens with float or int type, as in column mass,year,lat,long 
#pandas can view with iloc[i][j], yet change value only with iloc[i,j]
for nRow in range(np.shape(data)[0]):
    #about name(only if sep with space)
    '''if type(data.iloc[nRow][1]) is not type(data.iloc[1][1]):
        if type(data.iloc[nRow][2]) == type(data.iloc[1][0]) and data.iloc[nRow][2] != 'Valid':
            data.iloc[nRow][0] += data.iloc[nRow][1]+data.iloc[nRow][2]
            data.iloc[nRow][1:] = data.iloc[nRow][3:]
        elif data.iloc[nRow][2] != 'Valid':   
            data.iloc[nRow][0] += data.iloc[nRow][1]
            data.iloc[nRow][1:] = data.iloc[nRow][2:]'''
    #about mass
    if data.iloc[nRow][4] in ['Fell','Found','Discovery','Relict']:
        data.iloc[nRow,5:9] = data.iloc[nRow,4:8]
        data.iloc[nRow,4] = ''        
#        print(data.iloc[nRow][4])
    #about year
    if type(data.iloc[nRow][6]) == type(data.iloc[1][6]): 
        if np.isnan(data.iloc[nRow][6]):  
            data.iloc[nRow,7:9] = data.iloc[nRow,6:8]
            data.iloc[nRow,6] = ''
        elif int(data.iloc[nRow][6]) <= 180:
            data.iloc[nRow,7:9] = data.iloc[nRow,6:8]
            data.iloc[nRow,6] = ''
#        print(data.iloc[nRow][6])
    #missing lat is the same as missing long, type float, between -180 and 180    
    #data.iloc[nRow] = ['' for i in data.iloc[nRow] if np.isnan(i)]
    for dat in [data.iloc[nRow,4],data.iloc[nRow,6],data.iloc[nRow,7],data.iloc[nRow,8]]:
        print(dat)
        if dat != '':
            if np.isnan(float(dat)):
                dat = '' 

data.to_csv(r"E:\SQL\meteorites\datapro.csv",index = False)
    
try:
    # connect to database
    db = sqlite3.connect(r"E:\SQL\meteorites\meteorites.db")
    cursor = db.cursor()

    # Create database #.open E:\SQL\dont-panic\don-panic.db                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
    cursor.execute("""CREATE TABLE IF NOT EXISTS Meteorites (name text,id INTEGER PRIMARY KEY AUTOINCREMENT, nametype text, class varchar(255), mass integer, discovery text, year integer, lat integer, long integer);""")

    # Insert data into database
#    for row in data:
#        statement = f'''INSERT INTO Meteorites (name, id, nametype, class, mass, discovery, year, lat, long) values, {row}'''
    for nRow in range(np.shape(data)[0]):
        statement = f'''INSERT INTO Meteorites (name, id, nametype, class, mass, discovery, year, lat, long) values ({data.iloc[nRow]});'''
        print(statement)
        print(cursor.execute(statement).fetchall())

    db.commit()

except Exception as e:
    print("Connection failed: ", e)

#users items ordes user_logs    
print(cursor.execute(''' PRAGMA table_info(Meteorites);''').fetchall())
'''[(0, 'name', 'text', 0, None, 0), (1, 'id', 'INTEGER', 0, None, 1), (2, 'nametype', 'text', 0, None, 0), (3, 'class', 'varchar(255)', 0, None, 0), (4, 'mass', 'integer', 0, None, 0), (5, 'discovery', 'text', 0, None, 0), (6, 'year', 'integer', 0, None, 0), (7, 'lat', 'integer', 0, None, 0), (8, 'long', 'integer', 0, None, 0)]'''

'''In import.sql, write a series of SQL (and SQLite) statements to import and clean the data from meteorites.csv into a table, meteorites, in a database called meteorites.db.

Within meteorites.db, the meteorites table should have the following columns:

Columns in the meteorites table
Keep in mind that not all columns in the CSV should end up in the final table!

To consider the data in the meteorites table clean, you should ensure…
'''
#Any empty values in meteorites.csv are represented by NULL in the meteorites table.
for item in ['nametype','mass', 'year', 'lat', 'long']:
    checkEmpty = f'''select * from Meteorites where {item} is '';'''
    print(cursor.execute(checkEmpty).fetchall())
    nullEmpty = f'''update Meteorites set {item} = NULL where {item} = '';'''
    print(cursor.execute(nullEmpty).fetchall())
    rechecks = f'''select * from Meteorites where {item} is NULL'''
    print(cursor.execute(rechecks).fetchall())
    #All columns with decimal values (e.g., 70.4777) should be rounded to the nearest hundredths place (e.g., 70.4777 becomes 70.48).
    if item in ['mass', 'lat', 'long']:  
        statement = f'''update Meteorites set {item} = round({item},2);'''
        print(statement)
        print(cursor.execute(statement).fetchall())
    #All meteorites with the nametype “Relict” are not included in the meteorites table
    if item == 'nametype':  
        statement = f'''delete * from Meteorites where {item} == "Relict";'''
        print(statement)
        print(cursor.execute(statement).fetchall())
    #The meteorites are sorted by year, oldest to newest, and then—if any two meteorites landed in the same year—by name, in alphabetical order.
    statements = f'''select * from Meteorites order by "year","name" asc;'''
    print(cursor.execute(statements).fetchall())
    #You’ve updated the IDs of the meteorites from meteorites.csv, according to the order specified in #4.
    statement1 = f'''create table Metorites_N as select * from Meteorites order by "year","name" asc;'''
    print(cursor.execute(statement1).fetchall())
    statement2 = f'''set Metorites_N id = (select id from Meteorite);'''
    print(cursor.execute(statement2).fetchall())
    
    


#write into hack.sql
def asw(file,queries):
    with open(file,'w') as f:
        f.write(queries)

asw = '.separator "\t"'
asw0 = '.import '+r"E:\SQL\meteorites\dataprocessed.csv"+' Meteorites'
asw00 = 'create table Meteorites_copy as select * from Meteorites;'
asw11 ='update Meteorites_copy set "mass"= NULL where "mass" = "";'
asw12 = 'update Meteorites_copy set "year"= NULL where "year" = "";'
asw13 = 'update Meteorites_copy set "lat"= NULL where "lat" = "";'
asw14 = 'update Meteorites_copy set "long"= NULL where "long" = "";'
asw21 = 'update Meteorites_copy set "mass" = round("mass",2);'
asw22 = 'update Meteorites_copy set "lat" = round("lat",2);'
asw23 = 'update Meteorites_copy set "long" = round("long",2);'
asw31 = 'delete from Meteorites_copy where nametype is "Relict";'
asw41 = 'create table Meteorites_N as select * from Meteorites order by “year”, “name” asc;'
asw42 = 'update Meteorites_N set id = (select id from Meteorites);'

final = '\n'.join([asw,asw0,asw00,asw11,asw12,asw13,asw14,asw21,asw22,asw23,asw31,asw41,asw42])
asw(r'E:\SQL\meteorites\import.sql',f'{final}')

db.close()