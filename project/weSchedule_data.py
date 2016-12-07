#!/usr/local/bin/python2.7

'''Kelly Kung and Jason Lan'''
'''CS 304'''
'''weSchedule_data.py'''
'''This python file contains the code that connects to the database and handles it'''

import sys
import MySQLdb
import dbconn2
from datetime import datetime
from dateutil.relativedelta import relativedelta

#we get the connection into the database with this function
def getConn():
    dsn = dbconn2.read_cnf('/students/zlan/.my.cnf')
    dsn['db'] = 'zlan_db'
    return dbconn2.connect(dsn)

conn = getConn()

def getUserData(name):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    data = (name,)
    curs.execute('SELECT * from users WHERE user_name = LOWER(%s)', data)
    user = curs.fetchone()
    return user

def insertUser(name, isCreator):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    data = (name,isCreator, )
    curs.execute('INSERT INTO users (user_name, isCreator) VALUES (%s, %s)', data)

def insertEvent(eventName, start, end, creatorName):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    data = (eventName, start, end, creatorName)
    curs.execute('INSERT INTO events (event_name, startDate, endDate, UID) VALUES (%s, %s, %s, (SELECT UID FROM users WHERE user_name = %s))', data)

def register(username, password):
    if isUserExist(username) == -1:
        return -1
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    data = (username, password)
    curs.execute('INSERT INTO account (username, password) VALUES (%s, %s)', data)

def isUserExist(username):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    data = (username,)
    curs.execute('SELECT * from account WHERE username = %s', data)
    user = curs.fetchone()
    if user != None:
        return -1
    return 1

def login(username, password):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    data = (username,)
    curs.execute('SELECT * from account WHERE username = %s', data)
    user = curs.fetchone()
    if user == None:
        return -1 
    elif user['password'] == password:
        return user
    else:
        return -2


def getEvent(eventName, organizerName):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    data = (eventName,organizerName,)
    curs.execute('SELECT * FROM events WHERE event_name = %s and UID = (SELECT UID FROM users WHERE user_name = %s)', data)
    eventID = curs.fetchone()
    return eventID

def convertDate(time, format):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    data = (time,format, )
    curs.execute('SELECT str_to_date(%s, %s) as date', data)
    date = curs.fetchone()
    return date['date']

def insertAvailability(event_name, organizer_name, date):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    data = (organizer_name, event_name,organizer_name, date, )
    
    curs.execute('INSERT INTO availability (UID, eventID, availability) VALUES ((SELECT UID FROM users WHERE user_name = %s), (SELECT eventID FROM events WHERE event_name = %s and UID = (SELECT UID FROM users WHERE user_name = %s)), %s)', data)

def getEventName(eventID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    data = (eventID,)
    curs.execute('SELECT event_name FROM events WHERE eventID = %s', data)
    return curs.fetchone()

def getUserName(UID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    data = (UID, )
    curs.execute('SELECT user_name FROM users WHERE UID = %s', data)
    return curs.fetchone()

def getDates(eventID, UID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    data = (eventID, UID,)
    curs.execute('SELECT availability FROM availability WHERE eventID = %s and UID = %s', data)
    return curs.fetchall()
