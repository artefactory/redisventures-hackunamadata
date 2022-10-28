import sys

import loguru


NUMBER_NEAREST_ARTICLES = 5
VECTOR_SERVICE_ENDPOINT = "localhost/api/v1/text/{text}/nearest"

FORMAT_LOGGER = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "{extra[path]} | "
        "{extra[request_id]} - "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )


def configure_logger():
    logger = loguru.logger
    logger.remove()
    logger.add(sys.stdout, format=FORMAT_LOGGER, level="INFO", backtrace=False, diagnose=False, catch=False)
    logger.opt(exception=False)
