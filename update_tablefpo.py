
# -*- coding: utf-8 -*-
import json
import psycopg2 as psql
from datetime import date, datetime
import sched, time
try:
    conn_string = "host='ec2-174-129-193-169.compute-1.amazonaws.com' dbname='d9nq877dd80g1n' user='izplkvdovqxsdd' password='1648da433b873d2e5fb80eee0070cfc32dd0ef1005daf6928c389f9a7bb49745'"
    conn = psql.connect(conn_string)
    conn.autocommit = True
    cursor = conn.cursor()
    print("connect db")
except:
    print('cant connect db')

today = date.today()

def dataDB_fpo_past():
    try:
        query = ("Select content_topic From fpo3;")
        #fpo2  is true
        cursor.execute(query)
        data = cursor.fetchall()
        kebkum2 = []
        for c in data:
            word = str(c)
            word = word.replace("(", "")
            word = word.replace(")", "")
            word = word.replace("'(", "")
            word = word.replace("('", "")
            word = word.replace("',)", "")
            word = word.replace(" ", "")
            word = word.replace("'", "")
            word = word.replace("')", "")
            word = word.replace("\\r", "")
            word = word.replace("\\n", "")
            kebkum2.append(word)
        return kebkum2
        print("Select content_topic From fpo3")
    except:
        print("not Select content_topic From fpo3")



def dataDB_fpo_present():
    try:
        query = ("Select id_fpo,content_topic From fpo2;")
        cursor.execute(query)
        data = cursor.fetchall()
        print("Select content_topic From fpo2")
    except:
        print("not Select content_topic From fpo2")

    kebkum2 = []
    for c in data:
        word = str(c)
        word = word.replace("(", "")
        word = word.replace(")", "")
        word = word.replace("'(", "")
        word = word.replace("('", "")
        word = word.replace("',)", "")
        word = word.replace(" ", "")
        word = word.replace("'","")
        word = word.replace("')", "")
        word = word.replace("\\r", "")
        word = word.replace("\\n", "")
        word = word.split(",")

        kebkum2.append(word)
    return kebkum2
def main():
    try:
        db_fpo_past = dataDB_fpo_past()
        print("ok db fpo_past")
    except:
        print("error db fpo_past")

    try:
        db_fpo_future = dataDB_fpo_present()
        print("ok db fpo_new")
    except:
        print("error fpo_new")

    with open('dbfpo_last' + '.txt', 'w') as db_fpo:
        json.dump(db_fpo_past, db_fpo)

    with open('dbfpo_new' + '.txt', 'w') as db_fpo:
        json.dump(db_fpo_future, db_fpo)

def job():
    main()
    sched.schedule.every().day.at("00:30").do(job)
    while True:
        sched.schedule.run_pending()
    time.sleep(1)









