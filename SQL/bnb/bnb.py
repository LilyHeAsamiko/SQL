# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 23:24:15 2024

@author: Admin
"""

import sqlite3

try:
    # connect to database
    db = sqlite3.connect(r"E:\SQL\bnb\bnb.db")
    cursor = db.cursor()

    # Create database #.open E:\SQL\views\views.db                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
    cursor.execute("""CREATE TABLE IF NOT EXISTS Persons (PersonID INTEGER PRIMARY KEY AUTOINCREMENT,FirstName varchar(255),LastName varchar(255));""")

    # Insert data into database
    sql_statements = ["INSERT INTO Persons (FirstName,LastName) VALUES ('Charlie','Jackson');", "INSERT INTO Persons (FirstName,LastName) VALUES ('Scott','Jackson');", "INSERT INTO Persons (FirstName,LastName) VALUES ('Dave','Jackson');","INSERT INTO Persons (FirstName,LastName) VALUES ('Audrey','Plastiras');","INSERT INTO Persons (FirstName,LastName) VALUES ('Nikki','Plastiras');","INSERT INTO Persons (FirstName,LastName) VALUES ('Dave','Plastiras');","INSERT INTO Persons (FirstName,LastName) VALUES ('Grace','Plastiras');"]
    for statement in sql_statements:
        print(statement)
        cursor.execute(statement)

    db.commit()

except Exception as e:
    print("Connection failed: ", e)

    
print(cursor.execute('''PRAGMA table_info(listings);''').fetchall())
'''[(0, 'id', 'INTEGER', 0, None, 1), (1, 'property_type', 'TEXT', 0, None, 0), (2, 'host_name', 'TEXT', 0, None, 0), (3, 'accommodates', 'INTEGER', 0, None, 0), (4, 'bedrooms', 'INTEGER', 0, None, 0), (5, 'description', 'TEXT', 0, None, 0)]'''
def asw(file,queries):
    with open(file,'w') as f:
        f.write(queries)
        
print(cursor.execute('''SELECT * FROM "listings" LIMIT 5;''').fetchall())    
        
#In no_descriptions.sql, write a SQL statement to create a view named no_descriptions that includes all of the columns in the listings table except for description.print(cursor.execute('''select "0m" from normals where latitude=="42.5" and longitude == "-69.5";''').fetchall())
print(cursor.execute('''create view no_descriptions as select * from listings where not exists (select * from description);''').fetchall())   
asw(r'E:\SQL\bnb\no_descriptions.sql','''create view no_descriptions as select * from listings where not exists (select * from description);''')
print(cursor.execute('''SELECT * FROM no_descriptions;''').fetchall())    

#In one_bedrooms.sql, write a SQL statement to create a view named one_bedrooms. This view should contain all listings that have exactly one bedroom. Ensure the view contains the following columns:
'''id, which is the id of the listing from the listings table.
property_type, from the listings table.
host_name, from the listings table.
accommodates, from the listings table.'''
print(cursor.execute('''create view one_bedroom as select id,property_type,host_name,accomodates from listings;''').fetchall())
asw(r'E:\SQL\bnb\one_bedroom.sql','''create view one_bedroom as select id,property_type,host_name,accommodates from listings;''')
print(cursor.execute('''SELECT * FROM one_bedroom;''').fetchall())    

#In frequently_reviewed.sql, write a SQL statement to create a view named frequently_reviewed. This view should contain the 100 most frequently reviewed listings, sorted from most- to least-frequently reviewed. Ensure the view contains the following columns:
'''id, which is the id of the listing from the listings table.
property_type, from the listings table.
host_name, from the listings table.
reviews, which is the number of reviews the listing has received 
'''
print(cursor.execute('''create view frequently_reviewed as select A.id as id,A.property_type as property_type,A.host_name as host_name , count(B.id) as reviews from listings A inner join reviews B on A.id == B.listing_id order by reviews DESC, property_type ASC,host_name ASC limit 100;''').fetchall())
asw(r'E:\SQL\bnb\frequently_reviewed.sql','''create view frequently_reviewed as select A.id as id,A.property_type as property_type,A.host_name as host_name , count(B.id) as reviews from listings A inner join reviews B on A.id == B.listing_id order by reviews DESC, property_type ASC,host_name ASC limit 100;''')
print(cursor.execute('''SELECT * FROM frequently_reviewed;''').fetchall())    
#june_vacancies.sql, write a SQL statement to create a view named june_vacancies. This view should contain all listings and the number of days in June of 2023 that they remained vacant. Ensure the view contains the following columns:.

'''
id, which is the id of the listing from the listings table.
property_type, from the listings table.
host_name, from the listings table.
days_vacant, which is the number of days in June of 2023, that the given listing was marked as available.
'''
print(cursor.execute('''select A.id as id,A.property_type as property_type,A.host_name as host_name, count(B.price) as "days_vacant" from listings A inner join availabilities B on A.id == B.listing_id where B.date between "2023-06-01" and "2023-06-30" and B.available is "TRUE";''').fetchall());
asw(r'E:\SQL\bnb\june_vacancies.sql','''select A.id as id,A.property_type as property_type,A.host_name as host_name, count(B.price) as "days_vacant" from listings A inner join availabilities B on A.id == B.listing_id where B.date between "2023-06-01" and "2023-06-30" and B.available is "TRUE";''')
print(cursor.execute('''SELECT * FROM june_vacancies;''').fetchall())    
