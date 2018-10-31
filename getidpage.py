import psycopg2 as psql
from lxml import html
import re
from urllib.request import Request, urlopen
import sched, time

def sub_link(str):
    # pattern = re.compile('petitionID=+[a-zA-Z0-9&=_]*&')
    out = re.search('petitionID=(.+?)&',string=str).group(1)
    print(out)
    return out

user_agent = 'Maxthon/5.1.0.4000'
headers = { 'User-Agent' : user_agent }

def main():
    testja = []

    for c in range(50):
        url = "http://www.fpo.go.th/FPO/index2.php?mod=Petition&file=index&categoryID=CAT0000079&Page="+str(c+1)
        print(c,url)
        req = Request(url=url, headers=headers)

        with urlopen(req) as response:
            the_page = response.read()
            #print("page = ",the_page)
            # unicode_str = the_page.decode("UTF-8")
            tree = html.fromstring(the_page)

        # q_text = tree.xpath("//table[@class='detail']//a/font")
        q_link = tree.xpath("//table[@class='detail']//a/@href")

        print(len(q_link))
        for i in range(len(q_link)):
            tmp = q_link[i]
            id_page_fpo = sub_link(str(tmp))
            testja.append(id_page_fpo)
            # print(tmp, testja[i])
    out = ""
    for i in testja:
        out+= i+'\n'
    file = open(r"C:\Users\User\protected-shore-75514\id_page_fpo.txt", "w")
    file.write(out)

def job():
    main()
    sched.schedule.every().day.at("00:05").do(job)
    while True:
        sched.schedule.run_pending()
    time.sleep(1)
