from fastapi import APIRouter, HTTPException
from starlette import status

from app.libs.handlers.aiohttp import get_author_api_json, author_find_sa


dblp_router = APIRouter(tags=['dbpl'])


@dblp_router.get(path='/get_author',
                    summary='')
async def get_journal_info(name: str):
    if name.find(' '):
        name = name.replace(" ","+")
    results = await get_author_api_json(name=name)
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Authors not found")
    return results


# https://dblp.org/search?q=specom
@dblp_router.get(
    path='/get_author_subject_area',
    summary=''
)
async def get_author_subject_area(query:str):
    return await author_find_sa(query=query)