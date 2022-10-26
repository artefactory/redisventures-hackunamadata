from typing import List

from pydantic import BaseModel


class Article(BaseModel):
    id: str
    title: str
    abstract: str


class Articles(BaseModel):
    articles: List[Article]
