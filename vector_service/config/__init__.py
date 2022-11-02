import loguru
import sys

YEAR_PATTERN = r"(19|20[0-9]{2})"
PROJECT_NAME = "vector_service"
API_DOCS = "/docs"
OPENAPI_DOCS = "/openapi.json"
API_V1_STR = "/api/v1"

N_WORKERS = 2

def configure_logger():
    format_logger = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "{extra[path]} | "
        "{extra[request_id]} - "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )
    logger = loguru.logger
    logger.remove()
    logger.add(sys.stdout, format=format_logger, level="INFO", backtrace=False, diagnose=False, catch=False)
    logger.opt(exception=False)


configure_logger()
