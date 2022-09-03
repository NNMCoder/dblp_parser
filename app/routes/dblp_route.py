from fastapi import APIRouter, HTTPException
from starlette import status

from app.libs.handlers.aiohttp import get_author_api_json, get_author_publications_api


dblp_router = APIRouter(tags=['dbpl'])


@dblp_router.get(path='/get_author',
                    summary='')
async def get_journal_info(first_name: str,
                           last_name: str):
    results = await get_author_publications_api(first_name=first_name, last_name=last_name)
    # results = await get_author_api_json(first_name=first_name, last_name=last_name)
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Authors not found")
    return results
