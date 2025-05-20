from fastapi import APIRouter

from api.v1.endpoints import produtos


api_router = APIRouter()
api_router.include_router(produtos.router, prefix='/produtos', tags=["produtos"])


