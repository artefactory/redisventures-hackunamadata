from fastapi import FastAPI
import uvicorn

from api.routes import main_router
from config import API_DOCS, API_V1_STR, OPENAPI_DOCS, PROJECT_NAME
from config.redis_config import REDIS_URL


app = FastAPI(
    title=PROJECT_NAME,
    docs_url=API_DOCS,
    openapi_url=OPENAPI_DOCS
)

app.include_router(
    main_router,
    prefix=API_V1_STR
)


if __name__ == "__main__":

    server_attr = {
        "host": "0.0.0.0",
        "reload": True,
        "port": 8000,
        "workers": 1
    }
    uvicorn.run("main:app", **server_attr)
