from fastapi import APIRouter
from api.v1.endpoints import produtos, auth


api_router = APIRouter()
api_router.include_router(produtos.router, prefix='/produtos', tags=["produtos"])
api_router.include_router(auth.router, prefix='/auth', tags=['auth'])


