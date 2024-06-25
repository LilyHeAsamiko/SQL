# -*- coding: utf-8 -*-
"""
Created on Fri May 17 10:16:18 2024

@author: Admin
"""
import sqlite3
import numpy as np

try:
    # connect to database
    db = sqlite3.connect(r"E:\SQL\private\private.db")
    cursor = db.cursor()

    db.commit()

except Exception as e:
    print("Connection failed: ", e)

#users items ordes user_logs    
print(cursor.execute(''' PRAGMA table_info(sentences);''').fetchall())
'''[(0, 'id', 'INTEGER', 0, None, 1), (1, 'sentence', 'TEXT', 1, None, 0)]'''

#write into hack.sql
def asw(file,queries):
    with open(file,'w') as f:
        f.write(queries)

'''
Your task at hand is to decode the cipher left for you by the detective. How you do so is up to you, but you should ensure that—at the end of your process—you have a view structured as follows:

The view should be named message
The view should have a single column, phrase
When the following SQL query is executed on private.db, your view should return a single column in which each row is one phrase in the message.
'''
# In private.sql, you should write all SQL statements required to replicate your creation of the view. That is:
#(sentenceN, characterN, lengthN)
#(sentenceText, characterN, lengthN)
'''If creating the view requires creating a separate table and inserting data into it, you should ensure that private.sql contains the statements to create that table and insert that data. (Don’t be afraid to add tables and add data as you wish!)
private.sql, when run a fresh instance of private.db, should be able to fully reconstruct your view.
'''
decipher = [
[14,98,4],
[114,3,5],
[618,72,9],
[630,7,3],
[932,12,5],
[2230,50,7],
[2346,44,10],
[3041,14,5],
]

print(cursor.execute('''create table temp as select sentence as Sentence, id as ID from sentences;''').fetchall())

for ns in decipher: 
#    number1 = ns[0] 
#    number2 = ns[1]
#    number3 = ns[2]
#    print(f'''{number1}''')
#    print(f'''{number2}''')
#    print(f'''{number3}''')
    print(ns[0],ns[1],ns[2])
    print(cursor.execute(f'''select substr("sentence" , {ns[1]}, {ns[2]}) from sentences where id == {ns[0]};''').fetchall())
    print(cursor.execute(f'''update temp set "Sentence" == (select substr("sentence" , {ns[1]}, {ns[2]}) from sentences where id == {ns[0]}) where ID == {ns[0]};''').fetchall())

print(cursor.execute(f'''create view message as select Sentence from temp;''').fetchall())
print(cursor.execute('''drop table "temp";''').fetchall())
print(cursor.execute('''select * from "temp";''').fetchall())


print(cursor.execute(f'''create view message as select * from temp where ID in {np.array(decipher,dtype = int).reshape(8,3)[:,0]};''').fetchall())
print(cursor.execute('''select * from "message";''').fetchall())

s1 = '''create table temp as select sentence as Sentence, id as ID from sentences;'''
s2 = '''update temp set "Sentence" == (select substr("sentence" , 98, 4) from sentences where id == 14) where ID == 14;'''
s3 = f'''create view message as select * from temp where ID in {np.array(decipher,dtype = int).reshape(8,3)[:,0]};'''
asw(r"E:\SQL\private\private.sql",s1+'\n'+s2+'\n'+s3)

