#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
import json
import sqlite3
from datetime import datetime

# Loading config
CONFIG_FILE=r'config.json'
with open(CONFIG_FILE,'r',encoding='utf-8') as f:
    CONFIG=json.load(f)

paths = r'\\172.29.250.14\DevData1\激光钻机\二厂激光钻机\Q01'

for item in os.scandir(paths):
    if item.is_dir():
        print(item.path)
    
sys.exit(0)

# Sqlite3 datetime adapter
def date_to_str(date):
    return date.strftime('%Y/%m/%d %H:%M:%S')

def str_to_date(str):
    return datetime.strptime(str, '%Y/%m/%d %H:%M:%S')

sqlite3.register_adapter(datetime, date_to_str)



class Database(object):
    def __init__(self,database):
        self.database=database
        self.session=None
        self.cursor=None
        self.datetime={}

    def open(self):
        if os.path.isfile(self.database):
            create_table=False
        else:
            create_table=True
        self.session = sqlite3.connect(self.database)
        self.cursor = self.session.cursor()
        if create_table:
            # self.cursor.execute('''CREATE TABLE sinstatis
            #     (machine text,datetime text, lot text,prg text,cond text);''')
            self.cursor.execute('''CREATE TABLE sinstatis
                (machine text,datetime text);''')
            self.cursor.execute('''CREATE INDEX sinstatis_idx ON sinstatis (machine ASC,datetime DESC);''')
        self.update_datetime()

    def close(self):
        if self.session:
            self.session.close()
            self.session=None
        if self.cursor:
            self.cursor.close()
            self.cursor=None
    
    def insert(self):
        data=[
            ('Q01#','2024/10/01 01:00:01'),
            ('Q01#','2024/10/02 01:00:01'),
            ('Q01#','2024/10/03 01:00:01'),
            ('Q02#','2024/10/06 02:00:01'),
            ('Q02#','2024/10/05 02:00:01'),
            ('Q02#','2024/10/04 02:00:01')
        ]
        self.cursor.executemany("INSERT INTO sinstatis VALUES(?,  ?);", data)

    def update_datetime(self):
        self.datetime={}
        for row in self.session.execute("SELECT machine,MAX(datetime) FROM sinstatis GROUP BY machine;"):
            self.datetime[row[0]]=row[1]



db=Database('test.db')
db.open()
db.insert()
db.update_datetime()
print(db.datetime)
print('D01' in db.datetime)
print('Q01#' in db.datetime)