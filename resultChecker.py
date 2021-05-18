from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import bs4
import csv
import json
import os

import time

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


cookie = "PHPSESSID=sdfds"

# with open(os.path.join(os.getcwd() ,"students.json")) as f:
with open(os.path.join(os.getcwd() ,"students.json")) as f:
    students = json.load(f)

def extract_int(text):
    return "".join([str(char) for char in text if char.isdigit()])


def get_sgpa(table):

    g_to_gp ={'s':10,'a':9,'b':8,'c':7,'d':6,'e':5,'f':0,'ab':0}    

    ob_cred = 0
    tot_cred = 21.5
    ci, gi = 0, 0

    table_rows = table.findAll('tr')
    for row in table_rows:
        cols = row.findAll('td')
        foo = []
        for col in cols:
            foo.append(col.text)
        if len(foo) > 0:
            ci = float(foo[-1])
            gi = g_to_gp[foo[-2].lower()]
            ob_cred += ci*gi
    print(f'SGPA = {round(ob_cred/tot_cred,2)}')
    try:
        return round(ob_cred/tot_cred,2)
    except :
        return round(ob_cred/tot_cred,2)


def get_token(resultID):
    start_time = time.time()
    url = f'https://jntuaresults.ac.in/view-results-{resultID}.html'
    request = Request(url)
    request.add_header("Cookie", cookie)

    uClient = urlopen(request)
    page_html = uClient.read()
    uClient.close()

    page_soup = str(BeautifulSoup(page_html, 'html.parser'))
    start_index = int(page_soup.find('accessToken'))

    token_text = page_soup[start_index: start_index+30]

    access_token = "".join([str(char) for char in token_text if char.isdigit()])
    print(f'access token acquired -  {access_token} in {time.time() - start_time}s\n' )
    return access_token


def get_result(resultsID, token, htn, email, index):
    if students[index]['sent']:
        print(f"Result already sent to {email}")
        return
    
    url = f'https://jntuaresults.ac.in/results/res.php?ht={htn}&id={resultsID}&accessToken={token}'

    request = Request(url)
    request.add_header("Cookie", cookie)

    uClient = urlopen(request)
    page_html = uClient.read()
    uClient.close()

    page_soup = BeautifulSoup(page_html, 'html.parser')

    table = page_soup.find('table')
    sgpa = get_sgpa(table)
    if(table):
        rows = table.findAll('tr')

        name_index = str(page_soup).find('Student name')
        table_index = str(page_soup).find('table')
        name = str(page_soup)[name_index + 18: table_index - 6]
        print(f"Obtaining {name}'s result...")
        #print(table)
        style = '''<style>
             @import url('https://fonts.googleapis.com/css2?family=Lato:wght@300;400&family=Roboto+Condensed&family=Roboto+Mono:wght@300;500&display=swap');

            * {
                font-family: 'Lato', sans-serif;
                font-family: 'Roboto Condensed', sans-serif;
                font-family: 'Roboto Mono', monospace;
            }banner {margin: 70px 0px;width: 90vw;
            } .slider {width: 80%;height: 40px;margin: 20px 0px;background: #deacf5;border-radius: 25px;
            }.inner-slide {background: #6237a0;height: 100%;border-radius: 15px 0px 0px 15px;color: white;transition: all 1s;
            }.inner-slide-text {float: right;margin-right:10px;height: 100%;
            }.row {display: flex;flex-direction: row;
            }.col {flex: 50%;flex-direction: column;
            }.justify-center {display: flex;justify-content: center;
            }.ui td,.ui th {padding: 8px;
            }.ui tr:nth-child(odd) {background: #fefefe;
            }.ui tr:hover {background: #deacf5;
            }.ui th {padding-top: 12px;padding-bottom: 12px;text-align: left;background-color: #6237a0;color: white;
            }</style>'''
       
        testhtml = f'''<!DOCTYPE html>
                        <html lang="en">
                            <head>
                                <meta charset="utf-8" />
                                <title>Result</title>
                                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                                {style}
                            </head>
                            <body class='justify-center' style='width:80%>
                                <div class='banner'>
                                    <div class='justify-center'>    
                                        <div>
                                            <div>Hall Ticket No: <b>{htn} </b></div>
                                            <div>Student name: <b> {name} </b></div>
                                            <div>
                                                <div class='slider' style='width:500px'>
                                                    <div class='inner-slide' style='width:{sgpa*10}%'>
                                                        <div class='inner-slide-text' style='display:flex; align-items:center'>
                                                            SGPA: {sgpa}
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                {table}
                                 <th colspan="7" style="text-align:center">
                                    <div>
                                        Know more about your result <a href='https://naresh-khatri.github.io/JNTUA-result-analyser-spa/'> HERE </a>  
                                    </div>
                                        If you want to support this bot service please give us a <a href='https://github.com/Naresh-Khatri/resultsNotifier'>STAR!</a>
                                    </th>
                            </body>
                        </html>
                        '''
        send_result(testhtml, email, index)


def send_result(result_table, email, index):
  
    result = str(result_table)
    msg= MIMEMultipart('alternative')

    mime_text = MIMEText(result,'html')

    msg.attach(mime_text)
    msg['Subject'] = 'subscribe to HotChaddi on youtube 🤣💯👌'

    server = smtplib.SMTP_SSL("smtp.gmail.com:465")
    server.login("jntua.result.notifier.bot@gmail.com", "poojapooja2")
    server.sendmail(
        "rosisgreaterthanpubg@gmail.com",
        email,
        msg.as_string()
    )

    # index =[i for i in students if i['email'] == email]
    # print(index)
    students[index]["sent"] = True
    # studentsJson = open(os.path.join(os.getcwd(),"students.json"), "w")
    studentsJson = open(os.path.join(os.getcwd(),"students.json"), "w")
    json.dump(students, studentsJson)
    studentsJson.close()
    print(f'mail sent to {email}')

    server.quit()
   

def result_polling():
    request = Request('https://jntuaresults.ac.in/')
    uClient = urlopen(request)
    page_html = uClient.read()
    uClient.close()

    page_soup = BeautifulSoup(page_html,"html.parser")

    tables = page_soup.find('table', attrs={"class": "ui table segment"})

    tr = tables.findAll("tr")
    # excluding titles row ie 0
    top5rows = tr[1:10]                                        
    r19rows= [row.find("a") for row in top5rows if 'R19' in row.find('a').text and 'B.Tech' in row.find('a').text]
    try:
        first_td = r19rows[0]
        resultID = extract_int(first_td['href'])
        token = get_token(resultID)
        
        #_old_result_id = 56736424

        index=0
        for student in students:
            start_time = time.time()
            get_result(resultID, token, student["htn"],student["email"], index)
            index+=1
            print(f'Time taken = {time.time() - start_time}\n') 
    except:
        print('Result not out yet :/')

result_polling()