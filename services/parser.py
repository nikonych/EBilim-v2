import time
import urllib
import prettytable as pt
import requests
from bs4 import BeautifulSoup

from services.dbhandler import get_userx

url = ('https://lms.inai.kg/Account/Login')
s_url = ('https://lms.inai.kg/')
transkript2 = ('https://lms.inai.kg/studentjurnal/semester?idSem=3&idGroup=17')
subjects = ('https://lms.inai.kg/studentjurnal/discipline')
schedule = ('https://lms.inai.kg/Scheduleteacher/group')


# with requests.session() as s:
#     s.post(url, data=payload)
#     r = s.get(s_url)
#     soup = BeautifulSoup(r.content, 'html.parser')
#     for span in soup.findAll('tr'):
#         # print(span.text)
#         for a in span.findAll('a'):
#             print(a.text)
#         print(span.find('span').text)
#     # print(soup.find_all("span"))
#     print()
#     for a in soup.find_all('dd'):
#         print(a.text)
#     print(soup.findAll('h2')[1].text)
#     # print(soup)

def check_ebilim(login, password):
    payload = {
        'Login': login,
        'Password': password,
        'LangID': '1049'
    }
    with requests.session() as s:
        s.post(url, data=payload)
        r = s.get(s_url)
        soup = BeautifulSoup(r.content, 'html.parser')
        if(soup.find('button').text == "Войти в систему "):
            return False
        else:

            return True

def get_transkript2(id):
    user = get_userx(user_id=id)

    payload = {
        'Login': user['inai_login'],
        'Password': user['inai_password'],
        'LangID': '1049'
    }
    with requests.session() as s:
        s.post(url, data=payload)
        r = s.get(transkript2)
        soup = BeautifulSoup(r.content, 'html.parser')
        info = {}
        for span in soup.findAll('tr'):
            text = []
            for a in span.findAll('a'):
                text.append(a.text)
                # print(a.text)
            if tuple(text) not in info.keys():
                if(span.find('span') is None):
                    info[tuple(text)] = '0,0'
                else:
                    info[tuple(text)] = span.find('span').text
            # print(span.find('span').text)
            # print(soup.find_all("span"))
        # print(info)
        # for a in soup.find_all('dd'):
        #     print(a.text)
        # print(soup.findAll('h2')[1].text)
        return info


def get_subjects(id):
    log_pas = main.db.getLogPas(id)
    payload = {
        'Login': log_pas[0],
        'Password': log_pas[1],
        'LangID': '1049'
    }
    with requests.session() as s:
        s.post(url, data=payload)
        r = s.get(subjects)
        soup = BeautifulSoup(r.content, 'html.parser')
        info = {}
        for desc in soup.findAll('div', class_="product-desc"):
            name = desc.find('a', class_="product-name").text
            print(name.strip())
            price = desc.find('span', class_="product-price").text
            div = desc.find('div', class_="m-t text-righ")
            link = div.find('a', href=True)['href']
            info[name.strip() + " " + price.strip()] = link

        return info


def get_subject(id, link):
    log_pas = main.db.getLogPas(id)
    payload = {
        'Login': log_pas[0],
        'Password': log_pas[1],
        'LangID': '1049'
    }
    with requests.session() as s:
        s.post(url, data=payload)
        urlsub = ('https://lms.inai.kg' + link)

        r = s.get(urlsub)
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find_all('table')
        print(table)

        return soup.find_all('table', class_='table table-bordered dataTable no-footer')


def get_shedule(id):
    log_pas = main.db.getLogPas(id)
    payload = {
        'Login': log_pas[0],
        'Password': log_pas[1],
        'LangID': '1049'
    }
    with requests.session() as s:
        s.post(url, data=payload)
        r = s.get(schedule)
        soup = BeautifulSoup(r.content, 'html.parser')
        # table1 = soup.findAll('tr', class_=lambda x: x != 'transparent')
        table1 = soup.find('div', {"id": "tab-3"})
        table2 = table1.find_all('tr', class_=lambda x: x != 'transparent')
        # print(table2)
        # print(table1)
        days = {'Пн': [], 'Вт': [], 'Ср': [], 'Чт': [], 'Пт': []}
        for data in table2:
            print(data)
        print(days)

        table = pt.PrettyTable(['Время занятия', 'Дисциплина', 'Вид занятия', 'Аудитория'])
        # print(table1)




