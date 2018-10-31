
#-*-coding: utf-8 -*-
import time, json
import re
from flask import Flask, request, abort
from random import randint
from pythainlp.tokenize import word_tokenize
import psycopg2 as psql
import json
from operator import eq

from datetime import date, datetime

from linebot import (
    LineBotApi, WebhookHandler
)

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

d = open('dbfpo.txt', 'r')
c = open('dbocpb.txt', 'r')
aa = json.load(c)
b = json.load(d)

try:
    from wordcut import Wordcut
    print('workcut import OK!!')
except:
    print('cant import wordcut')

try:
    with open(r'dc.txt')as dict_file:
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

line_bot_api = LineBotApi('Pdt/ED1rOmznxrHueW+DLuKS/7jbqjwR+mU/vUyRBNxxmcmF+MD3omp03ROculxF2ziMKLIo5BwRWT9dwSKMMzApjKgPQCrVuF5yWkwcy9YL6B0Q4Turo9l8ydmbU59GNPT/8c16RspQQ31i4X1V/gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0802071f6bf26e330f0c61b392b0a5e2')

mode = 0
#
# confirm_template_message = TemplateSendMessage(
#             alt_text='Confirm template',
#             template=ConfirmTemplate(
#                 text='Are you sure?',
#                 actions=[PostbackTemplateAction(label='postback', text='postback text',data='action=buy&itemid=1'),
#                     MessageTemplateAction(label='message', text='message text')]))
def createbutton(mode):
    headTitle = ["ค้นหาข้อมูล", "ข้อมูลที่น่าสนใจ", "รับข้อมูลแจ้งเตือน", "ยกเลิกการแจ้งเตือน"]
    subTitle2 = ["เรื่องร้องเรียน", "บริษัทถูกดำเนินคดี"]
    subTitle4 = ["เรื่องร้องเรียน", "บริษัทถูกดำเนินคดี"]
    subTitle6 = ["เรื่องร้องเรียน", "บริษัทถูกดำเนินคดี"]
    subTitle8 = ["เรื่องร้องเรียน", "บริษัทถูกดำเนินคดี"]

    if mode == 0:
        tmp = []

        for i, text in enumerate(headTitle):
            text = text[:20]
            index = i+1
            print(text)
            post_tmp = PostbackTemplateAction(
                label=str(text),
                data= str(index) + "_sentBtm"
            )
            tmp.append(post_tmp)
        for i in tmp:

            print(i)
        ButtonConfrim = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title=' ', text='กรุณาเลือกรายการที่ต้องการ',
                actions=tmp
            )
        )
        return ButtonConfrim

    if mode == 1:
        tmp = []
        index = 1
        for i, text in enumerate(subTitle2):
            text = text[:20]
            ob = str(index) + "_setMode"
            print(text)
            post_tmp = PostbackTemplateAction(
                label=str(text),

                data=ob
            )
            tmp.append(post_tmp)
            index = index + 1
        for i in tmp:
            print(i)
        ButtonConfrim = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title=' ', text='ค้นหาข้อมูล',
                actions=tmp
            )
        )
        return ButtonConfrim

    if mode == 2:
        tmp = []
        index = 3
        for i, text in enumerate(subTitle4):
            text = text[:20]
            ob = str(index)+"_setMode"
            print(text)
            post_tmp = PostbackTemplateAction(
                label=str(text),

                data=ob
            )
            index = index + 1
            tmp.append(post_tmp)
        for i in tmp:
            print(i)
        ButtonConfrim = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title=' ', text='ข้อมูลที่น่าสนใจ',
                actions=tmp
            )
        )
        return ButtonConfrim
    if mode == 3:
        tmp = []
        index = 5
        for i, text in enumerate(subTitle6):
            text = text[:20]
            ob = str(index) + "_setMode"
            print(text)
            post_tmp = PostbackTemplateAction(
                label=str(text),

                data=ob
            )
            index = index + 1
            tmp.append(post_tmp)
        for i in tmp:
            print(i)
        ButtonConfrim = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title=' ', text='รับข้อมูลแจ้งเตือน',
                actions=tmp
            )
        )
        return ButtonConfrim
    if mode == 4:
        tmp = []
        index = 7
        for i, text in enumerate(subTitle8):
            text = text[:20]
            ob = str(index) + "_setMode"
            print(text)
            post_tmp = PostbackTemplateAction(
                label=str(text),
                data=ob
            )
            index = index + 1
            tmp.append(post_tmp)
        for i in tmp:
            print(i)
        ButtonConfrim = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title=' ', text='ยกเลิกการแจ้งเตือน',
                actions=tmp
            )
        )
        return ButtonConfrim





# def warpcut(text):
#     wordcut = Wordcut(word_list)
#     return wordcut.tokenize(text)
def mergStr(list_str):
    tmp_list = list_str
    tmp_out = []
    tmp_str = ''
    for i, data in enumerate(tmp_list):
        # print(data)
        t_ = tmp_str + data
        print(i, len(t_), t_)
        if len(t_) < 1500:
            tmp_str = t_
        if len(t_) > 1500 or i == len(tmp_list)-1:
            tmp_out.append(tmp_str)
            tmp_str = data

    return tmp_out


def cutkumkean(tmp_str):
    tmp_str = word_tokenize(tmp_str, engine='newmm')
    print('len_Bcut:', len(tmp_str))
    return mergStr(tmp_str)

def join_text(list_str):
    tmp = ''
    for i in list_str:
        tmp += i+', '
    tmp = list(tmp)
    tmp[-1] = ''
    tmp = ''.join(tmp)
    return tmp

def check(inputword):
    strth = ""
    input2 = []
    checkid = {}
    for i in range(ord('ก'), ord('๙')):
        strth += chr(i)

    thai = re.findall("[" + strth + "]+", inputword)
    eng = re.findall("[A-Za-z0-9]+", inputword)

    thai = str(thai)
    thai = thai.replace(" ", "")
    thai = thai.replace("[", "")
    thai = thai.replace("]", "")
    thai = thai.replace("'", "")
    thai = thai.replace(",", "")
    if(len(eng)>=0):
        input2.append(eng)
        #print("input2.append(eng) =",input2)
        kebidcount = []
        for nn in input2[0]:
            #print("nn = ",nn)
            try:
                query = ("Select id From ocpb2 where company_name LIKE '%" + nn + "%'")
                cursor.execute(query)
                data = cursor.fetchall()
                #print("ccccc")
                #print("data",data)
                for a in data:
                    i = str(a)
                    i = i.replace("(", "")
                    i = i.replace(",)", "")
                    i = int(i)
                    print("i =",i)
                    #print("data[i] =",data[i])
                    try:
                        checkid[i] = checkid[i] + 1
                    except:
                        checkid[i] = 1

            except:
                print("error")
        print("check id eng =", checkid)
        # for num in data[1]:
        #     print(num)
    input3 = []
    if(len(thai)>=1):
        #input2.append(eng + warpcut(thai))
        input3.append(word_tokenize(thai, engine='newmm'))
        print("input2.append(eng + warpcut(thai)) =" ,input3)
    #print("input 2 = ",input2)

        feq = []
        for i,e in enumerate(aa):
            count = 0
            for j in input3[0]:
                if j in aa[i][1]:
                    try:
                        checkid[aa[i][0]] = checkid[aa[i][0]] + 1
                    except:
                        checkid[aa[i][0]] = 1
                    #count += 1
        print("check id thai =",checkid)
            # try:
            #     if (count >= len(input2[0])):
            #         feq.append([aa[i][0], count])
            #         # print("if(count>=len(input2[0])):")
            # except:

            # if (count != 0):
            #         feq.append([aa[i][0], count])

                # print("if(count!=0):")
    #tmp = sorted(feq, key=lambda student: student[1], reverse=True)[:5]
    #tmp = sorted(feq, key=lambda student: student[1], reverse=True)
    tmp = sorted(checkid, key=checkid.__getitem__, reverse=True)
    return tmp

def remove_space(textList):
    tmp = textList
    while ' ' in textList:
        tmp.remove(' ')
    return tmp

