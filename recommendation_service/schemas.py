from pydantic import BaseModel


class UserTextSimilarityRequest(BaseModel):
    text: str
    categories: list = []
    years: list = []
    number_of_results: int = 5
