import asyncio
from fastapi import APIRouter, HTTPException
from starlette import status
from app.schemas.schemas import BaseQuery

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
@dblp_router.post(
    path='/get_author_subject_area',
    summary=''
)
async def get_author_subject_area(query: BaseQuery):
    # results = await author_find_sa(query=query.required_keywords)
    print(query.required_keywords)
    tasks = []
    for query in query.required_keywords:
        task = asyncio.ensure_future(author_find_sa(query=query))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Authors not found")
    return results