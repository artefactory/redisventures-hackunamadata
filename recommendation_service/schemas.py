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

    class Config:
        fields = {'similarity_score': {'exclude': True}}


class Papers(BaseModel):
    papers: list[Paper]

    @validator("papers", each_item=True, pre=True)
    def remove_paper_with_low_similarity(self, value):
        if value["similarity_score"] < SIMILARITY_SCORE_LIMIT:
            return None
        return value
