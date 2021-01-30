from bs4 import BeautifulSoup
import bs4
from urllib.request import urlopen, Request
import re

request = Request('https://jntuaresults.ac.in/')
uClient = urlopen(request)
page_html = uClient.read()
uClient.close()

page_soup = BeautifulSoup(page_html,"html.parser")

tables = page_soup.find('table', attrs={"class": "ui table segment"})

tr = tables.findAll("tr")
first_td = tr[1]

content = first_td.find("a")

if "R15" in content.text:
    print(content.text)
    print(content["href"])