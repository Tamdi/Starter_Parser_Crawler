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
        print(new['date'])
        result = news_model.insert().values(
            date=new['date'],
            title=new['title'],
            text=new['text'],
            url=new['url'],
            img_url=new['img_url']
        )
        conn = engine.connect()
        res = conn.execute(result)


# def saver(data: list):
#     connection = create_connection(
#         "postgres", "postgres", "1", "127.0.0.1", "5432"
#     )
#
#     create_database_query = "CREATE DATABASE [IF NOT EXISTS] crawler_full_news"
#
#     create_database(connection, create_database_query)
#
#     connection = create_connection(
#         "crawler_full_news", "postgres", "1", "127.0.0.1", "5432"
#     )
#
#
#     create_full_news_table = """
#     CREATE TABLE IF NOT EXISTS full_news(
#         id INT PRIMARY KEY,
#         url VARCHAR,
#         title VARCHAR,
#         text VARCHAR,
#         img_url VARCHAR,
#         date_time DATE
#     )
#     """
#     execute_query(connection, create_full_news_table)
