import uuid

from config import configure_logger, NUMBER_NEAREST_ARTICLES
from helpers.input_helper import build_vector_service_url
from schemas import Articles

from fastapi import FastAPI, APIRouter, status
from fastapi.responses import JSONResponse
from loguru import logger
import requests


app = FastAPI()
configure_logger()


@app.middleware("http")
async def middleware(request, call_next):
    path = request.scope['path']
    request_id = str(uuid.uuid4())
    with logger.contextualize(request_id=request_id, path=path):
        response = await call_next(request)
        return response


@app.get("/api/v1/recommendations/", response_model=Articles)
async def get_recommendations(text: str):
    logger.info("Getting recommendations")
    try:
        response = requests.get(url=build_vector_service_url(text), params={"k": NUMBER_NEAREST_ARTICLES})
        result = response.json()
        if response.status_code == status.HTTP_200_OK:
            articles = Articles(**result)
            return JSONResponse(articles)

        logger.error({"result": result, "status_code": response.status_code})
        return {
            "details": "An error occurred when requesting vector service",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
        }
    except Exception as e:
        logger.error(e)
        raise