def checkfpo(inputtext):
    strth = ""
    input2 = []
    checkid = {}
    for i in range(ord('ก'), ord('๙')):
        strth += chr(i)

    thai = re.findall("[" + strth + "]+", inputtext)
    eng = re.findall("[A-Za-z0-9]+", inputtext)

    thai = str(thai)
    thai = thai.replace(" ", "")
    thai = thai.replace("[", "")
    thai = thai.replace("]", "")
    thai = thai.replace("'", "")
    thai = thai.replace(",", "")
    if (len(eng) >= 0):
        input2.append(eng)
        print("input2.append(eng) =", input2)
        kebidcount = []
        for nn in input2[0]:

            try:
                query = ("Select id_fpo From fpo3 where content_topic LIKE '%" + nn + "%'")
                cursor.execute(query)
                data = cursor.fetchall()
                for a in data:
                    i = str(a)
                    i = i.replace("(", "")
                    i = i.replace(",)", "")
                    i = int(i)
                    print("i =", i)
                    # print("data[i] =",data[i])
                    try:
                        checkid[i] = checkid[i] + 1
                    except:
                        checkid[i] = 1

            except:
                print("error")
        print("check id eng =", checkid)
        # for num in data[1]:
        #     print(num)
    input3 = []
    if (len(thai) >= 1):
        # input2.append(eng + warpcut(thai))
        input3.append(word_tokenize(thai, engine='newmm'))
        print("input2.append(eng + warpcut(thai)) =", input3)
        # print("input 2 = ",input2)

        feq = []
        for i, e in enumerate(b):
            count = 0
            for j in input3[0]:
                if j in b[i][1]:
                    try:
                        checkid[b[i][0]] = checkid[b[i][0]] + 1
                    except:
                        checkid[b[i][0]] = 1

        print("check id thai =", checkid)
    #----------------------------------------------
    # inputtext = inputtext.replace(" ","")
    # inputword = word_tokenize(inputtext, engine='newmm')
    # #inputword = warpcut(inputtext)
    # print("inputword ",inputword)
    # # for ii in inputword:
    # #     print("ii =",ii)
    # inputword = remove_space(inputword)
    # print("inputword remove",inputword)
    # feq = []
    # for i, e in enumerate(b):
    #     count = 0
    #     for j in inputword:
    #         if j in b[i][1]:
    #             count += 1
    # ----------------------------------------------
        # if(count>=len(inputword)):
        #     print("b[i][0] =",b[i][0])
        #     feq.append([b[i][0], count])
        #     print("if(count>=len(input2[0])):")
        #
        # elif(count!=0):
        #     feq.append([b[i][0], count])


        # if(len(inputword)<=2):
        #     print("len(inputword)<=2")
        #     if(count!=0):
        #         feq.append([b[i][0], count])
        # elif (count >= len(inputword)-1):
        #     print("count >= len(inputword)-2")
        #     feq.append([b[i][0], count])


        # if (count != 0):
        #     feq.append([b[i][0], count])
    # tmp = sorted(feq, key=lambda student: student[1], reverse=True)[:5]
    #tmp = sorted(feq, key=lambda student: student[1], reverse=True)
    tmp = sorted(checkid, key=checkid.__getitem__, reverse=True)
    return tmp

def loop_send(text_list,user_id):
    for c in text_list:
        line_bot_api.push_message(
            user_id,
            TextSendMessage(text=str(c)))

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

