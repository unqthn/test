
#-*-coding: utf-8 -*-
import time, json
from flask import Flask, request, abort
from random import randint
import psycopg2 as psql
import json
import re
from pythainlp.tokenize import word_tokenize
import sched, time

try:
    from wordcut import Wordcut
    print('workcut import OK!!')
except:
    print('cant import wordcut')

try:
    with open(r'dc - Copy.txt')as dict_file:
        word_list = [w.rstrip() for w in dict_file.readlines()]
        word_list.sort()
    print("dick OK!!")
except:
    print('cant open dict thai')

try:
    conn_string = "host='ec2-174-129-193-169.compute-1.amazonaws.com' dbname='d9nq877dd80g1n' user='izplkvdovqxsdd' password='1648da433b873d2e5fb80eee0070cfc32dd0ef1005daf6928c389f9a7bb49745'"
    conn = psql.connect(conn_string)
    conn.autocommit = True
    cursor = conn.cursor()
    print("connect db")
except:
    print('cant connect db')


app = Flask(__name__)

def warpcut(text):
    wordcut = Wordcut(word_list)
    return wordcut.tokenize(text)

def cutkumkean(str):
    out=[]
    for i in range(0,len(str),1000):
        if i+1000 < len(str):
            tmp_ = ''
            for j in str[i:i+1000]:
                tmp_ += j
            out.append(tmp_)
        else:
            tmp_ = ''
            for j in str[i:]:
                tmp_ += j
            out.append(tmp_)
    return out

def join_text(list_str):
    tmp = ''
    for i in list_str:
        tmp += i+', '
    tmp = list(tmp)
    tmp[-1] = ''
    tmp = ''.join(tmp)
    return tmp

def dataDBocpb():
    try:
        query = ("Select id,company_name From ocpb2;")
        cursor.execute(query)
        data = cursor.fetchall()
        print("Select id,companyname ocpb2 qury")
    except:
        print("not Select id,companyname ocpb2 qury")

    kebkum2 = []
    for c in range(len(data)):
        word = str(data[c][1])
        word = word.replace("('", "")
        word = word.replace("',)", "")
        word = word.replace(" ", "")
        word = word.replace("\\n", "")
        word = word.replace("\\r", "")

        symbol_th = []
        for i in range(3585, 3800):
            cha = chr(i)
            if i >= 3585 and i <= 3642:
                symbol_th.append(cha)
            if i >= 3648 and i <= 3662:
                symbol_th.append(cha)
            if i >= 3664 and i <= 3673:
                symbol_th.append(cha)
        comp = "[" + ''.join(symbol_th) + "]+"
        print("aaaaaaaaaa")
        th = re.findall(comp, word)
        eng = re.findall("""[A-Za-z]+""", word)
        strthai = ""
        kebword = []
        print("bbbbbbbbbbbb")
        for addth in th:
            strthai += addth
        for addEng in eng:
            if (addEng != 'xa'):
                addEng = addEng.lower()
                kebword.append(addEng)
        # kebkum2 = kebkum2+warpcut(strthai)
        print("cccccccccccc")
        kebword = kebword + word_tokenize(strthai, engine='newmm')
        print("ddddddddddddddddddddddd")
        kebkum2.append([data[c][0], kebword])

    #     kebkum2.append([data[c][0], warpcut(word)])
    for cc in kebkum2:
        print(cc)
    return kebkum2

def dataDBfpo():
    try:
        qu = ("Select id_fpo,content_topic From fpo3;")
        cursor.execute(qu)
        data2 = cursor.fetchall()
        print("select content fpo3 qury")
    except:
        print("not select content fpo3 qury")
    kebkum = []
    for c in range(len(data2)):
        word = str(data2[c][1])
        word = word.replace("('", "")
        word = word.replace("',)", "")
        word = word.replace(" ", "")
        word = word.replace("\\n", "")
        word = word.replace("\\r", "")

        symbol_th = []
        for i in range(3585, 3800):
            cha = chr(i)
            if i >= 3585 and i <= 3642:
                symbol_th.append(cha)
            if i >= 3648 and i <= 3662:
                symbol_th.append(cha)
            if i >= 3664 and i <= 3673:
                symbol_th.append(cha)
        comp = "[" + ''.join(symbol_th) + "]+"
        th = re.findall(comp, word)
        eng = re.findall("""[A-Za-z]+""", word)
        strthai = ""
        kebword = []
        for addth in th:
            strthai += addth
        for addEng in eng:
            if(addEng != 'xa'):
                addEng= addEng.lower()
                kebword.append(addEng)
        #kebkum2 = kebkum2+warpcut(strthai)
        kebword = kebword + word_tokenize(strthai, engine='newmm')
        kebkum.append([data2[c][0],kebword])
    for aa in kebkum:
        print(aa)
    return kebkum

def main():
    try:
        dbocpb = dataDBocpb()
        print("ok db ocpb")
    except:
        print("error db ocpb")

    try:
        dbfpo = dataDBfpo()
        print("ok db fpo")
    except:
        print("error db fpo")

    with open('dbfpo'+'.txt', 'w') as db_fpo:
        json.dump(dbfpo, db_fpo)

    with open('dbocpb'+'.txt', 'w') as db_ocpb:
        json.dump(dbocpb, db_ocpb)

    #s.enter(40, 1, main, ())

def job():
    main()
    sched.schedule.every().day.at("00:40").do(job)
    while True:
        sched.schedule.run_pending()
    time.sleep(1)
# s = sched.scheduler(time.time, time.sleep)
# s.enter(40, 1, main, ())
# s.run()