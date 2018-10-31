
# -*- coding: utf-8 -*-
import psycopg2 as psql
from flask import Flask, request, abort
from random import randint
import json
import psycopg2 as psql
import sched, time
from lxml import html
from urllib.request import urlopen
from datetime import date, datetime
try:
    conn_string = "host='ec2-174-129-193-169.compute-1.amazonaws.com' dbname='d9nq877dd80g1n' user='izplkvdovqxsdd' password='1648da433b873d2e5fb80eee0070cfc32dd0ef1005daf6928c389f9a7bb49745'"
    conn = psql.connect(conn_string)
    conn.autocommit = True
    cursor = conn.cursor()
    print("connect db")
except:
    print('cant connect db')

today = date.today()

def dataDB1():
    try:
        query = ("Select company_name,project_name From ocpb2;")
        cursor.execute(query)
        data = cursor.fetchall()
        print("Select companyname,project_name ocpb2 qury")
    except:
        print("not Select companyname,project_name ocpb2 qury")

    kebkum2 = []
    for c in data:
        word = str(c)
        word = word.replace("('", "")
        word = word.replace("')", "")
        word = word.replace("',)", "")
        word = word.replace(" ", "")
        word = word.replace("'", "")
        kebkum2.append(word)
    return kebkum2

def dataDB():
    try:
        query = ("Select company_name,project_name From ocpb_new;")
        cursor.execute(query)
        data = cursor.fetchall()
        print("Select companyname,project_name ocpb_new qury")
    except:
        print("not Select companyname,project_name ocpb_new qury")

    kebkum2 = []
    for c in data:
        word = str(c)
        word = word.replace("('", "")
        word = word.replace("')", "")
        word = word.replace("',)", "")
        word = word.replace(" ", "")
        word = word.replace("'", "")
        kebkum2.append(word)
    return kebkum2
def main():
    try:
        db1 = dataDB1()
        print("ok db ocpb")
    except:
        print("error db ocpb")

    try:
        db = dataDB()
        print("ok db ocpb")
    except:
        print("error db ocpb")

    with open('dbocpb_last' + '.txt', 'w') as db_ocpb:
        json.dump(db1, db_ocpb)

    with open('dbocpb_new' + '.txt', 'w') as db_ocpb:
        json.dump(db, db_ocpb)
    # s.enter(86400, 1, main, ())
def job():
    main()
    sched.schedule.every().day.at("00:30").do(job)
    while True:
        sched.schedule.run_pending()
    time.sleep(1)
# s = sched.scheduler(time.time, time.sleep)
# s.enter(86400, 1, main, ())
# s.run()















