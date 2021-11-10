from bottle import get, run, request
import json
from crawler import parse_short_obj, parse_full_obj
from log import get_logger
# from crawler import create_connection, create_database, execute_query
from db import sqlalchemy_saver

@get('/short_news')
def return_short_news():
    log.info("Sending request from zakon.kz general short info")
    count = request.params.get('count', [0])[0]# count =
    log.info("Getting request from zakon.kz general short info")
    return json.dumps(parse_short_obj(count), ensure_ascii=False)


@get('/full_news')
def return_full_news():
    log.info("Sending request from zakon.kz general full info")
    count = request.params.get('count', [0])[0] #count =
    log.info("Getting request from zakon.kz general full info")
    result = json.dumps(parse_full_obj(count), ensure_ascii=False)
    sqlalchemy_saver(result)
    return result
#
# connection = create_connection(
#     "crawler_full_news", "postgres", "1", "127.0.0.1", "5432"
# )
#
#
# create_full_news_table = """
# CREATE TABLE IF NOT EXISTS full_news(
#     id INT PRIMARY KEY,
#     url VARCHAR,
#     title VARCHAR,
#     text VARCHAR,
#     img_url VARCHAR,
#     date_time DATE
# )
# """
# execute_query(connection, create_full_news_table)
#

if __name__ == "__main__":
    # get_logger("Starting service")
    log = get_logger("starter")
    run(host='0.0.0.0', port=8080)
