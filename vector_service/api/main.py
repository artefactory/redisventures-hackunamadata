from fastapi import FastAPI
from loguru import logger
import uuid
import uvicorn

from api.routes import main_router
from config import API_DOCS, API_V1_STR, OPENAPI_DOCS, PROJECT_NAME


app = FastAPI(
    title=PROJECT_NAME,
    docs_url=API_DOCS,
    openapi_url=OPENAPI_DOCS
)

app.include_router(
    main_router,
    prefix=API_V1_STR
)


@app.middleware("http")
async def middleware(request, call_next):
    path = request.scope['path']
    request_id = str(uuid.uuid4())
    logger.configure(extra={"path": path, "request_id": request_id})
    response = await call_next(request)
    return response


if __name__ == "__main__":

    server_attr = {
        "host": "0.0.0.0",
        "reload": True,
        "port": 8000,
        "workers": 1
    }
    uvicorn.run("main:app", **server_attr)
