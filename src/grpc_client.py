import grpc
from src.proto.zakon_pb2_grpc import ZakonCrawlerStub
from src.proto.zakon_pb2 import ShortNewsRequest, FullNewsRequest

if __name__ == '__main__':
    with grpc.insecure_channel("localhost:8080") as channel:
        stub = ZakonCrawlerStub(channel)
        response_short = stub.GetShortNews(ShortNewsRequest(count=10)) #http://ZakonCrawler.com/getShortNews?count=1
        for n in response_short.news:
            print("----")
            print(f'Time: {n.time}')
            print(f'Title: {n.title}')

        response_full = stub.GetFullNews(FullNewsRequest(count=10))  #http://ZakonCrawler.com/getShortNews?count=1
        for n in response_full.news:
            print("----")
            print(f'Url: {n.url}')
            print(f'Title: {n.title}')
            print(f'Full_text: {n.full_text}')
            print(f'Image_link: {n.image_link}')
            print(f'News_date: {n.news_date}')
