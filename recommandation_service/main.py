from fastapi import FastAPI, status
from loguru import logger
import requests
import uuid
import uvicorn

from config import configure_logger, VECTOR_SERVICE_ENDPOINT, VECTOR_SERVICE_HOST, SATURN_TOKEN
from schemas import UserTextSimilarityRequest


app = FastAPI()
configure_logger()


@app.middleware("http")
async def middleware(request, call_next):
    path = request.scope['path']
    request_id = str(uuid.uuid4())
    logger.configure(extra={"path": path, "request_id": request_id})
    response = await call_next(request)
    return response


@app.post("/recommandation_service/v1/recommendations/")
async def get_recommendations(similarity_request: UserTextSimilarityRequest):
    logger.info("Getting recommendations")
    try:
        response = requests.post(
            url=f"{VECTOR_SERVICE_HOST}/{VECTOR_SERVICE_ENDPOINT}",
            json=dict(similarity_request),
            headers={"Authorization": f"token {SATURN_TOKEN}"}
        )
        result = response.json()
        if response.status_code == status.HTTP_200_OK:
            return {"papers": result["papers"]}

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
