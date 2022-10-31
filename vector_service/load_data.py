import json
from loguru import logger
import requests


def process(paper: dict) -> dict:
    paper = json.loads(paper)
    if not paper['journal-ref']:
        paper['journal-ref'] = ""
    return {
        'id': paper['id'],
        'title': paper['title'],
        'journal_ref': paper['journal-ref'],
        'authors': paper['authors'],
        'categories': paper['categories'],
        'abstract': paper['abstract']
    }


def process_all_papers(data_path: str):
    processed_papers = []
    logger.info("Pre-processing all the papers")
    with open(data_path, 'r') as f:
        first_papers = f.readlines()[0:1000]
        for paper in first_papers:
            paper = process(paper)
            processed_papers.append(paper)
    return processed_papers


def load_all_papers_in_redis(data_path: str):
    papers = process_all_papers(data_path)
    try:
        logger.info("Loading data into Redis")
        requests.post(
            "http://0.0.0.0:8000/vector_service/v1/arxiv/papers",
            json={
                "papers": papers
            }
        )
    except Exception as e:
        logger.error(e)
        raise


if __name__ == "__main__":
    data_path = "data/arxiv-metadata-oai-snapshot.json"
    load_all_papers_in_redis(data_path)
