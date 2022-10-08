import time
import urllib
import prettytable as pt
import requests
from bs4 import BeautifulSoup

from services.dbhandler import get_userx, get_settings

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
    user = get_userx(user_id=id)

    payload = {
        'Login': user['inai_login'],
        'Password': user['inai_password'],
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
    user = get_userx(user_id=id)
    week_num = get_settings()['week_num']

    payload = {
        'Login': user['inai_login'],
        'Password': user['inai_password'],
        'LangID': '1049'
    }
    with requests.session() as s:
        s.post(url, data=payload)
        r = s.get(schedule)
        soup = BeautifulSoup(r.content, 'html.parser')
        # print(soup.findAll('h4'))
        table1 = soup.find('div', attrs={"id": f"tab-{week_num}"})
        table2 = table1.find_all('tr', class_=lambda x: x != 'transparent')
        week1 = table1.findAll("div", class_='vertical rotate')
        week = [i.text for i in week1]
        days = {}
        for day in week:
            l = table1.find_all('tr', {"data-day": f"{day[4:]}"}, class_=lambda x: x != 'transparent')
            unter0 = []
            for i in l:
                unter = []
                unter.append(i.find('td', class_="time-column").text.replace(" ", "").replace("\r", "").replace('\n', ''))
                unter2 = i.find_all('td', class_="text-center")
                for j in range(1, len(unter2)):
                    unter.append(unter2[j].text.replace('\n', ''))
                unter0.append(unter)
            days[day] = unter0

        # days = {'Пн': [], 'Вт': [], 'Ср': [], 'Чт': [], 'Пт': []}
        # for data in table2:
        #     print(data)
        # print(days)

        return days




