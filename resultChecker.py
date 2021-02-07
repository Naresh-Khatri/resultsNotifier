from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import bs4
import csv
import json
import os

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


cookie = "_ga=GA1.3.1774447704.1597145128; _gid=GA1.3.505915151.1608124559; PHPSESSID=nilfesqjlr1jo8mpi8k1ecdu17"
filename = 'testing'

with open(os.path.join( "/home/code/resultsNotifier","studentsTesting.json")) as f:
    students = json.load(f)

def extract_int(text):
    return "".join([str(char) for char in text if char.isdigit()])

def result_polling():
    #while True:
        request = Request('https://jntuaresults.ac.in/')
        uClient = urlopen(request)
        page_html = uClient.read()
        uClient.close()

        page_soup = BeautifulSoup(page_html,"html.parser")

        tables = page_soup.find('table', attrs={"class": "ui table segment"})

        tr = tables.findAll("tr")
        top5rows = tr[1:10]
        r19rows= [row.find("a") for row in top5rows if 'B.Tech' and 'R19' in row.find('a').text]
        print(r19rows)
        #print(r19rows[0])

        #content = first_td.find("a")

        if r19rows:
            first_td = r19rows[0]
            print(first_td.text)
            print(f'Result ID acquired - {extract_int(first_td["href"])}')
            #print(extract_int( first_td['href']))
            index = 0
            for student in students:
                get_result(extract_int(first_td['href']), student["htn"],student["email"], index)
                index+=1
            print('All results sent to mails')

        else:
            print("not released yet!")


        # if "R17" in content.text:
        #     print(content.text)
        #     print(f'Result ID acquired - {extract_int(content["href"])}')
        #     index = 0
        #     for student in students:
        #         get_result(extract_int(content['href']), student["htn"],student["email"], index)
        #         index+=1

        # else:
        #     print("not released yet!")

def get_token(resultID):

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
    print('access token acquired -  ' +  access_token)
    return access_token


def get_result(resultsID,htn, email, index):
    token = get_token(resultsID)
    oldresultID = '56736322'
    url = f'https://jntuaresults.ac.in/results/res.php?ht={htn}&id={resultsID}&accessToken={token}'

    request = Request(url)
    request.add_header("Cookie", cookie)

    uClient = urlopen(request)
    page_html = uClient.read()
    uClient.close()

    page_soup = BeautifulSoup(page_html, 'html.parser')

    table = page_soup.find('table')
    if(table):
        rows = table.findAll('tr')

        name_index = str(page_soup).find('Student name')
        table_index = str(page_soup).find('table')
        name = str(page_soup)[name_index + 18:table_index-6]
        print(f"Obtaining {name}'s result...")
        f = open(filename + '.csv', 'a', newline='')
        writer = csv.writer(f)
        writer.writerow([f'*{name} ({htn})'])
        f.close()

        data =[]

        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])


            tup = (cols)
            f = open(filename + '.csv', 'a', newline='')
            writer = csv.writer(f)
            writer.writerow(tup)
            f.close()

        data.pop(0)
        data.pop(-1)

        #print(page_html)
        send_result(page_html, email, index)
        #send_result(data)


def send_result(result_table, email, index):
    # if True:
    if students[index]["sent"] == False:
        result = str(result_table)
        msg= MIMEMultipart('alternative')

        mime_text = MIMEText(result,'html')

        msg.attach(mime_text)
        msg['Subject'] = 'subscribe to HotChaddi on youtube 🤣💯👌'

        server = smtplib.SMTP_SSL("smtp.gmail.com:465")
        server.login("subscribe.to.hotchaddi.on.yt@gmail.com", "poojapooja1")
        server.sendmail(
        "rosisgreaterthanpubg@gmail.com",
        email,
        msg.as_string()
        )
        # index =[i for i in students if i['email'] == email]
        # print(index)
        students[index]["sent"] = True
        studentsJson = open(os.path.join( os.path.realpath('.'),"students.json"), "w")
        json.dump(students, studentsJson)
        studentsJson.close()
        print(f'mail sent to {email}\n')

        server.quit()
    else:
        print(f"Result already sent to {email}\n")

#print(extract_int("as1dfff2f34sdf5r6"))
result_polling()
#result_polling.apply_async()
