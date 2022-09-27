import re
import configparser
import sqlite3
import twython
import sys
import os

configParser = configparser.RawConfigParser()
configFilePath = r'config.config'
configParser.read(configFilePath)

db_name = configParser.get('db-settings', 'db-name')

# create db file if not already present 
if not os.path.exists(db_name):
    with open(db_name, 'w'):
        pass

# create DB table if not already present
try:
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS "USERDATA" ( `userid` TEXT NOT NULL UNIQUE, `username` TEXT NOT NULL, `last_post_id` TEXT NOT NULL, PRIMARY KEY(`userid`) )')
    conn.commit()
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print('\n**ERROR**\n{0}, {1}, {2}\n{3}\n'.format(exc_type, fname, exc_tb.tb_lineno, str(e)))
finally:
    if(conn):
        conn.close()

# insert new user in database 
def insert_to_userdata(userid, username, last_post_id):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute('INSERT INTO USERDATA (userid, username, last_post_id) VALUES (?, ?, ?)', (userid, username, last_post_id))
        conn.commit()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('\n**ERROR**\n{0}, {1}, {2}\n{3}\n'.format(exc_type, fname, exc_tb.tb_lineno, str(e)))
    finally:
        if(conn):
            conn.close()

# update last_post_id using user name
def update_post_id_in_userdata(username, last_post_id):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute('Update userdata set last_post_id = ? where username = ?', (last_post_id, username))
        conn.commit()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('\n**ERROR**\n{0}, {1}, {2}\n{3}\n'.format(exc_type, fname, exc_tb.tb_lineno, str(e)))
    finally:
        if(conn):
            conn.close()

# delete a row 
def delete_user_from_userdata(username):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute('delete from userdata where username=?', (username,))
        conn.commit()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('\n**ERROR**\n{0}, {1}, {2}\n{3}\n'.format(exc_type, fname, exc_tb.tb_lineno, str(e)))
    finally:
        if(conn):
            conn.close()

# list users and userids
def list_all_users():
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute('select userid, username, last_post_id from userdata')
        output = cur.fetchall()
        conn.commit()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('\n**ERROR**\n{0}, {1}, {2}\n{3}\n'.format(exc_type, fname, exc_tb.tb_lineno, str(e)))
    finally:
        if(conn):
            conn.close()
        return output # returns list of lists [(1,2,3),(4,5,6)]

# update username using userid
def update_username(userid, username):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute('UPDATE USERDATA SET username = ? where userid = ?', (username, userid)) 
        # cur.execute('INSERT INTO USERDATA (userid, username, last_post_id) VALUES (?, ?, ?)', (userid, username, last_post_id))
        # cur.execute('UPDATE mytable SET status = "Online" WHERE name is ?', (data[0], ))
        conn.commit()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('\n**ERROR**\n{0}, {1}, {2}\n{3}\n'.format(exc_type, fname, exc_tb.tb_lineno, str(e)))
    finally:
        if(conn):
            conn.close()
       