from config import SIMILARITY_SCORE_LIMIT
from pydantic import BaseModel, validator


class UserTextSimilarityRequest(BaseModel):
    text: str
    categories: list = []
    years: list = []
    number_of_results: int = 5


class Paper(BaseModel):
    id: str
    title: str
    authors: str
    abstract: str
    categories: str
    journal_ref: str
    similarity_score: float


class Papers(BaseModel):
    papers: list[Paper]

    @validator("papers", pre=True)
    def remove_paper_with_low_similarity(values):
        return [paper for paper in values if paper["similarity_score"] > SIMILARITY_SCORE_LIMIT]
