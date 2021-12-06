import grpc
import json
from src.proto.zakon_pb2_grpc import ZakonCrawlerStub
from src.proto.zakon_pb2 import ShortNewsRequest, FullNewsRequest
from bottle import get, run, request
from db import sqlalchemy_saver, sqlalchemy_getData
from utils import get_logger


@get('/short_news')
def return_short_news():
    log.info("Sending request from zakon.kz general short info")
    count = request.params.get('count', [0])[0]  # count =
    log.info("Getting request from zakon.kz general short info")
    with grpc.insecure_channel("localhost:8080") as channel:
        stub = ZakonCrawlerStub(channel)
        response_short = stub.GetShortNews(
            ShortNewsRequest(count=int(count)))  # http://ZakonCrawler.com/getShortNews?count=1
        news = []
        for n in response_short.news:
            news.append(
                {
                    "time": n.time,
                    "title": n.title
                }
            )

        result = json.dumps(news, ensure_ascii=False)
        return result


@get('/full_news')
def return_full_news():
    log.info("Sending request from zakon.kz general full info")
    count = request.params.get('count', [0])[0]  # count =
    log.info("Getting request from zakon.kz general full info")
    with grpc.insecure_channel("localhost:8080") as channel:
        stub = ZakonCrawlerStub(channel)
        response_full = stub.GetFullNews(
            FullNewsRequest(count=int(count)))  # http://ZakonCrawler.com/getShortNews?count=1
        news = []
        for n in response_full.news:
            news.append(
                {
                    "url": n.url,
                    "title": n.title,
                    "text": n.full_text,
                    "img_url": n.image_link,
                    "date": n.news_date
                }
            )
        result = json.dumps(news, ensure_ascii=False)
    sqlalchemy_saver(result)
    return result


@get('/saved_news')
def get_saved():
    return json.dumps(sqlalchemy_getData(from_date=None, to_date=None), ensure_ascii=False)


if __name__ == "__main__":
    log = get_logger("starter")
    run(host='0.0.0.0', port=8082)
