import asyncio
from fastapi import APIRouter
from loguru import logger
import redis.asyncio as redis
from typing import Any, Dict, List

from api.schemas.similarity_search import UserTextSimilarityRequest
from config.redis_config import INDEX_NAME, REDIS_URL, ARXIV_PAPERS_PREFIX_KEY
from lib.embeddings import Embeddings
from lib.search_index import SearchIndex
from api.schemas.papers import Paper

router = APIRouter()
redis_client = redis.from_url(REDIS_URL)
embeddings = Embeddings()
search_index = SearchIndex()


async def process_paper(p, i: int) -> Dict[str, Any]:
    fields = [field for field in Paper.__fields__.keys() if field != "vector"]
    values = await redis_client.hmget(
        f"{ARXIV_PAPERS_PREFIX_KEY}/{p.paper_id}",
        fields
    )
    paper = dict(zip(fields, values))
    score = 1 - float(p.vector_score)
    paper['similarity_score'] = score
    return paper


async def papers_from_results(total, results) -> Dict[str, Any]:
    return {
        'total': total,
        'papers': [
            await process_paper(p, i)
            for i, p in enumerate(results.docs)
        ]
    }


@router.post("/nearest/", response_model=Dict)
async def find_papers_by_user_text(similarity_request: UserTextSimilarityRequest):
    logger.info("Getting the nearest articles for given text and parameters")
    try:
        query = search_index.vector_query(
            similarity_request.categories,
            similarity_request.years,
            similarity_request.search_type,
            similarity_request.number_of_results
        )
        count_query = search_index.count_query(
            years=similarity_request.years,
            categories=similarity_request.categories
        )
        total, results = await asyncio.gather(
            redis_client.ft(INDEX_NAME).search(count_query),
            redis_client.ft(INDEX_NAME).search(
                query,
                query_params={
                    "vec_param": embeddings.make(similarity_request.text).tobytes()
                }
            )
        )
        return await papers_from_results(total.total, results)
    except Exception as e:
        logger.error(e)
        raise
