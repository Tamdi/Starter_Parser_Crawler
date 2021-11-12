import json
from datetime import datetime
from dateparser import parse
from bs4 import BeautifulSoup
import requests
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Date, String


def sqlalchemy_saver(news_list):
    engine = create_engine('postgresql://postgres:1@localhost:5432/postgres', echo=True)
    meta = MetaData()
    news_model = Table(
        'new', meta,
        Column('id', Integer, primary_key=True),
        Column('date', Date),
        Column('title', String),
        Column('text', String),
        Column('url', String),
        Column('img_url', String)
    )
    meta.create_all(engine)
    news_list = json.loads(news_list)
    for new in news_list:
        result = news_model.insert().values(
            date=new['date'],
            title=new['title'],
            text=new['text'],
            url=new['url'],
            img_url=new['img_url']
        )
        conn = engine.connect()
        res = conn.execute(result)


def sqlalchemy_getAllData():
    engine = create_engine('postgresql://postgres:1@localhost:5432/postgres', echo=True)
    meta = MetaData()
    meta.create_all(engine)
    result = engine.execute("SELECT * FROM new")
    for r in result:
        print(r)

# def parse_db_full_obj_by_date(params):
#     engine = create_engine('postgresql://postgres:1@localhost:5432/postgres', echo=True)
#     meta = MetaData()
#     meta.create_all(engine)
#     result = engine.execute("SELECT * FROM new")
#     if result.ok:
#         response_content = result.content
#         soup = BeautifulSoup(response_content, 'html.parser')
#         div = soup.find("div", {"class": "lastnews"})
#         data = []
#         for _i, _a in enumerate(div.find_all('a')):
#             if params:
#                 if str(_i) == params:
#                     break
#             url = _a.get('href')
#             if (url[0] == "/") and (url[1] != "/"):
#                 url = "".join(("https://www.zakon.kz", url))
#             response_new = requests.get(
#                 url=url,
#                 timeout=10,
#             )
#             response_content_new = response_new.content
#             soup_new = BeautifulSoup(response_content_new, 'html.parser')
#
#             # image_url
#             div_img = soup_new.find("div", {"class": "newspic"})
#             if not div_img:
#                 continue
#             image_link = div_img.findAll('img')[0]['src']
#             if '//' in image_link:
#                 image_link = "".join(("https:", image_link))
#
#             # title
#             div_head = soup_new.find("div", {"class": "fullhead"})
#             head = div_head.findAll('h1')[0].text.strip()
#
#             # text
#             full_text = soup_new.find("div", {"class": "newscont"}).text.strip()
#
#             # date
#             div_date = soup_new.find("div", {"class": "extrainfo"})
#             date = div_date.span
#             date_field=str(date)
#             date_text = date_field.replace("<span>", '').replace("</span>", '').replace("ноября", 'November')
#             dt = parse(date_text)
#             new_date = datetime.strftime(dt, '%d %m %Y, %H:%M')
#
#             data.append(
#                 {
#                     "url": url,
#                     "title": head,
#                     "text": full_text,
#                     "img_url": image_link,
#                     "date": new_date,
#                 }
#             )
#         return data


