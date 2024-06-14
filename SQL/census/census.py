# -*- coding: utf-8 -*-
"""
Created on Fri May 17 10:16:18 2024

@author: Admin
"""
import sqlite3

try:
    # connect to database
    db = sqlite3.connect(r"E:\SQL\census\census.db")
    cursor = db.cursor()

    db.commit()

except Exception as e:
    print("Connection failed: ", e)

#users items ordes user_logs    
print(cursor.execute(''' PRAGMA table_info(census);''').fetchall())
'''[(0, 'id', 'INTEGER', 0, None, 1), (1, 'district', 'TEXT', 1, None, 0), (2, 'locality', 'TEXT', 1, None, 0), (3, 'families', 'INTEGER', 1, None, 0), (4, 'households', 'INTEGER', 1, None, 0), (5, 'population', 'INTEGER', 1, None, 0), (6, 'male', 'INTEGER', 1, None, 0), (7, 'female', 'INTEGER', 1, None, 0)]'''

#write into hack.sql
def asw(file,queries):
    with open(file,'w') as f:
        f.write(queries)

# In rural.sql, write a SQL statement to create a view named rural. This view should contain all census records relating to a rural municipality (identified by including “rural” in their name). Ensure the view contains all of the columns from the census table.#1|admin|e10adc3949ba59abbe56e057f20f883e
print(cursor.execute('''create view rural as select * from census where locality like "%rural%";''').fetchall())
asw(r'E:\SQL\census\rural.sql','create view rural as select * from census where locality like "%rural%";')

# In total.sql, write a SQL statement to create a view named total. This view should contain the sums for each numeric column in census, across all districts and localities. Ensure the view contains each of the following columns:
print(cursor.execute('''create view total as select sum(families) as families, sum(households) as households, sum(population) as population, sum(male) as males, sum(female) as females from census;''').fetchall())
asw(r'E:\SQL\census\total.sql','create view total as select sum(families) as families, sum(households) as households, sum(population) as population, sum(male) as males, sum(female) as females from census;')

#In by_district.sql, write a SQL statement to create a view named by_district. This view should contain the sums for each numeric column in census, grouped by district. 
print(cursor.execute('''create view "by_district" as select district,families,households,population,male,female from census group by district;''').fetchall())
asw(r'E:\SQL\census\by_district.sql','create view "by_district" as select district,families,households,population,male,female from census group by district;')

#In most_populated.sql, write a SQL statement to create a view named most_populated. This view should contain, in order from greatest to least, the most populated districts in Nepal. Ensure the view contains each of the following columns
print(cursor.execute('''create view "Most Populated" as select district,families,households,population,male,female from census order by population desc;''').fetchall())
asw(r'E:\SQL\census\.sql','create view "Most Populated" as select district,families,households,population,male,female from census order by population desc;')

