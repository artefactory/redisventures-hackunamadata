from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import requests
import uuid
import uvicorn

from config import (
    configure_logger,
    API_DOCS,
    API_V1_STR,
    OPENAPI_DOCS,
    PROJECT_NAME,
    VECTOR_SERVICE_ENDPOINT,
    VECTOR_SERVICE_HOST,
    SATURN_TOKEN
)
from schemas import Papers, UserTextSimilarityRequest


app = FastAPI(
    title=PROJECT_NAME,
    docs_url=API_DOCS,
    openapi_url=OPENAPI_DOCS
)
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="chrome-extension:\/\/.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
configure_logger()


@app.middleware("http")
async def middleware(request, call_next):
    path = request.scope['path']
    request_id = str(uuid.uuid4())
    logger.configure(extra={"path": path, "request_id": request_id})
    response = await call_next(request)
    return response


@app.post(f"{API_V1_STR}/recommendations/", response_model=Papers)
def get_recommendations(similarity_request: UserTextSimilarityRequest):
    logger.info("Getting recommendations")
    try:
        response = requests.post(
            url=f"{VECTOR_SERVICE_HOST}/{VECTOR_SERVICE_ENDPOINT}",
            json=dict(similarity_request),
            headers={"Authorization": f"token {SATURN_TOKEN}"}
        )
        result = response.json()
        if response.status_code == status.HTTP_200_OK:
            return Papers(papers=result["papers"])
        logger.error({"result": result, "status_code": response.status_code})
        return {
            "details": "An error occurred when requesting vector service",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
        }
    except Exception as e:
        logger.error(e)
        raise


if __name__ == "__main__":

    server_attr = {
        "host": "0.0.0.0",
        "reload": True,
        "port": 8080,
        "workers": 1
    }
    uvicorn.run("main:app", **server_attr)
