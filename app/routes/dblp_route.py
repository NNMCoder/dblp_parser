from fastapi import APIRouter, HTTPException
from starlette import status

from app.libs.handlers.aiohttp import get_author_api_json


dblp_router = APIRouter(tags=['dbpl'])


@dblp_router.get(path='/get_author',
                    summary='')
async def get_journal_info(name: str):
    name = name.replace(" ","+")
    results = await get_author_api_json(name=name)
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Authors not found")
    return results
