#!/usr/bin/python
#-*-coding: utf-8 -*-
import psycopg2 as psql
from lxml import html
from urllib.request import urlopen
import re
import requests
from bs4 import BeautifulSoup
from urllib import request
import pymysql
import sched, time

conn_string = "host='ec2-174-129-193-169.compute-1.amazonaws.com' dbname='d9nq877dd80g1n' user='izplkvdovqxsdd' password='1648da433b873d2e5fb80eee0070cfc32dd0ef1005daf6928c389f9a7bb49745'"
conn = psql.connect(conn_string)
conn.autocommit = True
cursor = conn.cursor()

try:
    cursor.execute('drop table ocpb')
    cursor.execute('create table ocpb(id serial primary key,company_name varchar(250),project_name varchar(250))')
    print("drop sucsess")
except:
    cursor.execute('create table ocpb(id serial primary key,company_name varchar(250),project_name varchar(250))')
    #print("create")


def trade_spider(max_pages):
    page = 0

    while page <= max_pages:
        #url = 'http://www.ocpb.go.th/more_news.php?offset=0&cid=24&filename=index'
        url = "http://www.ocpb.go.th/more_news.php?offset=" + str(page) + "&cid=24&filename=index"
        html_ = urlopen(url).read()
        unicode_str = html_.decode("cp874")
        #encoded_str = unicode_str.encode("utf8")
        tree = html.fromstring(unicode_str) #เก็บค่าเอาไว้ในรูปแบบ html


        q = tree.xpath("//span[@class='text_head']/text()") #เติม text() เข้าไปเพื่อดึงข้อความ
        #q = tree.xpath("//a[@class='text_head']/text()")
        count = 0
        for c in q:
            count+=1

            if count%2!=0:
                #a=c.encode("utf8")
                a=c
                #print(c)

            if(count%2==0):
                #b=c.encode("utf8")
                b=c
                #print(c)
                tmp = str(a) + "','" + str(b)
                cursor.execute  ("INSERT into ocpb(company_name,project_name)values('"+tmp+"')")
                print(tmp)
                #conn.autocomm(True)
                conn.commit()

        page+=20
    cursor.close()
trade_spider(1000)

def job():
    trade_spider()
    sched.schedule.every().day.at("00:15").do(job)
    while True:
        sched.schedule.run_pending()
    time.sleep(1)


