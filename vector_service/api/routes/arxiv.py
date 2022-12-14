import asyncio
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from loguru import logger
import redis.asyncio as redis
from typing import Dict

from api.schemas.papers import Paper, PapersList
from config.redis_config import ARXIV_PAPERS_PREFIX_KEY, QUEUE_NAME, REDIS_URL
from lib.embeddings import Embeddings


router = APIRouter()
redis_client = redis.from_url(REDIS_URL)
embeddings = Embeddings()


@router.post("/arxiv/papers")
async def load_papers(papers_list: PapersList):
    logger.info("Loading all papers in redis")

    async def load_paper(paper: Paper):
        await redis_client.hset(
            f"{ARXIV_PAPERS_PREFIX_KEY}/{paper.id}",
            mapping=dict(paper)
        )
        await redis_client.lpush(
            QUEUE_NAME,
            paper.id
        )
    try:
        await asyncio.gather(*[load_paper(paper) for paper in papers_list.papers])
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"status": "ok"})
    except Exception as e:
        logger.error(e)
        raise


@router.get("/arxiv/papers/{id}")
async def get_arxiv_paper(id: str) -> Dict:
    logger.info(f"Retrieving Arxiv paper with id {id}")
    fields = [field for field in Paper.__fields__.keys()]
    try:
        values = await redis_client.hmget(
            f"{ARXIV_PAPERS_PREFIX_KEY}/{id}",
            fields
        )
        result = {
            "result": dict(zip(fields, values))
        }
        return result
    except Exception as e:
        logger.error(e)
        raise
