import json

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
    # for r in result:
    #     print(r)


def sqlalchemy_getData_by_date(news_list):
    date_input = input()
    engine = create_engine('postgresql://postgres:1@localhost:5432/postgres', echo=True)
    meta = MetaData()
    meta.create_all(engine)
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
        select = news_model.select().where(news_model.c.date == date_input)

        conn = engine.connect()
        res = conn.execute(select)


def sqlalchemy_deleteData_by_date(news_list):
    date_input = input()
    engine = create_engine('postgresql://postgres:1@localhost:5432/postgres', echo=True)
    meta = MetaData()
    meta.create_all(engine)
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
        delete = news_model.delete().where(news_model.c.date == date_input)
        conn = engine.connect()
        res = conn.execute(delete)


def sqlalchemy_deleteAllData():
    engine = create_engine('postgresql://postgres:1@localhost:5432/postgres', echo=True)
    meta = MetaData()
    meta.create_all(engine)
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
    delete = news_model.delete()
    conn = engine.connect()
    res = conn.execute(delete)
