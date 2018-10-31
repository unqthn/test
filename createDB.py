
# -*- coding: utf-8 -*-
import psycopg2 as psql

try:
    conn_string = "host='ec2-174-129-193-169.compute-1.amazonaws.com' dbname='d9nq877dd80g1n' user='izplkvdovqxsdd' password='1648da433b873d2e5fb80eee0070cfc32dd0ef1005daf6928c389f9a7bb49745'"
    conn = psql.connect(conn_string)
    conn.autocommit = True
    cursor = conn.cursor()
    print("connect db")
except:
    print('cant connect db')

try:
    db = 'create table sent_mode1_user(user_id text primary key,count_topic text)'
    cursor.execute(db)
    print("create table sent_mode1_user sucsess")
except:
    print("Error create table sent_mode1_user")

try:
    query4 = ('create table user_history_company(id_his_company serial primary key,'
              'user_id_hiscompany  text,'
              'namecompany_his text)')
    cursor.execute(query4)
    print("create table user_history_company sucsess")
except:
    print("error table user_history_company")

try:
    query4 = ('create table user_history_fpo(id_his_fpo serial primary key,'
              'user_id_hisfpo  text,'
              'fpo_his text)')
    cursor.execute(query4)
    print("create table user_history_fpo sucsess")

except:
    print("error table user_history_fpo")

try:
    cursor.execute('drop table topchart_fpo')
    cursor.execute('drop table count_fpo')
    print("drop table sucsess")
except:
    print("No drop table")

try:
    query3 = ('create table topchart_fpo(id_count_fpo serial primary key,'
             'topic_fpo_count text)')
    cursor.execute(query3)

    query4 = ('create table count_fpo(id_topic_name serial primary key,'
              'id_fpo_count int,'
              'date_topicname date)')
    cursor.execute(query4)
    print("create table fpo sucsess")

except:
    print("error table topchart_fpo")
