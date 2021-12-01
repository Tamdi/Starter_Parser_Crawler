import grpc
from src.proto.zakon_pb2_grpc import ZakonCrawlerServicer, add_ZakonCrawlerServicer_to_server
from src.proto.zakon_pb2 import ShortNewsResponse, ShortNews, FullNewsResponse, FullNews
from crawler import parse_short_obj, parse_full_obj

from concurrent import futures


class Service (ZakonCrawlerServicer):
    def GetShortNews(self, request, context):
        data_short = parse_short_obj(request.count)
        news = []
        for n in data_short:
            news.append(
                ShortNews(
                    time=n["time"],
                    title=n["title"]
                )
            )
        return ShortNewsResponse(
            news=news
        )

    def GetFullNews(self, request, context):
        data_full = parse_full_obj(request.count)
        news = []
        for n in data_full:
            news.append(
                FullNews(
                    url=n["url"],
                    title=n["title"],
                    full_text=n["full_text"],
                    image_link=n["image_link"],
                    news_date=n["news_date"]
                )
            )
        return FullNewsResponse(
            news=news
        )


if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4),)
    add_ZakonCrawlerServicer_to_server(Service(), server)
    server.add_insecure_port('[::]:8080')
    print("Starting grpc server...")
    server.start()
    server.wait_for_termination()
