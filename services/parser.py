import time
import urllib
import prettytable as pt
import requests
from bs4 import BeautifulSoup
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from services.dbhandler import get_userx, get_settings

url = ('https://lms.inai.kg/Account/Login')
s_url = ('https://lms.inai.kg/')
main_url = 'https://lms.inai.kg/'
subjects = ('https://lms.inai.kg/studentjurnal/discipline')
schedule = ('https://lms.inai.kg/Scheduleteacher/group')
payment = ('https://lms.inai.kg/payment/addpayment')

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

import re

MATCH_ALL = r'.*'


def like(string):
    """
    Return a compiled regular expression that matches the given
    string with any prefix and postfix, e.g. if string = "hello",
    the returned regex matches r".*hello.*"
    """
    string_ = string
    if not isinstance(string_, str):
        string_ = str(string_)
    regex = MATCH_ALL + re.escape(string_) + MATCH_ALL
    return re.compile(regex, flags=re.DOTALL)

def find_by_text(soup, text, tag, **kwargs):
    """
    Find the tag in soup that matches all provided kwargs, and contains the
    text.

    If no match is found, return None.
    If more than one match is found, raise ValueError.
    """
    elements = soup.find_all(tag, **kwargs)
    matches = []
    for element in elements:
        if element.find(text=like(text)):
            matches.append(element)
    if len(matches) > 1:
        raise ValueError("Too many matches:\n" + "\n".join(matches))
    elif len(matches) == 0:
        return None
    else:
        return matches[0]


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
        main = s.post(url, data=payload)
        soup = BeautifulSoup(main.content, 'html.parser')
        # print(soup.find_all('a', href=True, target="_blank"))
        r = s.get(main_url[:-1] + find_by_text(soup, "3",'a', href=True, target="_blank")['href'])
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
            price = desc.find('span', class_="product-price").text
            div = desc.find('div', class_="m-t text-righ")
            link = div.find('a', href=True)['href']
            info[name.strip() + " " + price.strip()] = link
        print(info)
        return info


def get_subject(id, link):
    user = get_userx(user_id=id)

    payload = {
        'Login': user['inai_login'],
        'Password': user['inai_password'],
        'LangID': '1049'
    }
    with requests.session() as s:
        s.post(url, data=payload)
        urlsub = ('https://lms.inai.kg' + link)
        option = Options()
        option.add_argument("--disable-infobars")
        browser = webdriver.Chrome('data/chromedriver', chrome_options=option)
        browser.get(url)
        login = browser.find_element_by_id("Login").send_keys(user['inai_login'])
        password = browser.find_element_by_id("Password").send_keys(user['inai_password'])
        submit = browser.find_element_by_xpath("//button[@type='submit']").click()
        r = browser.get(urlsub)
        html = browser.page_source
        # r = s.get(urlsub)
        print(html)
        soup = BeautifulSoup(html, 'html.parser')
        td = soup.find_all('td')
        info = [i.text for i in td]
        print(info)

        browser.close()


        return info


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

def get_user_info(id):
    user = get_userx(user_id=id)
    week_num = get_settings()['week_num']

    payload = {
        'Login': user['inai_login'],
        'Password': user['inai_password'],
        'LangID': '1049'
    }
    with requests.session() as s:
        info = []
        s.post(url, data=payload)
        r = s.get(payment)
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find("table", class_="table table-striped mb0 font13")
        name = table.find('a', {"target": "_blank"}).text.replace(" ", "").replace("\r", "").replace("\n","")
        full_name = re.findall('[А-Я][^А-Я]*', name)
        info.append(full_name)
        soup_money = BeautifulSoup(s.get(s_url).content, 'html.parser')
        money = soup_money.find("h1", class_="no-margins").text
        info.append(money)
        more_info = table.find_all("td")
        [info.append(i.text.replace("\r", "").replace("\n","").strip()) for i in more_info[1:]]
    return info

