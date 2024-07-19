# -*- coding: utf-8 -*-
"""
Created on Fri May 17 10:16:18 2024

@author: Qin_LilyHeAsamiko
"""
import sqlite3

try:
    # connect to database
    db = sqlite3.connect("E:\SQL\harvard\harvard.db")
    cursor = db.cursor()

    db.commit()

except Exception as e:
    print("Connection failed: ", e)

#users items ordes user_logs    
print(cursor.execute(''' PRAGMA table_info(students);''').fetchall())
'''[(0, 'id', 'INTEGER', 0, None, 1), (1, 'name', 'TEXT', 1, None, 0)]'''

#write into hack.sql
def asw(file,queries):
    with open(file,'w') as f:
        f.write(queries)

#In indexes.sql, write a set of SQL statements that create indexes which will speed up typical queries on the harvard.db database. The number of indexes you create, as well as the columns they include, is entirely up to you. Be sure to balance speed with disk space, only creating indexes you need.
#When engineers optimize a database, they often care about the typical queries run on the database. Such queries highlight patterns with which a database is accessed, thus revealing the best columns and tables on which to create indexes. Click the spoiler tag below to see the set of typical SELECT queries run on harvard.db.print(cursor.execute('''CREATE INDEX "search_users_by_last_login" ON "users"("last_login_date");''').fetchall())
print(cursor.execute('''CREATE INDEX "search_course_id_by_student_id" ON "enrollments"("student_id");''').fetchall())
print(cursor.execute('''select number,title,department,semester from cources where id in (select course_id from enrollments indexed by search_course_id_by_student_id where student_id > 24999);''').fetchall())
#write above example test
asw(r"E:\SQL\harvard\indexes.sql",'CREATE INDEX "search_course_id_by_student_id" ON "enrollments"("student_id");\n'+'select number,title,department,semester from cources where id == (select "course_id" indexed by search_course_id_by_student_id where student_id > 24999);\n'+'select number,title,department,semester from cources where id in (select course_id from enrollments indexed by search_course_id_by_student_id where student_id > 24999);')
print(cursor.execute('''CREATE INDEX "search_requirements_id_by_course_id" ON "satisfies"("course_id");''').fetchall())
print(cursor.execute('''select name from requirements where id in (select requirement_id from satisfies indexed by search_requirements_id_by_course_id where course_id > 1);''').fetchall())
asw(r"E:\SQL\harvard\indexes.sql",'CREATE INDEX "search_course_id_by_student_id" ON "enrollments"("student_id");\n'+'select number,title,department,semester from cources where id == (select "course_id" indexed by search_course_id_by_student_id where student_id > 24999);\n'+'CREATE INDEX "search_requirements_id_by_course_id" ON "satisfies"("course_id");\n'+'select name from requirements where id in (select requirement_id from satisfies indexed by search_requirements_id_by_course_id where course_id > 1);')
