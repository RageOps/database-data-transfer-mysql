import mysql.connector
import json

## Connect to the databases

mydb = mysql.connector.connect(
    host='localhost',
    user='',
    password='',
    database='db1',
)
print('db started')

newdb = mysql.connector.connect(
    host='localhost',
    user='',
    password='',
    database='db2',
)
print('2nd db started')

## Select all data from the first db -- mydb

mycursor = mydb.cursor()

mycursor.execute('SELECT * FROM ap_bans')

myresult = mycursor.fetchall()

bansdict = {}

## Define functions that we will need later

def findType(thing, table):
    t = json.loads(table)
    for x in t:
        if x.find(thing) != -1:
            return x
    return None

def returnVals(x):
    return x['id'], x['name'], x['license'], x['discord'], x['ip'], x['reason'], x['expire'], x['bannedby']

## Sort all of the data from the first db query into a table so that we can insert the old data into the newdb with correct formatting

for x in myresult:
    ids = x[3]
    time = json.loads(x[4])
    bansdict[x[0]] = {
        'id': x[0],
        'name': x[1],
        'license': findType('license', ids) or 'n/a',
        'discord': findType('discord', ids) or 'n/a',
        'ip': findType('ip', ids) or 'n/a',
        'reason': x[5],
        'expire': time['timeEnd'],
        'bannedby': x[2],
    }

## Take the old data and insert it into the new database

newcursor = newdb.cursor()

sql = 'INSERT INTO bans (id, name, license, discord, ip, reason, expire, bannedby) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'

for x in bansdict:
    val = (returnVals(bansdict[x]))
    newcursor.execute(sql, val)

newdb.commit()