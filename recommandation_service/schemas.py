from datetime import datetime
from typing import List

from pydantic import BaseModel


class Article(BaseModel):
    id: str
    title: str
    abstract: str
    authors: List[str]
    categories: List[str]
    published: datetime
    updated: datetime


class Articles(BaseModel):
    articles: List[Article]
