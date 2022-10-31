import asyncio
from loguru import logger
import pandas as pd
import redis.asyncio as redis
from typing import Dict, List

from config.redis_config import ARXIV_PAPERS_PREFIX_KEY, QUEUE_NAME, REDIS_URL
from lib.embeddings import Embeddings
from papers_embeddor.load_embeddings import load_all_embeddings
from api.schemas.papers import Paper


redis_client = redis.from_url(REDIS_URL, decode_responses=True)
embeddings = Embeddings()


async def get_papers_in_queue() -> Dict:
    logger.info("Extracting the list of papers to process")
    papers_ids = await redis_client.lrange(QUEUE_NAME, 0, -1)
    logger.info(f"Found {len(papers_ids)} papers to process")
    return papers_ids


async def get_arxiv_papers(ids: List[str]) -> List[Dict]:

    async def get_arxiv_paper(id: str) -> dict:
        fields = [field for field in Paper.__fields__.keys()]
        values = await redis_client.hmget(
            f"{ARXIV_PAPERS_PREFIX_KEY}/{id}",
            fields
        )
        return dict(zip(fields, values))

    papers = await asyncio.gather(*[get_arxiv_paper(id) for id in ids])
    return papers


async def get_arxiv_papers_to_process() -> pd.DataFrame:
    papers_ids = await get_papers_in_queue()
    papers = await get_arxiv_papers(papers_ids)
    return pd.DataFrame([paper for paper in papers])


def create_embeddings(papers_df: pd.DataFrame):
    emb = embeddings.make((papers_df["title"] + ' ' + papers_df["abstract"]).to_list())
    return emb.tolist()


if __name__ == "__main__":
    papers_df = asyncio.run(get_arxiv_papers_to_process())
    papers_df["vector"] = create_embeddings(papers_df)
    asyncio.run(load_all_embeddings(papers_df))
