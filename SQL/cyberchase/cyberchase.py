# -*- coding: utf-8 -*-
"""
Created on Fri May 17 10:16:18 2024

@author: Admin
"""
import sqlite3

try:
    # connect to database
    db = sqlite3.connect("E:\SQL\cyberchase\cyberchase.db")
    cursor = db.cursor()

    # Create database #。open E:\SQL\cyberchase\cyberchase.db                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
    cursor.execute("""CREATE TABLE IF NOT EXISTS Persons (PersonID INTEGER PRIMARY KEY AUTOINCREMENT,FirstName varchar(255),LastName varchar(255));""")

    # Insert data into database
    sql_statements = ["INSERT INTO Persons (FirstName,LastName) VALUES ('Charlie','Jackson');", "INSERT INTO Persons (FirstName,LastName) VALUES ('Scott','Jackson');", "INSERT INTO Persons (FirstName,LastName) VALUES ('Dave','Jackson');","INSERT INTO Persons (FirstName,LastName) VALUES ('Audrey','Plastiras');","INSERT INTO Persons (FirstName,LastName) VALUES ('Nikki','Plastiras');","INSERT INTO Persons (FirstName,LastName) VALUES ('Dave','Plastiras');","INSERT INTO Persons (FirstName,LastName) VALUES ('Grace','Plastiras');"]
    for statement in sql_statements:
        print(statement)
        cursor.execute(statement)

    db.commit()

except Exception as e:
    print("Connection failed: ", e)
    
    
print(cursor.execute('''PRAGMA table_info(episodes);''').fetchall())
'''[(0, 'id', 'INTEGER', 0, None, 1), (1, 'season', 'INTEGER', 0, None, 0), (2, 'episode_in_season', 'INTEGER', 0, None, 0), (3, 'title', 'TEXT', 0, None, 0), (4, 'topic', 'TEXT', 0, None, 0), (5, 'air_date', 'NUMERIC', 0, None, 0), (6, 'production_code', 'TEXT', 0, None, 0)]'''
def asw(file,queries):
    with open(file,'w') as f:
        f.write(queries)
#In 1.sql, write a SQL query to list the titles of all episodes in Cyberchase’s original season, Season 1.
print(cursor.execute('''select title from episodes where season==1;''').fetchall())
#must have exactly one of create/read/write/append mode
with open(r'E:\SQL\cyberchase\1.sql','w') as f:
    f.write('select title from episodes where season==1;')
#In 2.sql, list the season number of, and title of, the first episode of every season.    
print(cursor.execute('''select season,title from episodes where episode_in_season == 1''').fetchall())
asw(r'E:\SQL\cyberchase\2.sql','select season,title from episodes where episode_in_season == 1')
#In 3.sql, find the production code for the episode “Hackerized!”.
print(cursor.execute('select production_code from episodes where title == "Hackerized!";').fetchall())
asw(r'E:\SQL\cyberchase\3.sql','select production_code from episodes where title == “Hackerized!“;')
#In 4.sql, write a query to find the titles of episodes that do not yet have a listed topic
print(cursor.execute('select titles from episodes where topic is NULL;').fetchall())
asw(r'E:\SQL\cyberchase\4.sql','select titles from episodes where topic is NULL;')
#In 5.sql, find the title of the holiday episode that aired on December 31st, 2004.
print(cursor.execute('select title from episodes where air_date == "2004-12-31";').fetchall())
asw(r'E:\SQL\cyberchase\5.sql','select title from episodes where air_date == "2004-12-31";')
#In 6.sql, list the titles of episodes from season 6 (2008) that were released early, in 2007.
print(cursor.execute('select title from episodes where season==6 and air_date between "2007-01-01" and "2007-12-31";').fetchall())
asw(r'E:\SQL\cyberchase\6.sql','select title from episodes where season==6 and air_date between "2007-01-01" and "2007-12-31";')
#In 7.sql, write a SQL query to list the titles and topics of all episodes teaching fractions.
print(cursor.execute('select title,topic from episodes where topic LIKE "%fraction%";').fetchall())
asw(r'E:\SQL\cyberchase\7.sql','select title,topic from episodes where topic LIKE "%fraction%";')
#8.write a query that counts the number of episodes released in the last 6 years, from 2018 to 2023, inclusive.
print(cursor.execute('select count(id) from episodes where air_date between "2018-01-01" and "2023-12-31";').fetchall())
asw(r'E:\SQL\cyberchase\8.sql','select count(id) from episodes where air_date between "2018-01-01" and "2023-12-31";')
#In 9.sql, write a query that counts the number of episodes released in Cyberchase’s first 6 years, from 2002 to 2007, inclusive.
print(cursor.execute('select count(id) from episodes where air_date between "2002-01-01" and "2007-12-31";').fetchall())
asw(r'E:\SQL\cyberchase\9.sql','select count(id) from episodes where air_date between "2002-01-01" and "2007-12-31";')
#In 10.sql, write a SQL query to list the ids, titles, and production codes of all episodes. Order the results by production code, from earliest to latest.
print(cursor.execute('select id,title,production_code from episodes order by production_code ASC;').fetchall())
asw(r'E:\SQL\cyberchase\10.sql','select id,title,production_code from episodes order by production_code ASC;')
# 11.list the titles of episodes from season 5, in reverse alphabetical order.
print(cursor.execute('select title from episodes where season==5 order by title DESC;').fetchall())
asw(r'E:\SQL\cyberchase\11.sql','select title from episodes where season==5 order by title DESC;')
#In 12.sql, count the number of unique episode titles.
print(cursor.execute('select count(distinct title) from episodes;').fetchall())
asw(r'E:\SQL\cyberchase\12.sql','select count(distinct title) from episodes;')
#In 13.sql, write a SQL query to explore a question of your choice. This query should: Involve at least one condition, using WHERE with AND or OR
print(cursor.execute('select count(distinct title) from episodes where title like "%tree%";').fetchall())
asw(r'E:\SQL\cyberchase\13.sql','select count(distinct title) from episodes where title like "%tree%"；')

