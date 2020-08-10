# coding:utf8
# 作者： 蓝一潇
import sqlite3
import time

def create():
    db = sqlite3.connect('EVENT.DB')
    c = db.cursor()
    c.execute('''CREATE TABLE EVENT (
ID INTEGER PRIMARY KEY AUTOINCREMENT ,
STATUS INTEGER NOT NULL ,
TIMESTAMPS VARCHAR(15),
PATH VARCHAR(255),
REMARK1 VARCHAR(255),
REMARK2 VARCHAR(255),
REMARK3 VARCHAR(255)
)''')
    db.commit()
    db.close()
    return

def get_last_one():
    db = sqlite3.connect('EVENT.DB')
    c = db.cursor()
    res = c.execute("""SELECT * FROM EVENT ORDER BY ID DESC LIMIT 1""")
    for i in res:
        db.close()
        return {'id': i[0], 'status': i[1], 'timestamp': i[2], 'path': i[3], 'remark1': i[4], 'remark2': i[5], 'remark3': i[6]}
    db.close()
    return {'status': None}

def insert(status, path=None, remark1=None, remark2=None, remark3=None):
    db = sqlite3.connect('EVENT.DB')
    c = db.cursor()
    curr = time.time()
    c.execute("INSERT INTO EVENT (STATUS, TIMESTAMPS, PATH, REMARK1, REMARK2, REMARK3) VALUES (?, ?, ?, ?, ?, ?)", (status, curr, path, remark1, remark2, remark3))
    db.commit()
    db.close()
    return 0

def get_all():
    ret = []
    db = sqlite3.connect('EVENT.DB')
    c = db.cursor()
    res = c.execute("""SELECT * FROM EVENT ORDER BY ID DESC""")
    for i in res:
        ret.append(i)
    db.close()
    return ret

if __name__ == '__main__':

    # create()
    print(get_all())


