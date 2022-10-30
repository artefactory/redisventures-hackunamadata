import os

REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
REDIS_DB = os.environ.get("REDIS_DB", 0)
REDIS_USERNAME = os.environ.get("REDIS_USERNAME", "default")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "testing123")
REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
os.environ["REDIS_DATA_URL"] = REDIS_URL
os.environ["REDIS_OM_URL"] = REDIS_URL
QUEUE_NAME = "papers_to_process"
INDEX_NAME = "papers_index"
INDEX_TYPE = os.environ.get("INDEX_TYPE", "HNSW")
ARXIV_PAPERS_PREFIX_KEY = "/arxiv/papers"
