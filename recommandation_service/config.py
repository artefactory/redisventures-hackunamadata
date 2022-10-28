import sys

import loguru


NUMBER_NEAREST_ARTICLES = 5
VECTOR_SERVICE_ENDPOINT = "localhost/api/v1/text/{text}/nearest"


def configure_logger():
    logger = loguru.logger
    logger.remove()
    format_logger = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "{extra[path]} | "
        "{extra[request_id]} - "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )
    logger.add(sys.stderr, format=format_logger)