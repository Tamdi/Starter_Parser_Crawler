from pydantic import BaseModel


class ShortNews(BaseModel):
    time: str
    title: str


class FullNews(BaseModel):
    url: str
    title: str
    text: str
    img_url: str
    date: str
