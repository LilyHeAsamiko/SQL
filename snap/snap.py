# -*- coding: utf-8 -*-
"""
Created on Fri May 17 10:16:18 2024

@author: LilyHeAsamiko
"""
import sqlite3

try:
    # connect to database
    db = sqlite3.connect(r"E:\SQL\snap\snap.db")
    cursor = db.cursor()

    db.commit()

except Exception as e:
    print("Connection failed: ", e)

#users items ordes user_logs    
print(cursor.execute(''' PRAGMA table_info(users);''').fetchall())
'''[(0, 'id', 'INTEGER', 0, None, 1), (1, 'district', 'TEXT', 1, None, 0), (2, 'locality', 'TEXT', 1, None, 0), (3, 'families', 'INTEGER', 1, None, 0), (4, 'households', 'INTEGER', 1, None, 0), (5, 'population', 'INTEGER', 1, None, 0), (6, 'male', 'INTEGER', 1, None, 0), (7, 'female', 'INTEGER', 1, None, 0)]'''

#write into hack.sql
def asw(file,queries):
    with open(file,'w') as f:
        f.write(queries)

#The app’s user engagement team needs to identify active users. Find all usernames of users who have logged in since 2024-01-01. Ensure your query uses the search_users_by_last_login index, which is defined as follows
print(cursor.execute('''CREATE INDEX "search_users_by_last_login" ON "users"("last_login_date");''').fetchall())
print(cursor.execute('''select username from users indexed by search_users_by_last_login where last_login_date >= 2024-01-01;''').fetchall()) 
asw(r'E:\SQL\snap\1.sql','CREATE INDEX "search_users_by_last_login" ON "users"("last_login_date");\n'+'select username from users indexed by search_users_by_last_login where last_login_date >= 2024-01-01;')

#Users need to be prevented from re-opening a message that has expired. Find when the message with ID 151 expires. You may use the message’s ID directly in your query.
print(cursor.execute('''CREATE INDEX "search_expire_time_by_id" ON "messages"("id");''').fetchall())
print(cursor.execute('''select expires_timestamp from messages indexed by "search_expire_time_by_id" where id = 151;''').fetchall())
asw(r'E:\SQL\snap\2.sql','CREATE INDEX "search_expire_time_by_id" ON "messages"("id");\n'+'select expires_timestamp from messages indexed by "search_expire_time_by_id" where id = 151;')

#The app needs to rank a user’s “best friends,” similar to Snapchat’s “Friend Emojis” feature. Find the user IDs of the top 3 users to whom creativewisdom377 sends messages most frequently. Order the user IDs by the number of messages creativewisdom377 has sent to those users, most to least.
#print(cursor.execute('''select to_user_id,count(to_user_id) from messages group by to_user_id order by count(to_user_id) where from_user_id == 2318;''').fetchall())
print(cursor.execute('''CREATE INDEX "search_messages_by_from_user_id" ON "messages"("from_user_id");''').fetchall())
print(cursor.execute('''select to_user_id,count(to_user_id) from messages indexed by search_messages_by_from_user_id where from_user_id == 2318 group by to_user_id order by count(to_user_id) DESC limit 3; ''').fetchall())
asw(r'E:\SQL\snap\3.sql','CREATE INDEX "search_messages_by_from_user_id" ON "messages"("from_user_id");\n'+'select to_user_id,count(to_user_id) from messages indexed by search_messages_by_from_user_id where from_user_id == 2318 group by to_user_id order by count(to_user_id) DESC limit 3;')

#The app needs to send users a summary of their engagement. Find the username of the most popular user, defined as the user who has had the most messages sent to them.
print(cursor.execute('''CREATE INDEX "search_messages_by_to_user_id"
ON "messages"("to_user_id"); ''').fetchall())
print(cursor.execute('''CREATE INDEX "search_username_by_to_user_id" ON "users"("id","to_user_id");''').fetchall())
print(cursor.execute('''select username from users indexed by "search_username_by_to_user_id" where id == (select to_user_id from messages indexed by "search_messages_by_to_user_id" where id == (select to_user_id from messages group by to_user_id order by count(to_user_id) DESC limit 1)); ''').fetchall())
asw(r'E:\SQL\snap\4.sql','CREATE INDEX "search_username_by_to_user_id" ON "users"("id","to_user_id");\n'+'select username from users indexed by "search_username_by_to_user_id" where id == (select to_user_id from messages indexed by "search_messages_by_to_user_id" where id == (select to_user_id from messages group by to_user_id order by count(to_user_id) DESC limit 1)); ')

#For any two users, the app needs to quickly show a list of the friends they have in common. Given two usernames, lovelytrust487 and exceptionalinspiration482, find the user IDs of their mutual friends. A mutual friend is a user that both lovelytrust487 and exceptionalinspiration482 count among their friends.
print(cursor.execute('''select friend_id from friends indexed by "sqlite_autoindex_friends_1" where user_id == (select id from users where username = "lovelytrust487") intersect select friend_id from friends indexed by "sqlite_autoindex_friends_1" where user_id == (select id from users where username ="exceptionalinspiration482"); ''').fetchall())
asw(r'E:\SQL\snap\5.sql','select friend_id from friends indexed by "sqlite_autoindex_friends_1" where user_id == (select id from users where username = "lovelytrust487") intersect select friend_id from friends indexed by "sqlite_autoindex_friends_1" where user_id == (select id from users where username ="exceptionalinspiration482"); ')
