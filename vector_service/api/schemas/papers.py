from pydantic import BaseModel


class Paper(BaseModel):
    paper_id: str
    title: str
    authors: str
    abstract: str
    categories: str
    year: str


class PapersList(BaseModel):
    papers: list[Paper]
