from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import bs4
import csv
import json
import os

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


with open(os.path.join( "/home/code/resultsNotifier","students.json")) as f:
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

        if not r19rows:
            print('not yet released')
            for student in students:
                sendNotif(student["email"])

def sendNotif(email):
    msg= MIMEMultipart('alternative')

    html_tamplete = '''<body style='background: yellow'>
<div style="background:yellow;display:flex; justify-content:center; align-items:center; border-radius: 25px;">
<div class='card' style="display:block;  box-shadow: 0 10px 30px -6px black;
border-radius:20px;
background:#7e5594;
  width: 400px;
  height: 400px;
  padding: 0px 10px;">
<div style="text-align:center;font-size:130px">
😔
</div>
<hr style="width:60%; border: 1px solid yellow">
<h1>
Results are not out yet!
</h1>
<li>
If you'd like to refer this mail service to your friends then reply to 
this mail providing their Hall Ticket Numbers along with their emails.
</li>
<li>
  To unsubscribe from this service, reply to this mail saying so.
</li>
<hr style="width:40%;border: 1px solid yellow;">

<div display:block>If you like this work then give a star on github <a style="color:yellow" href='https://github.com/Naresh-Khatri/resultsNotifier'>here</a></div>

</div>
</div>
</body>'''
    
    mime_text = MIMEText(html_tamplete,'html')

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
    #students[index]["sent"] = True
    #studentsJson = open(os.path.join( os.path.realpath('.'),"studentsTesting.json"), "w")
    #json.dump(students, studentsJson)
    #studentsJson.close()
    print(f'mail sent to {email}\n')

    server.quit()

result_polling()
