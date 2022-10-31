import json
from loguru import logger
import re
import requests

from config import YEAR_PATTERN


def process(paper: dict) -> dict:
    paper = json.loads(paper)
    if paper['journal-ref']:
        years = [int(year) for year in re.findall(YEAR_PATTERN, paper['journal-ref'])]
        year = min(years) if years else None
    else:
        year = None
    return {
        'paper_id': paper['id'],
        'title': paper['title'],
        'year': year,
        'authors': paper['authors'],
        'categories': '|'.join(paper['categories'].split(' ')),
        'abstract': paper['abstract']
    }


def process_all_papers(data_path: str):
    processed_papers = []
    logger.info("Pre-processing all the papers")
    with open(data_path, 'r') as f:
        for paper in f:
            paper = process(paper)
            if paper['year']:
                processed_papers.append(paper)
    return processed_papers


def load_all_papers_in_redis(data_path: str):
    papers = process_all_papers(data_path)
    try:
        logger.info("Loading data into Redis")
        requests.post(
            "http://0.0.0.0:8000/vector_service/v1/arxiv/papers",
            json={
                "papers": papers[20:40]
            }
        )
    except Exception as e:
        logger.error(e)
        raise


if __name__ == "__main__":
    data_path = "data/arxiv-metadata-oai-snapshot.json"
    load_all_papers_in_redis(data_path)
