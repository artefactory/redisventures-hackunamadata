from fastapi import APIRouter

from api.routes.arxiv import router as arxiv_router
from api.routes.text import router as text_router


main_router = APIRouter()
main_router.include_router(arxiv_router, tags=["arxiv/papers"])
main_router.include_router(text_router, tags=["text"])
