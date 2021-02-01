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

with open(os.path.join( os.path.realpath('.'),"studentsTesting.json")) as f:
    students = json.load(f)
  
#print(data)

# students = [
#             {"htn":"19fh1a0546", 'email': 'naresh.khatri2345@gmail.com'},
#             {"htn":"19fh1a0548", 'email': 'natesh.khatri31@gmail.com'},
#             {"htn":"19fh1a0549", 'email': 'rosisbetterthanpubg@gmail.com'},
#             # {"htn":"19fh1a0515", 'email': 'sukeerthana199@gmail.com'},
#             # {"htn":"19fh1a0530", 'email': 'fasiahmed65@gmail.com'},
#             # {'htn':"19fh1a0549", 'email':'perumalaachyuthkumar2000@gmail.com'},
# ]
# print(students)

def extract_int(text):
    num=''
    for char in text:
        if char.isdigit():
            num+=char
    return int(num)

def result_polling():
    #while True:
        request = Request('https://jntuaresults.ac.in/')
        uClient = urlopen(request)
        page_html = uClient.read()
        uClient.close()

        page_soup = BeautifulSoup(page_html,"html.parser")

        tables = page_soup.find('table', attrs={"class": "ui table segment"})

        tr = tables.findAll("tr")
        first_td = tr[1]

        content = first_td.find("a")

        
        if "R17" in content.text:
            print(content.text)
            print(f'Result ID acquired - {extract_int(content["href"])}')
            index = 0
            for student in students:
                get_result(extract_int(content['href']), student["htn"],student["email"], index)
                index+=1

        else:
            print("not released yet!")

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
    url = f'https://jntuaresults.ac.in/results/res.php?ht={htn}&id={oldresultID}&accessToken={token}'

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
    #if students[index]["sent"] == False:
    if True:
        result = str(result_table)
        msg= MIMEMultipart('alternative')
        
        # length_list = [len(element) for row in result_table for element in row]
        # column_width = max(length_list)
        # for row in result_table:
        #     row = "".join(element.ljust(column_width + 2) for element in row)
        #     msg+=row + '\n'
        # print(msg)

        #result.replace(":","")
        #result=result.split(":")
        #result= "".join(element for element in result)

        mime_text = MIMEText(result,'html')

        msg.attach(mime_text)
        msg['Subject'] = 'subscribe to HotChaddi on youtube 🤣💯👌'

        server = smtplib.SMTP_SSL("smtp.gmail.com:465")
        server.login("subscribe.to.hotchaddi.on.yt@gmail.com", "poojapooja1")
        # server.sendmail(
        # "rosisgreaterthanpubg@gmail.com",
        # email,
        # msg.as_string()
        # )
        #index =[i for i in students if i['email'] == email]
        #print(index)
        students[index]["sent"] = True
        studentsJson = open(os.path.join( os.path.realpath('.'),"studentsTesting.json"), "w")
        json.dump(students, studentsJson)
        studentsJson.close()
        print(f'mail sent to {email}\n')

        server.quit()
    else:
        print(f"Result already sent to {email}\n")

        
result_polling()
#result_polling.apply_async()





