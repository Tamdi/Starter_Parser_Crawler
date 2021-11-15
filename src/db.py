import json
import sqlalchemy.exc
from sqlalchemy import create_engine, MetaData, Table, Column, DateTime, String
from config import TABLE_NAME, POSTGRES_URL
from hashing import calc_hash


def sqlalchemy_saver(news_list):
    engine = create_engine(POSTGRES_URL, echo=True)
    meta = MetaData()
    news_model = Table(
        TABLE_NAME, meta,
        Column('id', String, primary_key=True),
        Column('date', DateTime),
        Column('title', String),
        Column('text', String),
        Column('url', String),
        Column('img_url', String)
    )
    meta.create_all(engine)
    news_list = json.loads(news_list)
    for new in news_list:
        result = news_model.insert().values(
            id=calc_hash(new['title']+new['url']),
            date=new['date'],
            title=new['title'],
            text=new['text'],
            url=new['url'],
            img_url=new['img_url']
        )
        conn = engine.connect()
    try:
        res = conn.execute(result)
    except sqlalchemy.exc.IntegrityError:
        print("this data already exists")


def sqlalchemy_getData(from_date=None, to_date=None):
    engine = create_engine(POSTGRES_URL, echo=True)
    meta = MetaData()
    meta.create_all(engine)
    if from_date:
        result = engine.execute(f"SELECT * FROM {TABLE_NAME} WHERE date BETWEEN {from_date} AND {to_date}")
    else:
        result = engine.execute(f"SELECT * FROM {TABLE_NAME}")
    res = []
    for i in result:
        data = {
            'id': i[0],
            'date': i[1].strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'title': i[2],
            'text': i[3],
            'url': i[4],
            'img_url': i[5]
        }
        res.append(data)
    return res
