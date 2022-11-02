from pydantic import BaseModel


class Paper(BaseModel):
    id: str
    title: str
    authors: str
    abstract: str
    categories: str
    journal_ref: str


class PapersList(BaseModel):
    papers: list[Paper]
