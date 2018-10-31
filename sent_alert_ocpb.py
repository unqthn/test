
# -*- coding: utf-8 -*-
import psycopg2 as psql
import json
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
import sched, time
from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate,  URITemplateAction,
    PostbackTemplateAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent
)

try:
    conn_string = "host='ec2-174-129-193-169.compute-1.amazonaws.com' dbname='d9nq877dd80g1n' user='izplkvdovqxsdd' password='1648da433b873d2e5fb80eee0070cfc32dd0ef1005daf6928c389f9a7bb49745'"
    conn = psql.connect(conn_string)
    conn.autocommit = True
    cursor = conn.cursor()
    print("connect db")
except:
    print('cant connect db')

app = Flask(__name__)

line_bot_api = LineBotApi('Pdt/ED1rOmznxrHueW+DLuKS/7jbqjwR+mU/vUyRBNxxmcmF+MD3omp03ROculxF2ziMKLIo5BwRWT9dwSKMMzApjKgPQCrVuF5yWkwcy9YL6B0Q4Turo9l8ydmbU59GNPT/8c16RspQQ31i4X1V/gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0802071f6bf26e330f0c61b392b0a5e2')

def main():
    db_last = open('dbocpb_last.txt', 'r')
    db_present = open('dbocpb_new.txt', 'r')
    data_past = json.load(db_last)
    data_future = json.load(db_present)

    cursor.execute('''select (user_id_hiscompany,namecompany_his) from user_history_company''')
    q = cursor.fetchall()
    data_user = []

    for c in q:
        c = str(c)
        data_user.append(c.split(","))

    spit = []

    try:
        for k in range(len(data_future)):
            teab = q
            if data_future[k] not in data_past:
                print("data_future[k] =",data_future[k])
                print(" not in data_past")
                tmp = str(data_future[k])
                spit.append(tmp.split(","))

        print("len spit =")
    except:
        print("zero teab kum")

    # for a in range(len(spit)):
    #     print("spit[a][0]spit[a][1] =",spit[a])
    #     print("spit tee dai ",spit[a][0],"--",spit[a][1])

    # try:
    #     for keb in range(len(spit)):
    #         bbbbbb = 0
    #         try:
    #             cursor.execute('''insert into ocpb2 (company_name,project_name)values (%s,%s)''', (spit[keb][0], spit[keb][1]))
    #             print("insert ok")
    #         except:
    #             print("error insert")
    #
    #
    #         # c = open('dbocpb_last.txt', 'r')
    #         # d = json.load(c)
    #         # c.close()
    #         # d = list(d)
    #         # aaa = spit[keb]
    #         # print(aaa)
    #         # d.append(aaa)
    #         # with open('dbocpb_last.txt', 'w') as db_ocpb:
    #         #      json.dump(d, db_ocpb)
    #     print("insert new data into ocpb2")
    # except:
    #     print("error insert new data into ocpb2")



    try:
        data_usernew = []
        for i in range(len(data_user)):
            print("a =",data_user[i][0]," ---------- ",data_user[i][1])
            data_user[i][0] = data_user[i][0].replace("('(", "")
            data_user[i][0] = data_user[i][0].replace("[", "")
            data_user[i][0] = data_user[i][0].replace("'", "")
            data_user[i][0] = data_user[i][0].replace("('(", "")
            data_user[i][1] = data_user[i][1].replace('"', "")
            data_user[i][1] = data_user[i][1].replace(")'", "")

            print("a =", data_user[i][0], " ---------- ", data_user[i][1])

            for keb in range(len(spit)):

                data_user[i][0] = data_user[i][0].replace("('(", "")
                data_user[i][0] = data_user[i][0].replace("'", "")

                data_user[i][1] = data_user[i][1].replace(")'", "")
                data_user[i][1] = data_user[i][1].replace("')", "")
                data_user[i][1] = data_user[i][1].replace('"', "")
                data_user[i][1] = data_user[i][1].replace(")'", "")

                teabkum11 = (data_user[i][1] in spit[keb][0])

                # print("user id = " + data_user[i][0])
                # print("company_name = " + data_user[i][1])

                if (teabkum11 == True):
                    print("data_user[i][1] = ", data_user[i][1])
                    print("spit[keb][0] = ", spit[keb][0])
                    print("yes")
                    # print("teamkum 11")
                    if(str(data_user[i][0]) == 'U93a07feadb4384226d2b88cf9a91c307' or str(data_user[i][0]) == 'Ud4720cf00f8a836c2e200eae75cd8fab'):
                        line_bot_api.push_message(
                            data_user[i][0],
                            TextSendMessage(
                                text=str(spit[keb][0]) + " " + str(
                                    spit[keb][1]) + "\n ถูกคณะกรรมการคุ้มครองผู้บริโภค มีมติให้ดำเนินคดี"))

                        print('sent 1')

                else:
                    print("sent 0")
        print("in if sent")
    except:
        print("no sent")

def job():
    main()
    sched.schedule.every().day.at("01:00").do(job)
    while True:
        sched.schedule.run_pending()
    time.sleep(1)



