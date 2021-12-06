import requests
import json
from models import ShortNews, FullNews
from bs4 import BeautifulSoup
from config import RESOURCE_URL


def parse_short_obj(params):
    response = requests.get(
        RESOURCE_URL,
        timeout=10,
    )
    print(response.status_code)
    print(response.content)
    if response.ok:
        response_content = response.content
        print(response_content)
        data = []
        json_data = response.json()
        for _a in json_data["data_list"]:
            title = _a["page_title"]
            time = _a["published_date"]
            data.append(
                ShortNews(time=time, title=title)
            )
        if params:
            return data[0:int(params)]
        return data


def parse_full_obj(params):
    response = requests.get(
        RESOURCE_URL,
        timeout=10,
    )
    if response.ok:
        response_content = response.content
        print(response_content)
        data = []
        json_data = response.json()
        for _a in json_data["data_list"]:
            link_to_full_news = "https://zakon.kz/" + _a["alias"]
            response = requests.get(
                link_to_full_news,
                timeout=10,
            )
            response_content_new = response.content
            soup_new = BeautifulSoup(response_content_new, 'html.parser')
            json_full_news = soup_new.find("script", {"type": "application/ld+json"})
            full_news = json.loads(json_full_news.text)
            print(json_full_news)
            image_link = full_news["image"]["url"]
            url = full_news["mainEntityOfPage"]["@id"]
            title = full_news["headline"]
            full_text = full_news["description"]
            news_date = full_news["datePublished"]
            data.append(
                FullNews(url=url, title=title, text=full_text, date=news_date, img_url=image_link)
            )
        if params:
            return data[0:int(params)]
        return data


if __name__ == "__main__":
    start = parse_short_obj(1)
    print(start)
