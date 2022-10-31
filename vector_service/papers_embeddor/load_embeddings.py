import asyncio
from loguru import logger
import numpy as np
import pandas as pd
import redis.asyncio as redis
import re
from redis.commands.search.field import TagField

from config.redis_config import ARXIV_PAPERS_PREFIX_KEY, REDIS_URL, INDEX_TYPE
from config import YEAR_PATTERN
from lib.search_index import SearchIndex


def extract_year(journal_ref: str) -> str:
    if journal_ref:
        years = [int(year) for year in re.findall(YEAR_PATTERN, journal_ref)]
        year = min(years) if years else ""
    else:
        year = ""
    return year


def process_categories(categories: str) -> str:
    return '|'.join(categories.split(' '))


async def gather_with_concurrency(n, redis_conn, *papers):
    semaphore = asyncio.Semaphore(n)

    async def load_paper(paper):
        async with semaphore:
            vector = paper['vector']
            year = extract_year(paper["journal_ref"])
            categories_processed = process_categories(paper["categories"])
            await redis_conn.hset(
                f"{ARXIV_PAPERS_PREFIX_KEY}/{paper['id']}",
                mapping={
                    "vector": np.array(vector, dtype=np.float32).tobytes(),
                    "year": year,
                    "categories_processed": categories_processed
                }
            )

    await asyncio.gather(*[load_paper(p) for p in papers])


async def load_all_embeddings(papers: pd.DataFrame):
    redis_conn = redis.from_url(REDIS_URL)
    search_index = SearchIndex()
    logger.info("Loading embeddings into Redis")
    papers = papers.to_dict('records')
    await gather_with_concurrency(100, redis_conn, *papers)
    logger.info("Papers loaded!")

    logger.info("Creating vector search index")
    categories_field = TagField("categories_processed", separator="|")
    year_field = TagField("year", separator="|")
    try:
        if INDEX_TYPE == "HNSW":
            await search_index.create_hnsw(
                categories_field,
                year_field,
                redis_conn=redis_conn,
                number_of_vectors=len(papers),
                prefix=ARXIV_PAPERS_PREFIX_KEY,
                distance_metric="IP",
            )
        else:
            await search_index.create_flat(
                categories_field,
                year_field,
                redis_conn=redis_conn,
                number_of_vectors=len(papers),
                prefix=ARXIV_PAPERS_PREFIX_KEY,
                distance_metric="IP",
            )
        logger.info("Search index created")
    except Exception:
        logger.info("Index arlready exists")
