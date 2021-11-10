from datetime import datetime
from dateparser import parse
from bs4 import BeautifulSoup
import requests
import psycopg2
from psycopg2 import OperationalError
from psycopg2 import Error


# def create_database(connection, query):
#     connection.autocommit = True
#     cursor = connection.cursor()
#     try:
#         cursor.execute(query)
#         print("Query executed successfully")
#     except OperationalError as e:
#         print(f"The error '{e}' occurred")
#
#
# def create_connection(db_name, db_user, db_password, db_host, db_port):
#     connection = None
#     try:
#         connection = psycopg2.connect(
#             database=db_name,
#             user=db_user,
#             password=db_password,
#             host=db_host,
#             port=db_port,
#         )
#         print("Connection to PostgreSQL DB successful")
#     except OperationalError as e:
#         print(f"The error '{e}' occurred")
#     return connection
#
#
# def execute_query(connection, query):
#     cursor = connection.cursor()
#     try:
#         cursor.execute(query)
#         connection.commit()
#         print("Query executed successfully")
#     except Error as e:
#         print(f"The error '{e}' occurred")


def parse_short_obj(params):
    response = requests.get(
        "https://www.zakon.kz/",
        timeout=10,
    )
    if response.ok:
        response_content = response.content
        soup = BeautifulSoup(response_content, 'html.parser')
        div = soup.find("div", {"class": "lastnews"})
        data = []
        for _a in div.find_all('a'):
            time = _a.text.strip()[0:5]
            title = _a.text.replace(time, '').strip()
            data.append(
                {
                    "time": time,
                    "title": title,
                }
            )
        if params:
            return data[0:int(params)]
        return data


def parse_full_obj(params):
    response = requests.get(
        "https://www.zakon.kz/",
        timeout=10,
    )
    if response.ok:
        response_content = response.content
        soup = BeautifulSoup(response_content, 'html.parser')
        div = soup.find("div", {"class": "lastnews"})
        data = []
        for _i, _a in enumerate(div.find_all('a')):
            if params:
                if str(_i) == params:
                    break
            url = _a.get('href')
            if (url[0] == "/") and (url[1] != "/"):
                url = "".join(("https://www.zakon.kz", url))
            response_new = requests.get(
                url=url,
                timeout=10,
            )
            response_content_new = response_new.content
            soup_new = BeautifulSoup(response_content_new, 'html.parser')

            # image_url
            div_img = soup_new.find("div", {"class": "newspic"})
            if not div_img:
                continue
            image_link = div_img.findAll('img')[0]['src']
            if '//' in image_link:
                image_link = "".join(("https:", image_link))

            # title
            div_head = soup_new.find("div", {"class": "fullhead"})
            head = div_head.findAll('h1')[0].text.strip()

            # text
            full_text = soup_new.find("div", {"class": "newscont"}).text.strip()

            # date
            div_date = soup_new.find("div", {"class": "extrainfo"})
            date = div_date.span
            date_field=str(date)
            date_text = date_field.replace("<span>", '').replace("</span>", '').replace("ноября", 'November')
            dt = parse(date_text)
            new_date = datetime.strftime(dt, '%d %m %Y, %H:%M')

            data.append(
                {
                    "url": url,
                    "title": head,
                    "text": full_text,
                    "img_url": image_link,
                    "date": new_date,
                }
            )
        return data
