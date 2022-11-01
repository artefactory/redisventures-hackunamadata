import loguru
import os
import sys


VECTOR_SERVICE_HOST = os.environ.get("VECTOR_SERVICE_HOST", "http://0.0.0.0:8000")
VECTOR_SERVICE_ENDPOINT = "api/v1/text/nearest/"
SATURN_TOKEN = os.environ.get("SATURN_TOKEN", "token")

FORMAT_LOGGER = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "{extra[path]} | "
        "{extra[request_id]} - "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

PROJECT_NAME = "recommendation_service"
API_DOCS = "/docs"
OPENAPI_DOCS = "/openapi.json"
API_V1_STR = "/api/v1"


def configure_logger():
    logger = loguru.logger
    logger.remove()
    logger.add(sys.stdout, format=FORMAT_LOGGER, level="INFO", backtrace=False, diagnose=False, catch=False)
    logger.opt(exception=False)