head_contect = []
head_contect_use = []



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global mode,mod,head_contect,head_contect_use
    tmp = []
    user_id = event.source.user_id
    type = event.message.type
    try:
        print("type =",type)
    except:
        print("error type")

    try:
        print("pre insert user_new_mode")
        insert_mode_zero = 0
        insert = ('''insert into mode_user(id_user,mode) values ('%s','%s')''' % (event.source.user_id, insert_mode_zero))
        cursor.execute(insert)

        qe = """select id_user,mode from mode_user where id_user = '""" + event.source.user_id + "'"
        cursor.execute(qe)
        mode_user = cursor.fetchall()
        mode_user = str(mode_user)
        mode_user = mode_user.replace("[('", "")
        mode_user = mode_user.replace("'", "")
        mode_user = mode_user.replace("')]", "")
        mode_user = mode_user.replace(")]", "")
        tmp.append(mode_user.split((",")))
        print("insert user_new_mode")

    except:
        print("pre select id_user,mode from mode")
        qe = """select id_user,mode from mode_user where id_user = '""" + event.source.user_id + "'"
        cursor.execute(qe)
        mode_user = cursor.fetchall()
        mode_user = str(mode_user)
        mode_user = mode_user.replace("[('", "")
        mode_user = mode_user.replace("'", "")
        mode_user = mode_user.replace("')]", "")
        mode_user = mode_user.replace(")]", "")
        tmp.append(mode_user.split((",")))
        print("select id_user,mode from mode")
        #print("insert and select id_user,mode from mode")
        #print(tmp[0][0])
        #print(tmp[0][1])
    try:
        print("mode tmp ",tmp[0][1])
        print("type mode ",type(tmp[0][1]))
    except:
        print("error type mode")
    mode = int(tmp[0][1])

    if mode == 0:
        # stick = event.message.StickerMessage
        # if stick == True:
        #     print("stick =")
        #     print("type =", type(stick))
        tmp__ = createbutton(0)
        line_bot_api.push_message(user_id, tmp__)
        # print("mode 0 wait input")
        # text = event.message.text
        #
        # if text == '2':
        #     choose_mode_2 = 2
        #     try:
        #         query5 = """delete from mode_user where id_user = '""" + event.source.user_id + "'"
        #         cursor.execute(query5)
        #         query4 = (
        #             '''insert into mode_user(id_user,mode) values ('%s','%s')''' % (
        #             event.source.user_id, choose_mode_2))
        #         cursor.execute(query4)
        #         print("insert table  mode_user sucsess")
        #     except:
        #         print("no insert table  mode_user sucsess")
        #
        #
        #     # time.sleep(10)
        #     boo = randint(0,2)
        #
        #     if(boo==0):
        #         line_bot_api.reply_message(
        #             event.reply_token,
        #             TextSendMessage(text='กรุณาพิมพ์ชื่อบริษัทที่ต้องการทราบครับ'))
        #     elif(boo==1):
        #         line_bot_api.reply_message(
        #             event.reply_token,
        #             TextSendMessage(text='กรอกชื่อบริษัทที่ต้องการทราบได้เลยค่ะ'))
        #     elif(boo==2):
        #         line_bot_api.reply_message(
        #             event.reply_token,
        #             TextSendMessage(text='ท่านต้องการตรวจสอบบริษัทใด'))
        #
        # elif text == '1':
        #     choose_mode_1 = 1
        #     try:
        #         query5 = """delete from mode_user where id_user = '""" + event.source.user_id + "'"
        #         cursor.execute(query5)
        #         query4 = (
        #         '''insert into mode_user(id_user,mode) values ('%s','%s')''' % (event.source.user_id, choose_mode_1))
        #         cursor.execute(query4)
        #         print("insert table  mode_user sucsess")
        #     except:
        #         print("no insert table  mode_user sucsess")
        #     # time.sleep(10)
        #     bee = randint(0,2)
        #     if(bee==0):
        #         line_bot_api.reply_message(
        #             event.reply_token,
        #             TextSendMessage(text='กรุณากรอกเรื่องร้องเรียนที่ต้องการทราบครับ')
        #         )
        #     elif (bee == 1):
        #         line_bot_api.reply_message(
        #             event.reply_token,
        #             TextSendMessage(text='ท่านต้องการดูเรื่องร้องเรียนเรื่องใด')
        #         )
        #     elif (bee == 2):
        #         line_bot_api.reply_message(
        #             event.reply_token,
        #             TextSendMessage(text='โปรดใส่เรื่องร้องเรียนที่อยากสอบถามค่ะ')
        #         )
        #
        # elif text == '4':
        #
        #
        #     print("mode 4")
        #     cursor.execute('''select company_name from count_ocpb where current_date - date_companyname < 30 ''')
        #     data_company_ocpb = cursor.fetchall()
        #     # print(data_company_ocpb)
        #     ar_company_ocpb = set(data_company_ocpb)
        #     # print(ar_company_ocpb)
        #     ar = []
        #     for i in ar_company_ocpb:
        #         count_company_ocpb = data_company_ocpb.count(i)
        #         ar.append([i, count_company_ocpb])
        #         # print(count_company_ocpb)
        #     ar = sorted(ar, key=lambda x: x[1], reverse=True)[:5]
        #     name, feq = zip(*ar)
        #     # line_bot_api.push_message(
        #     #     event.source.user_id,
        #     #     TextSendMessage(text="บริษัทที่ผู้ใช้สนใจมากที่สุดในเดือนนี\n"))
        #     keb_ro=[]
        #     count = 1
        #     for c in range(len(name)):
        #
        #         tmp = name[c][0].replace("('", "").replace("',)", "")
        #         tmp = "อันดับที่ "+str(count)+". "+tmp
        #         keb_ro.append(tmp)
        #         count+=1
        #     # print(name)
        #     # print(feq)
        #     line_bot_api.push_message(
        #         event.source.user_id,
        #         TextSendMessage(text="บริษัทที่ผู้ใช้สนใจมากที่สุดในเดือนนี้\n"+'\n'.join(keb_ro)))
        #
        #     mode_zeroo = 0
        #     try:
        #         query5 = """delete from mode_user where id_user = '""" + event.source.user_id + "'"
        #         cursor.execute(query5)
        #         print(query5)
        #         print("insert table mode_user")
        #         query44 = (
        #             '''insert into mode_user(id_user,mode) values ('%s','%s')''' % (event.source.user_id, mode_zeroo))
        #         cursor.execute(query44)
        #     except:
        #         print("error insert table mode_user")
        #
        # elif text == '3':
        #     head_contect = []
        #     print("mode 3")
        #     cursor.execute('''select id_fpo_count from count_fpo where current_date - date_topicname < 30 ''')
        #     data_company_fpo = cursor.fetchall()
        #     # print(data_company_fpo)
        #     ar_company_fpo = set(data_company_fpo)
        #     # print(ar_company_fpo)
        #     ar = []
        #     for i in ar_company_fpo:
        #         count_company_fpo = data_company_fpo.count(i)
        #         ar.append([i, count_company_fpo])
        #         print(count_company_fpo)
        #
        #     ar = sorted(ar, key=lambda x: x[1], reverse=True)[:5]
        #     name, feq = zip(*ar)
        #
        #     keb_ro = []
        #     for c in range(len(name)):
        #         tmp = name[c][0]
        #         keb_ro.append(tmp)
        #
        #     line_bot_api.push_message(
        #         event.source.user_id,
        #         TextSendMessage(text="เรื่องร้องเรียนที่ผู้ใช้สนใจมากที่สุดในเดือนนี\n"))
        #     data_fpo_check2 = []
        #     for c in keb_ro:
        #         print("c = "+str(c))
        #         q = ("Select topic,content_topic,doyheadsub,date_topic,feedback,doymaster,feedback_date From fpo2 where id_fpo=" + str(c) + ";")
        #         cursor.execute(q)
        #         datafpo = cursor.fetchall()
        #         #datafpo[0][0] = str(datafpo[0][0])
        #         topic = datafpo[0][0][:200]
        #
        #         t = cutkumkean(datafpo[0][1])[:4]
        #         t3 = "วันที่ร้องเรียน :" + str(datafpo[0][3])
        #         t4 = cutkumkean(str("ตอบข้อร้องเรียน :" + datafpo[0][4]))
        #         t6 = "วันที่ตอบข้อร้องเรียน :" + str(datafpo[0][6])
        #
        #         data_fpo_check2.append([topic.replace("หัวข้อร้องเรียน:", ""), t])
        #         head_contect.append([topic, t, t3, t4, t6, c])
        #     d = se(2, head_contect,event.source.user_id)
        #     if (len(d) == 0):
        #         line_bot_api.push_message(
        #             event.source.user_id,
        #             TextSendMessage(text="ไม่พบการกระทำผิดเกี่ยวกับข้อมูลที่ท่านได้สอบถาม")
        #         )
        #
        #     elif (len(d) > 5):
        #         for c in range(0, len(d) + 1, 5):
        #             if (c + 5 < len(d)):
        #
        #                 carousel_template_message = TemplateSendMessage(
        #                     alt_text='Carousel template',
        #                     template=CarouselTemplate(
        #                         columns=d[c:c + 5]
        #                     )
        #                 )
        #                 line_bot_api.push_message(event.source.user_id, carousel_template_message)
        #             else:
        #
        #                 carousel_template_message = TemplateSendMessage(
        #                     alt_text='Carousel template',
        #                     template=CarouselTemplate(
        #                         columns=d[c:]
        #                     )
        #                 )
        #                 line_bot_api.push_message(event.source.user_id, carousel_template_message)
        #                 print("send_se if1")
        #
        #
        #     else:
        #         carousel_template_message = TemplateSendMessage(
        #             alt_text='Carousel template',
        #             template=CarouselTemplate(
        #                 columns=d
        #             )
        #         )
        #         line_bot_api.push_message(event.source.user_id, carousel_template_message)
        #         print("send_se else")
        #
        #     mode_zeroo = 0
        #     try:
        #         query5 = """delete from mode_user where id_user = '""" + event.source.user_id + "'"
        #         cursor.execute(query5)
        #         print(query5)
        #         print("insert table mode_user")
        #         query44 = (
        #             '''insert into mode_user(id_user,mode) values ('%s','%s')''' % (event.source.user_id, mode_zeroo))
        #         cursor.execute(query44)
        #     except:
        #         print("error insert table mode_user")
        #
        # elif text == '6':
        #
        #     choose_mode_6 = 6
        #     try:
        #         query5 = """delete from mode_user where id_user = '""" + event.source.user_id + "'"
        #         cursor.execute(query5)
        #         query4 = (
        #             '''insert into mode_user(id_user,mode) values ('%s','%s')''' % (
        #             event.source.user_id, choose_mode_6))
        #         cursor.execute(query4)
        #         print("insert table  mode_user sucsess")
        #     except:
        #         print("no insert table  mode_user sucsess")
        #
        #     line_bot_api.push_message(
        #         event.source.user_id,
        #         TextSendMessage(text='โปรดกรอกคำสำคัญชื่อบริษัทที่ต้องการรับการแจ้งเตือนให้ถูกต้องครับ')
        #     )
        #
        # elif text == '5':
        #     choose_mode_5 = 5
        #     try:
        #         query5 = """delete from mode_user where id_user = '""" + event.source.user_id + "'"
        #         cursor.execute(query5)
        #         query4 = (
        #             '''insert into mode_user(id_user,mode) values ('%s','%s')''' % (
        #             event.source.user_id, choose_mode_5))
        #         cursor.execute(query4)
        #         print("insert table  mode_user sucsess")
        #     except:
        #         print("no insert table  mode_user sucsess")
        #
        #     line_bot_api.push_message(
        #         event.source.user_id,
        #         TextSendMessage(text='โปรดกรอกคำสำคัญเรื่องร้องเรียนที่ต้องการรับการแจ้งเตือนให้ถูกต้องครับ')
        #     )
        #
        # elif text == '7':
        #     choose_mode_7 = 7
        #     try:
        #         query5 = """delete from mode_user where id_user = '""" + event.source.user_id + "'"
        #         cursor.execute(query5)
        #         query4 = (
        #             '''insert into mode_user(id_user,mode) values ('%s','%s')''' % (
        #                 event.source.user_id, choose_mode_7))
        #         cursor.execute(query4)
        #         print("insert table  mode_user sucsess")
        #     except:
        #         print("no insert table  mode_user sucsess")
        #
        #     line_bot_api.push_message(
        #         event.source.user_id,
        #         TextSendMessage(text='กรอกหัวข้อร้องเรียนที่ไม่ต้องการรับการแจ้งเตือนครับ')
        #     )
        #
        # elif text == '8':
        #
        #     choose_mode_8 = 8
        #     try:
        #         query5 = """delete from mode_user where id_user = '""" + event.source.user_id + "'"
        #         cursor.execute(query5)
        #         query4 = (
        #             '''insert into mode_user(id_user,mode) values ('%s','%s')''' % (
        #             event.source.user_id, choose_mode_8))
        #         cursor.execute(query4)
        #         print("insert table  mode_user sucsess")
        #     except:
        #         print("no insert table  mode_user sucsess")
        #
        #     line_bot_api.push_message(
        #         event.source.user_id,
        #         TextSendMessage(text='กรอกชื่อบริษัทที่ไม่ต้องการรับการแจ้งเตือนครับ')
        #     )
        #
        # else:
        #     # carousel_template_message = TemplateSendMessage(
        #     #     alt_text='Carousel template',
        #     #     template=CarouselTemplate(
        #     #         columns=d[c:c + 5]
        #     #     )
        #     # )
        #     # print("send_se ifsad1")
        #
        #     # line_bot_api.push_message(event.source.user_id, carousel_template_message)
        #     line_bot_api.reply_message(
        #         event.reply_token,
        #         TextSendMessage(
        #             text="สวัสดีครับต้องการให้ผมช่วยเหลือด้านไหนครับ\nกด 1.ตรวจสอบเรื่องร้องเรียน\nกด 2 ตรวจสอบบริษัทที่ถูกดำเนินคดี"
        #                  "\nกด 3 ดูเรื่องร้องเรียนที่ผู้ใช้สนใจในเดือนนี้\nกด 4 ดูบริษัทที่ผู้ใช้สนใจในเดือนนี้"
        #                  "\nกด 5 รับการแจ้งเตือนเรื่องร้องเรียนของบริษัทจากสำนักงานเศรษฐกิจการคลัง\nกด 6 รับการแจ้งเตือนบริษัทที่ถูกคณะกรรมการคุ้มครองผู้บริโภคให้ดำเนินคดี \n"
        #                  "กด 7 ยกเลิกการแจ้งเตือนเรื่องร้องเรียน\nกด 8 ยกเลิกการแจ้งเตือนบริษัทที่ถูกดำเนินคดี"))
    elif mode == 2:
        print("mode 2")

        # boo = randint(0, 2)
        #
        # if(boo==0):
        #     line_bot_api.reply_message(
        #         event.reply_token,
        #         TextSendMessage(text='กรุณาพิมพ์ชื่อบริษัทที่ต้องการทราบครับ'))
        # elif(boo==1):
        #     line_bot_api.reply_message(
        #         event.reply_token,
        #         TextSendMessage(text='กรอกชื่อบริษัทที่ต้องการทราบได้เลยค่ะ'))
        # elif(boo==2):
        #     line_bot_api.reply_message(
        #         event.reply_token,
        #         TextSendMessage(text='ท่านต้องการตรวจสอบบริษัทใด'))

        a = event.message.text
        a = str(a).lower()
        today = date.today()

        try:
            # count_point = 1
            # cursor.execute('''select count(*) from topchart_ocpb''')
            # count_topchart_ocpb = cursor.fetchall()
            # count_topchart_ocpb =+1
            # insertmode1 = ('''insert into topchart_ocpb(company_name_count)
            #                 values (%s,%s)'''
            #                 ,(count_topchart_ocpb,a))
            # cursor.execute(insertmode1)

            cursor.execute('''insert into count_ocpb(company_name,date_companyname)
                            values (%s,%s)'''
                            ,(a,today))
            print("insert table topchart_ocpb sucsess")
        except:
            cursor.execute('''insert into count_ocpb(company_name,date_companyname)
                            values (%s,%s)'''
                            , (a,today))
            print("error insert table topchart_ocpb")


        try:
            tmp_ = check(a)
            print("check")
        except:
            print("not check")
        try:
            print("len tmp =", len(tmp_))
        except:
            print("not len tmp =")
        try:
            if(len(tmp_)!=0):
                try:
                    for i in tmp_:
                            index = i
                            #fre = tmp_[i]

                            print(index)
                            try:
                                q = ("select company_name,project_name from ocpb2 where id ="+str(index)+";")
                                cursor.execute(q)
                                de = cursor.fetchall()
                                kum = de[0][0] +" "+ de[0][1]+"\n ถูกคณะกรรมการคุ้มครองผู้บริโภค มีมติให้ดำเนินคดี"
                                line_bot_api.push_message(
                                    event.source.user_id,
                                    TextSendMessage(text=kum))
                                print(de[0][0])

                                # textdb = join_text(db[index-1])
                                # line_bot_api.push_message(
                                #     event.source.user_id,
                                #     TextSendMessage(text=textdb))
                                #print(len(de))
                            except:
                                print("error q")
                    mode_zeroo = 0
                    try:
                        query5 = """delete from mode_user where id_user = '""" + event.source.user_id + "'"
                        cursor.execute(query5)
                        print(query5)
                        print("insert table mode_user")
                        query44 = (
                            '''insert into mode_user(id_user,mode) values ('%s','%s')''' % (
                                event.source.user_id, mode_zeroo))
                        cursor.execute(query44)
                    except:
                        print("error insert table mode_user")
                except:
                    print("eeerrer")
                mode_zeroo = 0
                try:
                    query5 = """delete from mode_user where id_user = '""" + event.source.user_id + "'"
                    cursor.execute(query5)
                    print(query5)
                    print("insert table mode_user")
                    query44 = (
                        '''insert into mode_user(id_user,mode) values ('%s','%s')''' % (
                            event.source.user_id, mode_zeroo))
                    cursor.execute(query44)
                except:
                    print("error insert table mode_user")
            else:
                line_bot_api.push_message(
                    event.source.user_id,
                    TextSendMessage(text="บริษัทที่ท่านกรอกเข้ามาไม่ถูกดำเนินคดี"))

                mode_zeroo = 0
                try:
                    query5 = """delete from mode_user where id_user = '""" + event.source.user_id + "'"
                    cursor.execute(query5)
                    print(query5)
                    print("insert table mode_user")
                    query44 = (
                        '''insert into mode_user(id_user,mode) values ('%s','%s')''' % (
                        event.source.user_id, mode_zeroo))
                    cursor.execute(query44)
                except:
                    print("error insert table mode_user")
        except:
            line_bot_api.push_message(
                event.source.user_id,
                TextSendMessage(text="ขออภัยระบบขัดข้อง กรุณาทำรายการใหม่ครับ"))
            mode_zeroo = 0
            try:
                query5 = """delete from mode_user where id_user = '""" + event.source.user_id + "'"
                cursor.execute(query5)
                print(query5)
                print("insert table mode_user")
                query44 = (
                '''insert into mode_user(id_user,mode) values ('%s','%s')''' % (event.source.user_id, mode_zeroo))
                cursor.execute(query44)
            except:
                print("error insert table mode_user")

    elif mode == 1:
        print("mode 1")
        # time.sleep(20)
        a = event.message.text
        # stick = event.message.StickerMessage
        # if stick == True :
        #     print("stick =")
        #     print("type =",type(stick))
        a = str(a).lower()

        try:
            tmp_ = checkfpo(a)
            print(tmp_)
            #print("len tmp ="+len(tmp_))

            print("check")
        except:
            print("not check")
        try:
            print("check fpo ok")
            data_fpo_check=[]
            head_contect = []
            for i in tmp_:
                index = i
                #fre = i[1]
                #print(index+" "+fre)

                try:

                    q = ("Select topic,content_topic,doyheadsub,date_topic,feedback,doymaster,feedback_date From fpo3 where id_fpo="+str(index)+";")
                    cursor.execute(q)
                    datafpo = cursor.fetchall()


                    try:
                        topic = datafpo[0][0][:100]
                        t = cutkumkean(datafpo[0][1])[:4]
                        t3 = "วันที่ร้องเรียน :" + str(datafpo[0][3])
                        t4 = cutkumkean(str("ตอบข้อร้องเรียน :" + datafpo[0][4]))
                        t6 = "วันที่ตอบข้อร้องเรียน :" + str(datafpo[0][6])
                        data_fpo_check.append([topic.replace("หัวข้อร้องเรียน:", ""), t])
                        head_contect.append([topic, t, t3, t4, t6, index])
                        #print("head_contect topic - index")
                    except:
                        topic = datafpo[0][0][:100]
                        t = cutkumkean(datafpo[0][1])
                        t3 = "วันที่ร้องเรียน :" + str(datafpo[0][3])
                        head_contect.append([topic, t, t3,index])
                        #print("head_contect topic - t3 , index")
                    #print("con head_contect")
                except:
                    print("error con head_contect")

            try:
                #print("will d = se(1,head_contect)")
                d = se(1,head_contect,event.source.user_id)
                print("d = ")
                print(len(d))
                if(len(d)==0):
                    line_bot_api.push_message(
                        event.source.user_id,
                        TextSendMessage(text="ไม่พบเรื่องร้องเรียนที่กระทำผิดเกี่ยวกับข้อมูลที่ท่านได้สอบถาม")
                    )

                elif(len(d)>5):
                    print("d = >5 ")
                    for c in range(0,len(d),5):
                        #time.sleep(2)
                        if(c+5<len(d)):
                            print("c+5<len(d) ")
                            carousel_template_message = TemplateSendMessage(
                                alt_text='Carousel template',
                                template=CarouselTemplate(
                                    columns=d[c:c+5]
                                )
                            )
                            print("send_se ifsad1")
                            try:
                                line_bot_api.push_message(event.source.user_id, carousel_template_message)
                            except:
                                print("send_se if1")
                        else:
                            print("c+5>len(d) ")
                            carousel_template_message = TemplateSendMessage(
                                alt_text='Carousel template',
                                template=CarouselTemplate(
                                    columns=d[c:]
                                )
                            )
                            try:
                                line_bot_api.push_message(event.source.user_id, carousel_template_message)
                            except:
                                print("send_se if1")
                            print("send_se if")
                else:
                    print("c+5>len(d) elssssssssssssssse")
                    carousel_template_message = TemplateSendMessage(
                        alt_text='Carousel template',
                        template=CarouselTemplate(
                            columns=d
                        )
                    )
                    try:
                        line_bot_api.push_message(event.source.user_id, carousel_template_message)
                    except:
                        print("send_se if1")


                    print("send_se else")


                print("send message")
            except:
                print("not send message")

        except:
            print("check pfo error")
        mode_zeroo = 0
        try:
            query5 = """delete from mode_user where id_user = '""" + event.source.user_id + "'"
            cursor.execute(query5)
            print(query5)
            print("insert table mode_user")
            query44 = ('''insert into mode_user(id_user,mode) values ('%s','%s')''' % (event.source.user_id, mode_zeroo))
            cursor.execute(query44)
        except:
            print("error insert table mode_user")

    elif mode == 4:
        print("mode 4")
        cursor.execute('''select company_name from count_ocpb where current_date - date_companyname < 30 ''')
        data_company_ocpb = cursor.fetchall()
        # print(data_company_ocpb)
        ar_company_ocpb = set(data_company_ocpb)
        # print(ar_company_ocpb)
        ar = []
        for i in ar_company_ocpb:
            count_company_ocpb = data_company_ocpb.count(i)
            ar.append([i, count_company_ocpb])
            # print(count_company_ocpb)
        ar = sorted(ar, key=lambda x: x[1], reverse=True)[:5]
        name, feq = zip(*ar)
        # line_bot_api.push_message(
        #     event.source.user_id,
        #     TextSendMessage(text="บริษัทที่ผู้ใช้สนใจมากที่สุดในเดือนนี\n"))
        keb_ro=[]
        count = 1
        for c in range(len(name)):

            tmp = name[c][0].replace("('", "").replace("',)", "")
            tmp = "อันดับที่ "+str(count)+". "+tmp
            keb_ro.append(tmp)
            count+=1
        # print(name)
        # print(feq)
        line_bot_api.push_message(
            event.source.user_id,
            TextSendMessage(text="บริษัทที่ผู้ใช้สนใจมากที่สุดในเดือนนี้\n"+'\n'.join(keb_ro)))

        mode_zeroo = 0
        try:
            query5 = """delete from mode_user where id_user = '""" + event.source.user_id + "'"
            cursor.execute(query5)
            print(query5)
            print("insert table mode_user")
            query44 = (
                '''insert into mode_user(id_user,mode) values ('%s','%s')''' % (event.source.user_id, mode_zeroo))
            cursor.execute(query44)
        except:
            print("error insert table mode_user")

    elif mode == 3:
        head_contect = []
        print("mode 3")
        cursor.execute('''select id_fpo_count from count_fpo where current_date - date_topicname < 30 ''')
        data_company_fpo = cursor.fetchall()
        # print(data_company_fpo)
        ar_company_fpo = set(data_company_fpo)
        # print(ar_company_fpo)
        ar = []
        for i in ar_company_fpo:
            count_company_fpo = data_company_fpo.count(i)
            ar.append([i, count_company_fpo])
            print(count_company_fpo)

        ar = sorted(ar, key=lambda x: x[1], reverse=True)[:5]
        name, feq = zip(*ar)

        keb_ro = []
        for c in range(len(name)):
            tmp = name[c][0]
            keb_ro.append(tmp)

        line_bot_api.push_message(
            event.source.user_id,
            TextSendMessage(text="เรื่องร้องเรียนที่ผู้ใช้สนใจมากที่สุดในเดือนนี้\n"))
        data_fpo_check2 = []
        for c in keb_ro:
            print("c = "+str(c))
            q = ("Select topic,content_topic,doyheadsub,date_topic,feedback,doymaster,feedback_date From fpo2 where id_fpo=" + str(c) + ";")
            cursor.execute(q)
            datafpo = cursor.fetchall()
            #datafpo[0][0] = str(datafpo[0][0])
            topic = datafpo[0][0][:200]

            t = cutkumkean(datafpo[0][1])[:4]
            t3 = "วันที่ร้องเรียน :" + str(datafpo[0][3])
            t4 = cutkumkean(str("ตอบข้อร้องเรียน :" + datafpo[0][4]))
            t6 = "วันที่ตอบข้อร้องเรียน :" + str(datafpo[0][6])

            data_fpo_check2.append([topic.replace("หัวข้อร้องเรียน:", ""), t])
            head_contect.append([topic, t, t3, t4, t6, c])
        d = se(2, head_contect,event.source.user_id)
        if (len(d) == 0):
            line_bot_api.push_message(
                event.source.user_id,
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
                    line_bot_api.push_message(event.source.user_id, carousel_template_message)
                else:

                    carousel_template_message = TemplateSendMessage(
                        alt_text='Carousel template',
                        template=CarouselTemplate(
                            columns=d[c:]
                        )
                    )
                    line_bot_api.push_message(event.source.user_id, carousel_template_message)
                    print("send_se if1")


        else:
            carousel_template_message = TemplateSendMessage(
                alt_text='Carousel template',
                template=CarouselTemplate(
                    columns=d
                )
            )
            line_bot_api.push_message(event.source.user_id, carousel_template_message)
            print("send_se else")

        mode_zeroo = 0
        try:
            query5 = """delete from mode_user where id_user = '""" + event.source.user_id + "'"
            cursor.execute(query5)
            print(query5)
            print("insert table mode_user")
            query44 = (
                '''insert into mode_user(id_user,mode) values ('%s','%s')''' % (event.source.user_id, mode_zeroo))
            cursor.execute(query44)
        except:
            print("error insert table mode_user")

    elif mode == 6:
        print("elif mode 6")
        a = event.message.text
        try:
            qe = """select user_id_hiscompany,namecompany_his from user_history_company where user_id_hiscompany = '"""+event.source.user_id+"'"
            # print(qe)
            cursor.execute(qe)
            gg = cursor.fetchall()
            kebkum2 = []
            number = 0

            for c in gg:
                word = str(c)
                word = word.replace("('", "")
                word = word.replace("')", "")
                word = word.replace("'", "")
                word = word.replace(" ", "")
                # kebkum2.append(warpcut(word))
                kebkum2.append(word.split(","))
                number+=1
            # print("len(kebkum2)" + len(kebkum2))
            print(number)
            if(number==0):
                print("len(kebkum2) = 0 ")
                query555 = '''insert into user_history_company(user_id_hiscompany, namecompany_his) values ('%s','%s')''' % (
                event.source.user_id, a)
                cursor.execute(query555)
                line_bot_api.push_message(
                    event.source.user_id,
                    TextSendMessage(text='ระบบได้ทำการบันทึกข้อมูลเรียบร้อยครับ')
                )
                print("no campany by user ")

            else:
                print("in else mode 6")
                ccc = True
                for b in range(len(kebkum2)):

                    # repr(kebkum2[b][1])
                    # repr(a)

                    print(kebkum2[b][1])
                    print(a)
                    print(type(kebkum2[b][1]))
                    print(type(a))
                    try:
                        #teabkum1 = re.findall(r"""'+a+'""",kebkum2[b][1])
                        teabkum1 = (a in kebkum2[b][1])
                        print("teabkum1 = "+ teabkum1)
                    except:
                        print("no teamkum")
                    if(teabkum1==True):
                        print("check kebkum2[b][1] != a")
                        ccc = False

                if(ccc is True):
                    print("ccc is True")
                    query555 = '''insert into user_history_company(user_id_hiscompany, namecompany_his) values ('%s','%s')''' % (event.source.user_id, a)
                    cursor.execute(query555)
                    line_bot_api.push_message(
                        event.source.user_id,
                        TextSendMessage(text='ระบบได้ทำการบันทึกข้อมูลเรียบร้อยครับ')
                    )
                elif(ccc is False):
                    print("ccc is False")
                    line_bot_api.push_message(
                        event.source.user_id,
                        TextSendMessage(text='มีข้อมูลในระบบแล้ว ขอบคุณที่ใช้บริการครับ')
                    )
            print("sucsess insert user_history_company")


        except:
            print("no sucsess insert user_history_company")

        mode_zeroo = 0
        try:
            query5 = """delete from mode_user where id_user = '""" + event.source.user_id + "'"
            cursor.execute(query5)
            print(query5)
            print("insert table mode_user")
            query44 = (
            '''insert into mode_user(id_user,mode) values ('%s','%s')''' % (event.source.user_id, mode_zeroo))
            cursor.execute(query44)
        except:
            print("error insert table mode_user")

    elif mode == 5:
        print("elif mode 5")
        a = event.message.text
        a = str(a).lower()

        try:
            qe = """select user_id_hisfpo,fpo_his from user_history_fpo where user_id_hisfpo = '"""+event.source.user_id+"'"
            cursor.execute(qe)
            gg = cursor.fetchall()
            kebkum2 = []
            number = 0

            for c in gg:
                word = str(c)
                word = word.replace("('", "")
                word = word.replace("')", "")
                word = word.replace("'", "")
                word = word.replace(" ", "")
                # kebkum2.append(warpcut(word))
                kebkum2.append(word.split(","))
                print(kebkum2)
                number+=1
            # print("len(kebkum2)" + len(kebkum2))
            print(number)
            if(number==0):
                print("len(kebkum2) = 0 ")
                query555 = '''insert into user_history_fpo(user_id_hisfpo,fpo_his) values ('%s','%s')''' % (event.source.user_id, a)

                cursor.execute(query555)
                line_bot_api.push_message(
                    event.source.user_id,
                    TextSendMessage(text='ระบบได้ทำการบันทึกข้อมูลเรียบร้อยครับ')
                )
                print("no fpo by user ")

            else:
                print("no else fpo by user")

                ccc = True
                for b in range(len(kebkum2)):

                    print(kebkum2[b][1])
                    print(a)
                    print(type(kebkum2[b][1]))
                    print(type(a))
                    try:
                        #teabkum1 = re.findall(r"""'+a+'""",kebkum2[b][1])
                        teabkum1 = (a in kebkum2[b][1])
                        print("teabkum1 = "+ teabkum1)
                    except:
                        print("no teamkum")
                    if(teabkum1==True):
                        print("check kebkum2[b][1] != a")
                        ccc = False

                if(ccc is True):
                    print("ccc is True")
                    query555 = '''insert into user_history_fpo(user_id_hisfpo, fpo_his) values ('%s','%s')''' % (event.source.user_id, a)
                    cursor.execute(query555)
                    line_bot_api.push_message(
                        event.source.user_id,
                        TextSendMessage(text='ระบบได้ทำการบันทึกข้อมูลเรียบร้อยครับ')
                    )
                elif(ccc is False):
                    print("ccc is False")
                    line_bot_api.push_message(
                        event.source.user_id,
                        TextSendMessage(text='มีข้อมูลในระบบแล้ว ขอบคุณที่ใช้บริการครับ')
                    )
            print("sucsess insert user_history_company")


        except:
            print("no sucsess insert user_history_company")


        mode_zeroo = 0
        try:
            query5 = """delete from mode_user where id_user = '""" + event.source.user_id + "'"
            cursor.execute(query5)
            print(query5)
            print("insert table mode_user")
            query44 = (
            '''insert into mode_user(id_user,mode) values ('%s','%s')''' % (event.source.user_id, mode_zeroo))
            cursor.execute(query44)
        except:
            print("error insert table mode_user")

    elif mode == 7:

        print("elif mode 7")
        a = event.message.text
        a = str(a).lower()

        try:
            qe = """select user_id_hisfpo,fpo_his from user_history_fpo where user_id_hisfpo = '"""+event.source.user_id+"'"
            cursor.execute(qe)
            gg = cursor.fetchall()
            kebkum2 = []
            number = 0

            for c in gg:
                word = str(c)
                word = word.replace("('", "")
                word = word.replace("')", "")
                word = word.replace("'", "")
                word = word.replace(" ", "")
                # kebkum2.append(warpcut(word))
                kebkum2.append(word.split(","))
                print(kebkum2)
                number+=1
            # print("len(kebkum2)" + len(kebkum2))
            print(number)
            if(number==0):

                print("len(kebkum2) = 0 ")
                line_bot_api.push_message(
                    event.source.user_id,
                    TextSendMessage(text='ไม่มีข้อมูลเรื่องร้องเรียนที่ท่านต้องการลบในระบบครับ')
                )
                print("no delete fpo by user ")

            else:
                print("no else fpo by user")

                ccc = True
                for b in range(len(kebkum2)):

                    print("kebkum2[b][1] ="+kebkum2[b][1])
                    print("a ="+a)
                    # print(type(kebkum2[b][1]))
                    # print(type(a))

                    if(eq(kebkum2[b][1], a)==True):
                        ccc = False
                        print("eq(kebkum2[b][1], a)==True")

                if(ccc is True):
                    print("ccc is True")
                    line_bot_api.push_message(
                        event.source.user_id,
                        TextSendMessage(text='ไม่มีเรื่องร้องเรียนเรื่อง '+a+' ที่ต้องการลบในระบบครับ')
                    )
                elif(ccc is False):
                    print("ccc is False")
                    query555 = "delete from user_history_fpo where user_id_hisfpo = '"""+event.source.user_id+"' and fpo_his = '"+a+"'"
                    cursor.execute(query555)
                    line_bot_api.push_message(
                        event.source.user_id,
                        TextSendMessage(text='ระบบได้ทำการลบการแจ้งเตือนเรื่องร้องเรียน '+a+' เรียบร้อยครับ')
                    )
            print("sucsess delete user_history_company")


        except:
            print("no sucsess insert user_history_company")


        mode_zeroo = 0
        try:
            query5 = """delete from mode_user where id_user = '""" + event.source.user_id + "'"
            cursor.execute(query5)
            print(query5)
            print("insert table mode_user")
            query44 = (
            '''insert into mode_user(id_user,mode) values ('%s','%s')''' % (event.source.user_id, mode_zeroo))
            cursor.execute(query44)
        except:
            print("error insert table mode_user")

    elif mode == 8:

        print("elif mode 8")
        a = event.message.text
        a = str(a).lower()

        try:
            qe = """select user_id_hiscompany,namecompany_his from user_history_company where user_id_hiscompany = '"""+event.source.user_id+"'"
            cursor.execute(qe)
            gg = cursor.fetchall()
            kebkum2 = []
            number = 0

            for c in gg:
                word = str(c)
                word = word.replace("('", "")
                word = word.replace("')", "")
                word = word.replace("'", "")
                word = word.replace(" ", "")
                # kebkum2.append(warpcut(word))
                kebkum2.append(word.split(","))
                print(kebkum2)
                number+=1
            # print("len(kebkum2)" + len(kebkum2))
            print(number)
            if(number==0):

                print("len(kebkum2) = 0 ")
                line_bot_api.push_message(
                    event.source.user_id,
                    TextSendMessage(text='ไม่มีข้อมูลบริษัทที่ท่านต้องการลบในระบบครับ')
                )
                print("no delete fpo by user ")

            else:
                print("no else fpo by user")

                ccc = True
                for b in range(len(kebkum2)):

                    print("kebkum2[b][1] ="+kebkum2[b][1])
                    print("a ="+a)
                    # print(type(kebkum2[b][1]))
                    # print(type(a))

                    if(eq(kebkum2[b][1], a)==True):
                        ccc = False
                        print("eq(kebkum2[b][1], a)==True")

                if(ccc is True):
                    print("ccc is True")
                    line_bot_api.push_message(
                        event.source.user_id,
                        TextSendMessage(text='ไม่มีชื่อบริษัท '+a+' ที่ต้องการลบในระบบครับ')
                    )
                elif(ccc is False):
                    print("ccc is False")
                    query555 = "delete from user_history_company where user_id_hiscompany = '"""+event.source.user_id+"' and namecompany_his = '"+a+"'"
                    cursor.execute(query555)
                    line_bot_api.push_message(
                        event.source.user_id,
                        TextSendMessage(text='ระบบได้ทำการลบการแจ้งเตือนบริษัท '+a+' เรียบร้อยครับ')
                    )
            print("sucsess delete user_history_company")


        except:
            print("no sucsess insert user_history_company")


        mode_zeroo = 0
        try:
            query5 = """delete from mode_user where id_user = '""" + event.source.user_id + "'"
            cursor.execute(query5)
            print(query5)
            print("insert table mode_user")
            query44 = (
            '''insert into mode_user(id_user,mode) values ('%s','%s')''' % (event.source.user_id, mode_zeroo))
            cursor.execute(query44)
        except:
            print("error insert table mode_user")

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    tmp = []
    try:
        print("pre insert user_new_mode")
        insert_mode_zero = 0
        insert = ('''insert into mode_user(id_user,mode) values ('%s','%s')''' % (event.source.user_id, insert_mode_zero))
        cursor.execute(insert)

        qe = """select id_user,mode from mode_user where id_user = '""" + event.source.user_id + "'"
        cursor.execute(qe)
        mode_user = cursor.fetchall()
        mode_user = str(mode_user)
        mode_user = mode_user.replace("[('", "")
        mode_user = mode_user.replace("'", "")
        mode_user = mode_user.replace("')]", "")
        mode_user = mode_user.replace(")]", "")
        tmp.append(mode_user.split((",")))
        print("insert user_new_mode")

    except:
        print("pre select id_user,mode from mode")
        qe = """select id_user,mode from mode_user where id_user = '""" + event.source.user_id + "'"
        cursor.execute(qe)
        mode_user = cursor.fetchall()
        mode_user = str(mode_user)
        mode_user = mode_user.replace("[('", "")
        mode_user = mode_user.replace("'", "")
        mode_user = mode_user.replace("')]", "")
        mode_user = mode_user.replace(")]", "")
        tmp.append(mode_user.split((",")))
        print("select id_user,mode from mode")

    line_bot_api.push_message(event.source.user_id, TextSendMessage(text="โปรดเลือกรายการที่ต้องการทำ"))
    tmp__ = createbutton(0)
    line_bot_api.push_message(event.source.user_id, tmp__)

head_contect2 = []
def sent_mode4(u_id,index):

    i = index - 1
    line_bot_api.push_message(u_id, TextSendMessage(text=head_contect[i][0])) #------- debug runtime
    loop_send(head_contect[i][1], u_id)
    loop_send([head_contect[i][2]], u_id)
    # loop_send(head_contect[i][3], u_id)
    # loop_send([head_contect[i][4]], u_id)
    try:
        loop_send(head_contect[i][3], u_id)
        loop_send([head_contect[i][4]], u_id)
    #     print("ok sent loop_send(head_contect[i][3],head_contect[i][4]")
    except:
        print("no sent loop_send(head_contect[i][3],head_contect[1][4]")

def sent(u_id, head_contect):
    line_bot_api.push_message(u_id, TextSendMessage(text=head_contect[0]))
    loop_send(head_contect[1], u_id)
    loop_send([head_contect[2]], u_id)
    try:
        loop_send(head_contect[3], u_id)
    except:
        pass

    try:
        loop_send([head_contect[4]], u_id)
    except:
        pass


def setMode(user_id, mode):
    user_id = str(user_id)
    mode = str(mode)
    try:
        query5 = """delete from mode_user where id_user = '""" + user_id + "'"
        cursor.execute(query5)
        print(query5)
        print("insert table mode_user")
        query44 = (
            '''insert into mode_user(id_user,mode) values ('%s','%s')''' % (
                user_id, mode))
        cursor.execute(query44)
    except:
        print("error insert table mode_user")

    if(mode == '2'):
        boo = randint(0, 2)
        if(boo==0):
            line_bot_api.push_message(
                user_id,
                TextSendMessage(text='กรุณาพิมพ์ชื่อบริษัทที่ต้องการทราบครับ'))
        elif(boo==1):
            line_bot_api.push_message(
                user_id,
                TextSendMessage(text='กรอกชื่อบริษัทที่ต้องการทราบได้เลยค่ะ'))
        elif(boo==2):
            line_bot_api.push_message(
                user_id,
                TextSendMessage(text='ท่านต้องการตรวจสอบบริษัทใด'))

    if(mode == '1'):
        bee = randint(0, 2)
        if (bee == 0):
            line_bot_api.push_message(
                user_id,
                TextSendMessage(text='กรุณากรอกเรื่องร้องเรียนที่ต้องการทราบครับ')
            )
        elif (bee == 1):
            line_bot_api.push_message(
                user_id,
                TextSendMessage(text='ท่านต้องการดูเรื่องร้องเรียนเรื่องใด')
            )
        elif (bee == 2):
            line_bot_api.push_message(
                user_id,
                TextSendMessage(text='โปรดใส่เรื่องร้องเรียนที่อยากสอบถามค่ะ')
            )

    if mode == '4':
        print("mode 4")
        cursor.execute('''select company_name from count_ocpb where current_date - date_companyname < 30 ''')
        data_company_ocpb = cursor.fetchall()
        # print(data_company_ocpb)
        ar_company_ocpb = set(data_company_ocpb)
        # print(ar_company_ocpb)
        ar = []
        for i in ar_company_ocpb:
            count_company_ocpb = data_company_ocpb.count(i)
            ar.append([i, count_company_ocpb])
            # print(count_company_ocpb)
        ar = sorted(ar, key=lambda x: x[1], reverse=True)[:5]
        name, feq = zip(*ar)
        # line_bot_api.push_message(
        #     event.source.user_id,
        #     TextSendMessage(text="บริษัทที่ผู้ใช้สนใจมากที่สุดในเดือนนี\n"))
        keb_ro = []
        count = 1
        for c in range(len(name)):
            tmp = name[c][0].replace("('", "").replace("',)", "")
            tmp = "อันดับที่ " + str(count) + ". " + tmp
            keb_ro.append(tmp)
            count += 1
        # print(name)
        # print(feq)
        line_bot_api.push_message(
            user_id,
            TextSendMessage(text="บริษัทที่ผู้ใช้สนใจมากที่สุดในเดือนนี้\n" + '\n'.join(keb_ro)))

        mode_zeroo = 0
        try:
            query5 = """delete from mode_user where id_user = '""" + user_id + "'"
            cursor.execute(query5)
            print(query5)
            print("insert table mode_user")
            query44 = (
                '''insert into mode_user(id_user,mode) values ('%s','%s')''' % (
                user_id, mode_zeroo))
            cursor.execute(query44)
        except:
            print("error insert table mode_user")

    if mode == '3':
        head_contect = []
        print("mode 3")
        cursor.execute('''select id_fpo_count from count_fpo where current_date - date_topicname < 30 ''')
        data_company_fpo = cursor.fetchall()
        # print(data_company_fpo)
        ar_company_fpo = set(data_company_fpo)
        # print(ar_company_fpo)
        ar = []
        for i in ar_company_fpo:
            count_company_fpo = data_company_fpo.count(i)
            ar.append([i, count_company_fpo])
            print(count_company_fpo)

        ar = sorted(ar, key=lambda x: x[1], reverse=True)[:5]
        name, feq = zip(*ar)

        keb_ro = []
        for c in range(len(name)):
            tmp = name[c][0]
            keb_ro.append(tmp)

        line_bot_api.push_message(
            user_id,
            TextSendMessage(text="เรื่องร้องเรียนที่ผู้ใช้สนใจมากที่สุดในเดือนนี\n"))
        data_fpo_check2 = []
        for c in keb_ro:
            print("c = " + str(c))
            q = (
                "Select topic,content_topic,doyheadsub,date_topic,feedback,doymaster,feedback_date From fpo2 where id_fpo=" + str(
                    c) + ";")
            cursor.execute(q)
            datafpo = cursor.fetchall()
            # datafpo[0][0] = str(datafpo[0][0])
            topic = datafpo[0][0][:200]

            t = cutkumkean(datafpo[0][1])[:4]
            t3 = "วันที่ร้องเรียน :" + str(datafpo[0][3])
            t4 = cutkumkean(str("ตอบข้อร้องเรียน :" + datafpo[0][4]))
            t6 = "วันที่ตอบข้อร้องเรียน :" + str(datafpo[0][6])

            data_fpo_check2.append([topic.replace("หัวข้อร้องเรียน:", ""), t])
            head_contect.append([topic, t, t3, t4, t6, c])
        d = se(2, head_contect, user_id)
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
                    print("send_se if1")


        else:
            carousel_template_message = TemplateSendMessage(
                alt_text='Carousel template',
                template=CarouselTemplate(
                    columns=d
                )
            )
            line_bot_api.push_message(user_id, carousel_template_message)
            print("send_se else")

        mode_zeroo = 0
        try:
            query5 = """delete from mode_user where id_user = '""" + user_id + "'"
            cursor.execute(query5)
            print(query5)
            print("insert table mode_user")
            query44 = (
                '''insert into mode_user(id_user,mode) values ('%s','%s')''' % (
                user_id, mode_zeroo))
            cursor.execute(query44)
        except:
            print("error insert table mode_user")

    if mode == '6':
        line_bot_api.push_message(
            user_id,
            TextSendMessage(text='โปรดกรอกคำสำคัญชื่อบริษัทที่ต้องการรับการแจ้งเตือนให้ถูกต้องครับ')
        )

    if mode == '5':
        line_bot_api.push_message(
            user_id,
            TextSendMessage(text='โปรดกรอกคำสำคัญเรื่องร้องเรียนที่ต้องการรับการแจ้งเตือนให้ถูกต้องครับ')
        )

    if mode == '7':
        line_bot_api.push_message(
            user_id,
            TextSendMessage(text='กรอกหัวข้อร้องเรียนที่ไม่ต้องการรับการแจ้งเตือนครับ')
        )

    if mode == '8':
        line_bot_api.push_message(
            user_id,
            TextSendMessage(text='กรอกชื่อบริษัทที่ไม่ต้องการรับการแจ้งเตือนครับ')
        )


@handler.add(PostbackEvent)
def handle_postback(event):
    tmp = event.postback.data.split('_')
    mode = tmp[0]
    user_id = event.source.user_id
    try:
        index = int(tmp[1])
    except:
        index = tmp[1]

    head_contect2 = []


    print("index =",index)
    if index == "sentBtm":
        temp = createbutton(int(mode))
        print("temp ===== ",temp)
        line_bot_api.push_message(user_id, temp)
        # tmp_xx = "mode:"+str(index)
        # line_bot_api.push_message(user_id, TextSendMessage(text=tmp_xx))

    elif index == "setMode":
        setMode(user_id, mode)

    elif type(index) == int:
        if mode == '1' or mode == '2':
            try:
                q = (
                    "Select topic,content_topic,doyheadsub,date_topic,feedback,doymaster,feedback_date From fpo3 where id_fpo=" + str(
                        index) + ";")
                cursor.execute(q)
                datafpo = cursor.fetchall()

                try:
                    topic = datafpo[0][0][:100]
                    t = cutkumkean(datafpo[0][1])[:4]
                    t3 = "วันที่ร้องเรียน :" + str(datafpo[0][3])
                    t4 = cutkumkean(str("ตอบข้อร้องเรียน :" + datafpo[0][4]))
                    t6 = "วันที่ตอบข้อร้องเรียน :" + str(datafpo[0][6])
                    head_contect2.append([topic, t, t3, t4, t6, index])
                    print("head_contect topic - index")
                except:
                    topic = datafpo[0][0][:100]
                    t = cutkumkean(datafpo[0][1])
                    t3 = "วันที่ร้องเรียน :" + str(datafpo[0][3])
                    head_contect2.append([topic, t, t3, index])
                    print("head_contect topic - t3 , index")
                print("con head_contect")


            except:
                print("error con head_contect")
            head_contect2 = head_contect2[0]

        if mode == '9':
            # elif mode == '1':

            try:
                head_contect4alert = []
                q = (
                "Select topic,content_topic,doyheadsub,date_topic,feedback,doymaster,feedback_date From fpo2 where id_fpo=" + str(
                    index) + ";")
                cursor.execute(q)
                datafpo = cursor.fetchall()

                try:
                    topic = datafpo[0][0][:100]
                    t = cutkumkean(datafpo[0][1])[:4]
                    t3 = "วันที่ร้องเรียน :" + str(datafpo[0][3])
                    t4 = cutkumkean(str("ตอบข้อร้องเรียน :" + datafpo[0][4]))
                    t6 = "วันที่ตอบข้อร้องเรียน :" + str(datafpo[0][6])
                    head_contect4alert.append([topic, t, t3, t4, t6, index])
                    print("head_contect topic - index")
                except:
                    topic = datafpo[0][0][:100]
                    t = cutkumkean(datafpo[0][1])
                    t3 = "วันที่ร้องเรียน :" + str(datafpo[0][3])
                    head_contect4alert.append([topic, t, t3, index])
                    print("head_contect topic - t3 , index")
                print("head_contect4alert =", len(head_contect4alert))
                print("con head_contect")
                head_contect4alert = head_contect4alert[0]
                line_bot_api.push_message(event.source.user_id,
                                          TextSendMessage(text='Hello round:' + str(mode) + "\\" + str(index)))
                try:

                    sent(event.source.user_id, head_contect4alert)
                except:
                    pass
            except:
                print("error con head_contect")

        if mode == '2':

            print("pos mode 2")
            sent(event.source.user_id, head_contect2)
            try:
                query555 = '''insert into count_fpo(id_fpo_count,date_topicname) values (%s,'%s')''' % (
                head_contect2[5], str(date.today()))
                cursor.execute(query555)
                print("sucsess insert count fpo")
            except:
                print("error insert count_fpo")

        if mode == '1':
            # elif mode == '1':

            try:
                sent(event.source.user_id, head_contect2)
                print("sent(event.source.user_id, head_contect2) ok")
            except:
                print("sent(event.source.user_id, head_contect2) error ")
            try:
                query555 = '''insert into count_fpo(id_fpo_count,date_topicname) values (%s,'%s')''' % (
                head_contect2[5], str(date.today()))
                cursor.execute(query555)
                print("sucsess insert count fpo")
            except:
                print("error insert count_fpo")

        # if mode == '4':
        #     print("mode 4")
        #     cursor.execute('''select company_name from count_ocpb where current_date - date_companyname < 30 ''')
        #     data_company_ocpb = cursor.fetchall()
        #     # print(data_company_ocpb)
        #     ar_company_ocpb = set(data_company_ocpb)
        #     # print(ar_company_ocpb)
        #     ar = []
        #     for i in ar_company_ocpb:
        #         count_company_ocpb = data_company_ocpb.count(i)
        #         ar.append([i, count_company_ocpb])
        #         # print(count_company_ocpb)
        #     ar = sorted(ar, key=lambda x: x[1], reverse=True)[:5]
        #     name, feq = zip(*ar)
        #     # line_bot_api.push_message(
        #     #     event.source.user_id,
        #     #     TextSendMessage(text="บริษัทที่ผู้ใช้สนใจมากที่สุดในเดือนนี\n"))
        #     keb_ro = []
        #     count = 1
        #     for c in range(len(name)):
        #         tmp = name[c][0].replace("('", "").replace("',)", "")
        #         tmp = "อันดับที่ " + str(count) + ". " + tmp
        #         keb_ro.append(tmp)
        #         count += 1
        #     # print(name)
        #     # print(feq)
        #     line_bot_api.push_message(
        #         event.source.user_id,
        #         TextSendMessage(text="บริษัทที่ผู้ใช้สนใจมากที่สุดในเดือนนี้\n" + '\n'.join(keb_ro)))
        #
        #     mode_zeroo = 0
        #     try:
        #         query5 = """delete from mode_user where id_user = '""" + event.source.user_id + "'"
        #         cursor.execute(query5)
        #         print(query5)
        #         print("insert table mode_user")
        #         query44 = (
        #             '''insert into mode_user(id_user,mode) values ('%s','%s')''' % (event.source.user_id, mode_zeroo))
        #         cursor.execute(query44)
        #     except:
        #         print("error insert table mode_user")
        #
        # if mode == '3':
        #     head_contect = []
        #     print("mode 3")
        #     cursor.execute('''select id_fpo_count from count_fpo where current_date - date_topicname < 30 ''')
        #     data_company_fpo = cursor.fetchall()
        #     # print(data_company_fpo)
        #     ar_company_fpo = set(data_company_fpo)
        #     # print(ar_company_fpo)
        #     ar = []
        #     for i in ar_company_fpo:
        #         count_company_fpo = data_company_fpo.count(i)
        #         ar.append([i, count_company_fpo])
        #         print(count_company_fpo)
        #
        #     ar = sorted(ar, key=lambda x: x[1], reverse=True)[:5]
        #     name, feq = zip(*ar)
        #
        #     keb_ro = []
        #     for c in range(len(name)):
        #         tmp = name[c][0]
        #         keb_ro.append(tmp)
        #
        #     line_bot_api.push_message(
        #         event.source.user_id,
        #         TextSendMessage(text="เรื่องร้องเรียนที่ผู้ใช้สนใจมากที่สุดในเดือนนี\n"))
        #     data_fpo_check2 = []
        #     for c in keb_ro:
        #         print("c = " + str(c))
        #         q = (
        #         "Select topic,content_topic,doyheadsub,date_topic,feedback,doymaster,feedback_date From fpo2 where id_fpo=" + str(
        #             c) + ";")
        #         cursor.execute(q)
        #         datafpo = cursor.fetchall()
        #         # datafpo[0][0] = str(datafpo[0][0])
        #         topic = datafpo[0][0][:200]
        #
        #         t = cutkumkean(datafpo[0][1])[:4]
        #         t3 = "วันที่ร้องเรียน :" + str(datafpo[0][3])
        #         t4 = cutkumkean(str("ตอบข้อร้องเรียน :" + datafpo[0][4]))
        #         t6 = "วันที่ตอบข้อร้องเรียน :" + str(datafpo[0][6])
        #
        #         data_fpo_check2.append([topic.replace("หัวข้อร้องเรียน:", ""), t])
        #         head_contect.append([topic, t, t3, t4, t6, c])
        #     d = se(2, head_contect, event.source.user_id)
        #     if (len(d) == 0):
        #         line_bot_api.push_message(
        #             event.source.user_id,
        #             TextSendMessage(text="ไม่พบการกระทำผิดเกี่ยวกับข้อมูลที่ท่านได้สอบถาม")
        #         )
        #
        #     elif (len(d) > 5):
        #         for c in range(0, len(d) + 1, 5):
        #             if (c + 5 < len(d)):
        #
        #                 carousel_template_message = TemplateSendMessage(
        #                     alt_text='Carousel template',
        #                     template=CarouselTemplate(
        #                         columns=d[c:c + 5]
        #                     )
        #                 )
        #                 line_bot_api.push_message(event.source.user_id, carousel_template_message)
        #             else:
        #
        #                 carousel_template_message = TemplateSendMessage(
        #                     alt_text='Carousel template',
        #                     template=CarouselTemplate(
        #                         columns=d[c:]
        #                     )
        #                 )
        #                 line_bot_api.push_message(event.source.user_id, carousel_template_message)
        #                 print("send_se if1")
        #
        #
        #     else:
        #         carousel_template_message = TemplateSendMessage(
        #             alt_text='Carousel template',
        #             template=CarouselTemplate(
        #                 columns=d
        #             )
        #         )
        #         line_bot_api.push_message(event.source.user_id, carousel_template_message)
        #         print("send_se else")
        #
        #     mode_zeroo = 0
        #     try:
        #         query5 = """delete from mode_user where id_user = '""" + event.source.user_id + "'"
        #         cursor.execute(query5)
        #         print(query5)
        #         print("insert table mode_user")
        #         query44 = (
        #             '''insert into mode_user(id_user,mode) values ('%s','%s')''' % (event.source.user_id, mode_zeroo))
        #         cursor.execute(query44)
        #     except:
        #         print("error insert table mode_user")


def se(mode,me,uId):
    se = []
    i =1
    for c in me:
        #line_bot_api.push_message(uId, TextSendMessage(text='Hello round:' + str(i) + '/' + str(len(me)+1)))
        i += 1
        tmpHead = str(c[0])[:40] + '...'
        try:
            index_db = str(c[5])
        except:
            index_db = str(c[3])

        #print(type(tmpHead), len(tmpHead), tmpHead)
        o = CarouselColumn(title=' ', text=str(tmpHead),actions=[PostbackTemplateAction(label='ดูข้อมูลทั้งหมด', data=str(mode) + '_' + index_db)])
        se.append(o)
    return se

if __name__ == "__main__":
    app.run()









