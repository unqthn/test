
import psycopg2 as psql
from urllib.request import Request, urlopen
from lxml import html
from urllib.request import urlopen
import re
import requests
from bs4 import BeautifulSoup
from urllib import request
import pymysql
import sched, time

golf = """host='ec2-174-129-193-169.compute-1.amazonaws.com' dbname='d9nq877dd80g1n' user='izplkvdovqxsdd' password='1648da433b873d2e5fb80eee0070cfc32dd0ef1005daf6928c389f9a7bb49745'"""
conn = psql.connect(golf)
conn.autocommit = True
cursor = conn.cursor()

def cut(ttr):
    return ttr.replace(": ","")

def setdb():

    try:
        cursor.execute('drop table fpo2')
        query = ('create table fpo(id_fpo serial primary key,'
                 'topic text,'
                 'content_topic text,'
                 'doyheadsub text,'
                 'date_topic date,'
                 'feedback text,'
                 'doymaster text,'
                 'feedback_date date,'
                 'id_page text)')
        cursor.execute(query)
    except:
        query_create = ('create table fpo2(id_fpo serial primary key,'
                 'topic text,'
                 'content_topic text,'
                 'doyheadsub text,'
                 'date_topic date,'
                 'feedback text,'
                 'doymaster text,'
                 'feedback_date date,'
                 'id_page text)')
        cursor.execute(query_create)

def del_space_list(item):
    list_ = list(item)
    for e, i in enumerate(list_):
        count = i.count(" ")
        if count >= len(i) * 3 / 5:
            del list_[e]
    return list_

def sum(detaillist):
    tmp = ''
    for i in detaillist:
        tmp += i
    return tmp

# def check_pre_db(text):
#     word1 = r"ลงทุน"
#     word2 = r"ระดมทุน"
#     word3 = r"แชร์ลูกโซ่"
#     teabkum1 = re.findall(word1, text)
#     teabkum2 = re.findall(word2, text)
#     teabkum3 = re.findall(word3, text)
#
#     if (teabkum1 != []):
#         print(teabkum1)
#         return 1
#     elif (teabkum2 != []):
#         print(teabkum2)
#         return 1
#     elif (teabkum3 != []):
#         print(teabkum3)
#         return 1
#     else:
#         return 0

def check_mn(mn):
    if (mn == 'ม.ค.'):
        dmn = '01'
    elif (mn == 'ก.พ.'):
        dmn = '02'
    elif (mn == 'มี.ค.'):
        dmn = '03'
    elif (mn == 'เม.ย.'):
        dmn = '04'
    elif (mn == 'พ.ค.'):
        dmn = '05'
    elif (mn == 'มิ.ย.'):
        dmn = '06'
    elif (mn == 'ก.ค.'):
        dmn = '07'
    elif (mn == 'ส.ค.'):
        dmn = '08'
    elif (mn == 'ก.ย.'):
        dmn = '09'
    elif (mn == 'ต.ค.'):
        dmn = '10'
    elif (mn == 'พ.ย.'):
        dmn = '11'
    elif (mn == 'ธ.ค.'):
        dmn = '12'
    return dmn

def td():
    setdb()
    file = open(r"C:\Users\User\PycharmProjects\LINE-BOT-PHP-Starter\id2.txt")
    num = file.read()
    num = num.split("\n")

    for c in num:

        req = Request('http://www.fpo.go.th/FPO/index2.php?mod=Petition&categoryID=CAT0000079&petitionID='+c+'&file=answer', headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        unicode_str = webpage.decode("utf8")
        tree = html.fromstring(unicode_str)
        headsubject = tree.xpath("//div[contains(@style,'background-color: #ffcc99; width: auto; font-size: 14px; font-weight: 600; padding-left: 5px;')]")
        detailsubject = tree.xpath("//div[@style='background-color: #fff9e8; padding: 5px;']")
        doy = tree.xpath("//table[@class='detail']//table//tr/td[@colspan='2' and @valign='top']/text()")
        detailanssubject = tree.xpath("//div[@style='border: 1px dotted maroon; background-color: #fff9e8; padding: 5px;']//text()")
        doy = del_space_list(doy)
        detailans = sum(detailanssubject)
        page_num = str(c)
        if(detailsubject[0].text!=None):
            a = headsubject[0].text
            b = detailsubject[0].text

            if(len(doy)>2):
                try:
                    c = cut(doy[0])
                    d = cut(doy[1])
                    ggggg = d.split(" ")
                    mn = ggggg[2]
                    dmn =(check_mn(mn))
                    date = str(ggggg[3])+"-"+str(dmn)+"-"+str(ggggg[1])
                    f = cut(doy[2])
                    g = cut(doy[3])
                    feed_date = g.split(" ")
                    #print(feed_date)
                    feed_mn = feed_date[2]
                    feed_dmn = (check_mn(feed_mn))
                    feed_d = str(feed_date[3]+"-"+str(feed_dmn)+"-"+feed_date[1])
                    #print(feed_d)
                    cursor.execute('''INSERT into fpo2(topic,content_topic,doyheadsub,date_topic,feedback,doymaster,feedback_date,id_page)
                                    values (%s,%s,%s,%s,%s,%s,%s,%s)'''
                                    ,(a,b,c,date,detailans,f,feed_d,page_num))
                    print("insert max data")
                except:
                    print("error insert page_num =",page_num)
            else:
                try:
                    c = cut(doy[0])
                    d = cut(doy[1])
                    ggggg = d.split(" ")
                    mn = ggggg[2]
                    dmn =(check_mn(mn))
                    date = str(ggggg[3])+"-"+str(dmn)+"-"+str(ggggg[1])
                    cursor.execute('''INSERT into fpo2(topic,content_topic,doyheadsub,date_topic,id_page)
                                    values (%s,%s,%s,%s,%s)'''
                                   ,(a,b,c,date,page_num))
                    #print(a, b, c, date)
                    #print(date)
                except:
                    print("insert 5 data")


def job():
    td()
    sched.schedule.every().day.at("00:15").do(job)
    while True:
        sched.schedule.run_pending()
    time.sleep(1)
