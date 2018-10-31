
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

line_bot_api = LineBotApi(
    'Pdt/ED1rOmznxrHueW+DLuKS/7jbqjwR+mU/vUyRBNxxmcmF+MD3omp03ROculxF2ziMKLIo5BwRWT9dwSKMMzApjKgPQCrVuF5yWkwcy9YL6B0Q4Turo9l8ydmbU59GNPT/8c16RspQQ31i4X1V/gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0802071f6bf26e330f0c61b392b0a5e2')

db_last = open('dbfpo_last.txt', 'r')
db_present = open('dbfpo_new.txt', 'r')
a = json.load(db_last)
c = json.load(db_present)

def loop_send(text_list,user_id):
    for c in text_list:
        line_bot_api.push_message(
            user_id,
            TextSendMessage(text=str(c)))

def sent(u_id, head_contect):
    line_bot_api.push_message(u_id, TextSendMessage(text=head_contect[0]))
    loop_send(head_contect[1], u_id)
    loop_send([head_contect[2]], u_id)
    # loop_send(head_contect[3], u_id)
    # loop_send([head_contect[4]], u_id)
    try:
        loop_send(head_contect[3], u_id)
    except:
        pass

    try:
        loop_send([head_contect[4]], u_id)
    except:
        pass

def se(mode,me):
    se = []
    num = 1
    for c in me:
        o = CarouselColumn(
            title='หัวข้อร้องเรียน :', text=str(c[0]),
            actions=[
                PostbackTemplateAction(
                    label='ดูข้อมูลทั้งหมด',
                    data=str(mode)+'_'+str(num)
                )
            ]
        )
        num+=1
        se.append(o)
    return se

def cutkumkean(str):
    # tmp = str.split("\n")
    # for c in len(str):
    #     tm
    #tmp = str
    # print(tmp)
    out=[]
    for i in range(0,len(str),1000):
        if i+1000 < len(str):
            tmp_ = ''
            # out.append(''.join(tmp[i:i+3]))
            # print(out[0])
            for j in str[i:i+1000]:
                tmp_ += j
            out.append(tmp_)


        else:
            tmp_ = ''
            # out.append(''.join(tmp[i:i+3]))
            # print(out[0])
            for j in str[i:]:
                tmp_ += j
            out.append(tmp_)
            # for j in tmp[i:]:
            #     print(j)
    return out

def cut(ttr):
    return ttr.replace(": ","")

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

def forSent_Template(listOfTemp, user_id):
    d = listOfTemp

    if (len(d) == 0):
        line_bot_api.push_message(
            user_id,
            TextSendMessage(text="ไม่พบการกระทำผิดเกี่ยวกับข้อมูลที่ท่านได้สอบถาม")
        )

    elif (len(d) > 5):
        for c in range(0, len(d) + 1, 5):
            if (c + 5 < len(d)):

                carousel_template_message = TemplateSendMessage(
                    alt_text='Carousel template',
                    template=CarouselTemplate(
                        columns=d[c:c + 5]
                    )
                )
                line_bot_api.push_message(user_id, carousel_template_message)
            else:

                carousel_template_message = TemplateSendMessage(
                    alt_text='Carousel template',
                    template=CarouselTemplate(
                        columns=d[c:]
                    )
                )
                line_bot_api.push_message(user_id, carousel_template_message)


    else:
        carousel_template_message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=d
            )
        )
        line_bot_api.push_message(user_id, carousel_template_message)



def creTemplate(mode,listOfata):
    out_tem = []
    i =1
    for c in listOfata:
        #line_bot_api.push_message(uId, TextSendMessage(text='Hello round:' + str(i) + '/' + str(len(me)+1)))
        i += 1
        tmpHead = str(c[0])[:40] + '...'
        try:
            index_db = str(c[5])
        except:
            index_db = str(c[3])

        # print(type(tmpHead), len(tmpHead), tmpHead)
        print('index',index_db)
        o = CarouselColumn(title=' ', text=str(tmpHead),
                           actions=[PostbackTemplateAction(label='ดูข้อมูลทั้งหมด', data=str(mode) + '_' + index_db)])
        out_tem.append(o)
    return out_tem

