from bs4 import BeautifulSoup
import bs4
from urllib.request import urlopen, Request


cookie = "_ga=GA1.3.1774447704.1597145128; _gid=GA1.3.505915151.1608124559; PHPSESSID=nilfesqjlr1jo8mpi8k1ecdu17"


def extract_int(text):
    num=''
    for char in text:
        if char.isdigit():
            num+=char
    return int(num)

def result_polling():
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
        print(extract_int(content["href"]))
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
    access_token = ''
    for char in list(token_text):
        if char.isdigit():
            access_token += char

    print('acess token acquired -  ' +  access_token)
    return access_token




result_polling()





