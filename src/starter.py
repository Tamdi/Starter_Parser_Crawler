from bottle import get, run, request
import json
from crawler import parse_short_obj, parse_full_obj
from log import get_logger
from db import sqlalchemy_saver, sqlalchemy_getData

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


@get('/saved_news')
def get_saved():
    return json.dumps(sqlalchemy_getData(from_date=None, to_date=None), ensure_ascii=False)


if __name__ == "__main__":
    log = get_logger("starter")
    run(host='0.0.0.0', port=8080)
