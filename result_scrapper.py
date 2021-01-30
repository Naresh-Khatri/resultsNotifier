from bs4 import BeautifulSoup
import bs4
import csv
from urllib.request import urlopen, Request


filename = 'resultsSup'
cookie = "_ga=GA1.3.1774447704.1597145128; _gid=GA1.3.505915151.1608124559; PHPSESSID=nilfesqjlr1jo8mpi8k1ecdu17"

def getToken():

    url = 'https://jntuaresults.ac.in/view-results-56736380.html'
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

for i in range(1,64):

    if len(str(i)) == 1:
        htn = '19fh1a050' + str(i)
  #  elif len(str(i)) == 3:
#     htn = '19fh1a05a' + str(100-i)
    else:
        htn = '19fh1a05' + str(i)

    url = 'https://jntuaresults.ac.in/results/res.php?ht=' + htn + '&id=56736322&accessToken=' + getToken()

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
        print(name)
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

        print(data)
