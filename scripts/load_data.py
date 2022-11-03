import json
import os
from math import ceil
import requests
from tqdm import tqdm

VECTOR_SERVICE_URL = os.environ.get('VECTOR_SERVICE_SATURN_URL', 'http://0.0.0.0:8000')
TOKEN = os.environ.get("SATURN_TOKEN", "token")
LOAD_BATCH_SIZE = 10000


def process_paper(paper: str) -> dict:
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


def read_file(file_path: str) -> list[str]:
    print(f"Reading data from {file_path}")
    with open(file_path, 'r') as f:
        return f.readlines()


def paper_batch_generator(lines: list[str]) -> dict:
    for i in range(0, len(lines), LOAD_BATCH_SIZE):
        batch_of_papers = lines[i:i+LOAD_BATCH_SIZE]
        yield list(map(process_paper, batch_of_papers))


def load_all_papers_in_redis(file_path: str):
    data = read_file(file_path)
    progress_bar_length = ceil(len(data) / LOAD_BATCH_SIZE)
    print(f"Sending data to Vector Service per batch of {LOAD_BATCH_SIZE}.")
    try:
        for papers_batch in tqdm(paper_batch_generator(data), total=progress_bar_length):
            requests.post(
                f"{VECTOR_SERVICE_URL}/api/v1/arxiv/papers",
                json={"papers": papers_batch},
                headers={"Authorization": f"token {TOKEN}"}
            )
    except Exception as e:
        print(e)
        raise


if __name__ == "__main__":
    data_path = "../data/arxiv-metadata-oai-snapshot.json"
    load_all_papers_in_redis(data_path)
