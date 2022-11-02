import json
import os
import requests


VECTOR_SERVICE_URL = os.environ.get('VECTOR_SERVICE_SATURN_URL', 'http://0.0.0.0:8000')
TOKEN = os.environ.get("SATURN_TOKEN", "token")


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
    print("Pre-processing all the papers")
    with open(data_path, 'r') as f:
        first_papers = f.readlines()[:10000]
        for paper in first_papers:
            paper = process(paper)
            processed_papers.append(paper)
    return processed_papers


def load_all_papers_in_redis(data_path: str):
    papers = process_all_papers(data_path)
    try:
        print("Sending data to Vector Service")
        requests.post(
            f"{VECTOR_SERVICE_URL}/api/v1/arxiv/papers",
            json={"papers": papers},
            headers={"Authorization": f"token {TOKEN}"}
        )
    except Exception as e:
        print(e)
        raise


if __name__ == "__main__":
    data_path = "../data/arxiv-metadata-oai-snapshot.json"
    load_all_papers_in_redis(data_path)