def main():
    db_last = open('dbfpo_last.txt', 'r')
    db_present = open('dbfpo_new.txt', 'r')
    data_past = json.load(db_last)
    data_future = json.load(db_present)

    spit = []
    data_new_id = []
    try:
        for k in range(len(data_future)):
            check_data = False
            for num in data_past:

            #if data_future[k][1] not in data_past:
                #print("str(data_future[k][1] =",str(data_future[k][1]))
                #print("str(num) =",str(num))
                teabkum11 = (str(data_future[k][1]) in str(num))
                #if(str(data_future[k][1])==str(num)):
                if(teabkum11==True):
                    print("ok teabkum11==True")
                    #tmp = data_future[k][1]
                    data_new_id.append(data_future[k][0])#ไID new use sent messege
                    #print("tmp = ",tmp)
                    #spit.append(data_future[k])
                    #-------------------------------
        # for cc in data_new_id:
        #     #cc = cc.replace("(","")
        #     print(cc)


    except:
        print("zero teab kum")

    # for bb in data_new_id:
    #     print("bb =",bb)
    query = ("Select id_fpo,topic,content_topic,doyheadsub,date_topic,feedback,doymaster,feedback_date From fpo2 ")
    cursor.execute(query)
    data = cursor.fetchall()

    data_num_insert = []
    for k in range(len(data_future)):
        if data_future[k][0] not in data_new_id:
        #for bb in data_new_id:
            print("data_future[k][0] =", data_future[k][0])
            data_num_insert.append(data_future[k][0])


    # for a in range(len(data)):
    #     print(data[a][0])

    # for ab in range(len(data)):
    #     data1 = str(data[ab][0])
    for num in range(len(data)):
        for ab in data_num_insert:
            #test_data = False
            ab = int(ab)
            #------------------------------------------------------
            if(int(ab) == int(data[num][0])):

                print("data[num][0] =", data[num][0])
                print("ab =", ab)
                #print("data[ab][4] = ",data[ab][4])
                try:
                    d = cut(data[ab][4])
                    ggggg = d.split(" ")
                    mn = ggggg[2]
                    dmn = (check_mn(mn))
                    date = str(ggggg[3]) + "-" + str(dmn) + "-" + str(ggggg[1])
                except:
                    print("erere")
                try:
                    if(data[ab][5] != None):
                        qwe = cut(data[ab][7])
                        feedback_date = qwe
                        spitfeedbackdate = feedback_date.split(" ")
                        feedback_mn = spitfeedbackdate[2]
                        feedback_dmn = check_mn(feedback_mn)
                        date_feedback = str(spitfeedbackdate[3]) + "-" + str(feedback_dmn) + "-" + str(spitfeedbackdate[1])
                        #print(date_feedback)
                        try:
                            # cursor.execute('''insert into fpo3(topic,content_topic,doyheadsub,date_topic,feedback,doymaster,feedback_date) values (%s,%s,%s,%s,%s,%s,%s)'''
                            #            , (data[ab][1],data[ab][2],data[ab][3],date,data[ab][5],data[ab][6],date_feedback))
                            print("insert into fpo3 fulldata")
                        except:
                            print("no insert into fpo3 fulldata")
                    else:
                        try:
                            # cursor.execute('''insert into fpo3 (topic,content_topic,doyheadsub,date_topic) values (%s,%s,%s,%s) '''
                            #                ,(data[ab][1],data[ab][2],data[ab][3],date))
                            print("insert in fpo3 partdata")
                        except:
                            print("no insert in fpo3 partdata")
                except:
                    print("no in")
                    #print((data[ab][1],data[ab][2],data[ab][3],data[ab][4],data[ab][5],data[ab][6],data[ab][7] ))

                    #continue
    #-------------------------------------- error
    cursor.execute('''select (user_id_hisfpo,fpo_his) from user_history_fpo''')
    q = cursor.fetchall()
    print("len q ",len(q))
    data_user = []
    head_contect = []
    for c in q:
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
        print("word ",word)
        data_user.append(word.split(","))

    for index in data_num_insert:

        q = ("Select topic,content_topic,doyheadsub,date_topic,feedback,doymaster,feedback_date From fpo2 where id_fpo=" + str(index) + ";")
        cursor.execute(q)
        datafpo = cursor.fetchall()[0]
        # print(index,'\t')
        # print(type(data_fpo),type(data_fpo[0]))
        # print(data_fpo)
        # print(data_fpo[0])
        # print("ssssssssssssssssssssssssssssssssssssssssss")
        # print(data_fpo[1])
        head_contect = []
        try:
            topic = datafpo[0][:100]
            #print("topic =",topic)
            #print(str(datafpo[1]))
            t = cutkumkean(datafpo[1])[:4]
            t3 = "วันที่ร้องเรียน :" + str(datafpo[3])
            t4 = cutkumkean(str("ตอบข้อร้องเรียน :" + datafpo[4]))
            t6 = "วันที่ตอบข้อร้องเรียน :" + str(datafpo[6])
            head_contect.append([topic, t, t3, t4, t6, index])
            # print("head_contect topic - index")
            print("aaa 1")
        except:
            topic = datafpo[0][:100]
            t = cutkumkean(datafpo[1])
            t3 = "วันที่ร้องเรียน :" + str(datafpo[3])
            head_contect.append([topic, t, t3, index])
            print("aaa 2")

        for ba in data_user:
            try:
                #print("str(ba[1]) ",str(ba[1]))
                #print("str(t) ",str(t))
                teabkum11 = (str(ba[1]) in str(t))
                if(teabkum11 == True):
                    print("str(ba[1]) ",str(ba[1]))
                    print("str(t) ",str(t))
                    if (str(ba[0]) == 'U93a07feadb4384226d2b88cf9a91c307' or str(ba[0]) == 'Ud4720cf00f8a836c2e200eae75cd8fab'):
                        print("if sent")
                        print(" T ",t)
                        temp = creTemplate(9, head_contect)
                        forSent_Template(temp, ba[0])
            except:
                pass

def job():
    main()
    sched.schedule.every().day.at("01:00").do(job)
    while True:
        sched.schedule.run_pending()
    time.sleep(1)





