import asyncio
import json
from random import randint

from fastapi import APIRouter, HTTPException
from starlette import status

from app.libs.MySQL.crud import update_author_info_db
from app.schemas.schemas import BaseQuery

from app.libs.handlers.aiohttp import get_author_api_json, author_find_sa
import aiohttp

from app.settings import Settings

settings = Settings()

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
    print(query.query_id)
    tasks = []
    for _query in query.required_keywords:
        task = asyncio.ensure_future(author_find_sa(query=_query))
        tasks.append(task)

    results = await asyncio.gather(*tasks)

    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Authors not found")
    for result_one in results:
        for result in result_one:
            update_author_info_db((randint(1,9999),
                               None,
                               None,
                               result[0].get('cited_count'),
                               None,
                               result[0].get('h_index'),
                               result[0].get('authors_count'),
                               None,
                               None,
                               None,
                               None,
                               None,
                               None,
                               None,
                               result[0].get('links').get('orcid'),
                               result[0].get('author'),
                               result[0].get('author'),
                               result[0].get('url')
                               ))
    query_id = int(query.query_id)
    send_data = dict(query_id = query_id, user_type = "scopus")
  
    url = f'{settings.finish_end_point}/finish/scopus_search'
    
    # ! Test
    # url = f'{settings.finish_end_point}/dblp/test_router'

    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, json = send_data) as response:
            ...
    return results


@dblp_router.post(path="/test_router")
async def test_router(data: dict):
    print(data)