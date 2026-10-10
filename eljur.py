import requests
from bs4 import BeautifulSoup
import random
import os
import time

BASE = "https://eljur.gospmr.org"
# logo
logo = r"""
███████╗ ██╗      ██████╗ ██████╗   █████╗  ██████╗ ██╗  ██╗
██╔════╝ ██║     ██╔════╝ ██╔══██╗ ██╔══██╗ ██╔════╝ ██║ ██╔╝
█████╗   ██║     ██║      ██████╔╝ ███████║ ██║      █████═╝ 
██╔══╝   ██║     ██║      ██╔══██╗ ██╔══██║ ██║      ██╔═██╗ 
███████╗ ███████╗╚██████╗ ██║  ██║ ██║  ██║ ╚██████╗ ██║  ██╗
╚══════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═╝  ╚═╝  ╚═════╝ ╚═╝  ╚═╝
"""

login = ""
password = ""

session = requests.Session()


# функция измены ссесии
def ses_update():
    session.headers.update({
        "User-Agent": (
            f"Mozilla/{random.randint(2, 5)}.0 (Linux {random.randint(1, 1000000)}; Android {random.randint(1, 1000000)}); CPH2841) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            f"Chrome/{random.randint(70, 126)}.0.0.0 Mobile Safari/{random.randint(20, 537)}.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.9",
        "Origin": BASE,
        "Referer": f"{BASE}/authorize",
    })


ses_update()


# функция получение html от url
def get_soup(url):
    r = session.get(url)
    r.encoding = "utf-8"
    return BeautifulSoup(r.text, "html.parser")


# функция регистрации элжура в ссесии
def reg(login_val, password_val):
    data = {
        "username": login_val,
        "password": password_val,
        "return_uri": "/",
    }
    try:
        response = session.post(f"{BASE}/ajaxauthorize", data=data)
        if response.json == {'actions': [], 'errors': [{'field': None, 'text': 'Неверный логин или пароль'}],
                             'result': False}:
            return "Неверный логин или пароль"
        elif r""""result":true""" in str(response.text):
            return "ok"
        else:
            return response.text
    except Exception as e:
        return e


# функция создания календаря
def newcal(title="Новое событие", canEdit=True, description="Описание события", calendar_id="1220",
           datetime_start="2026-10-31 09:00:00", datetime_end="2026-10-31 10:00:00", presence="at_will",
           place_type="school", place_value="", status="published"):
    data = {
        "CalendarEvent": {
            "title": title,
            "canEdit": canEdit,
            "description": description,
            "calendar_id": calendar_id,
            "datetime_start": datetime_start,
            "datetime_end": datetime_end,
            "presence": presence,
            "place_type": place_type,
            "place_value": place_value,
            "status": status
        }
    }
    response = session.post(f"{BASE}/journal-calendar-api-action/type.event/action.create", json=data)
    return response.text


# функция отправки сообщения
def go_mess(id_in, description, tema, csrf):
    data = {
        "subject": tema,
        "message": description,
        "receivers": id_in,
        "vfiles": [],
        "csrf": csrf,
        "resources": ""
    }
    response = session.post(f"{BASE}/journal-messages-send-action", json=data)
    print(response.text)


# функция получение календаря по его счёту
def razved_cal(iddd):
    return session.get(
        f"https://eljur.gospmr.org/journal-calendar-api-action/type.event/action.one?id={iddd}").text.encode(
        'utf-8').decode('unicode_escape')


# функция интерфейса для введения логина и пароля
def login_password():
    global login, password
    while True:
        print(logo)
        print("\n                  ВВЕДИТЕ ЛОГИН\n")
        login = input("login>>  ")
        password = input("password>>  ")
        pp = reg(login, password)
        if pp == "ok":
            break
        elif pp == "Неверный логин или пароль":
            print("\n  Неверный логин или пароль")
            time.sleep(2)
            os.system("clear")
            continue
        else:
            print(f"\n  ошибка  {pp}")
        time.sleep(2)
        os.system("clear")
    os.system("clear")
    menu()


# функция интерфейса меню (не доделана)
def menu():
    while True:
        print(logo)
        print("\n                  ВВЕДИТЕ НОМЕР ДЕЙСТВИЯ\n\n  1)message boom\n  2)scan calendar\n  3)calendar boom")
        go = input(" >>   ")
        if go == "1":
            os.system("clear")
            message_go()
        elif go == "2":
            os.system("clear")
            break
        else:
            print(f"\n         ВВЕДИТЕ КОРЕКТНЫЙ НОМЕР")
            time.sleep(2)
            os.system("clear")
            continue


# функция интерфейса для отправки сообщения
def message_go():
    print(logo)
    print("\n                  Вы выбрали message boom\n")
    n = int(input("n>>  "))
    id = {}
    for i in range(1, n + 1):
        id[str(n)] = str(input(f"id_{n}>>  "))
    pp = reg(login, password)
    desc = input("description>>  ")
    tit = input("title>>  ")
    nn = int(input("N>>  "))
    dd = get_soup(f"{BASE}/journal-messages-compose-action")
    csrf = dd.find("input", id="csrf")["value"]
    for i in range(1, nn + 1):
        for i in id:
            print(go_mess([ id[str(i)] ], desc, tit, csrf))
    time.sleep(2)
    os.system("clear")
    menu()


# вызов функции интерфейса, начало работы
login_password()
