from asyncio import gather
import asyncio
from wsgiref import headers
from bs4 import BeautifulSoup as Bs
import aiohttp
import random


import json


useragents = open('useragents.txt').read().splitlines()

async def get_author_publications_api(session, name):
    base_url = 'https://dblp.org/search/publ/api?q='
    url = f'{base_url}{name}&format=json'
    useragent = random.choice(useragents)
    headers = {
        "User-Agent": useragent
    }
    
    async with session.request(method = "GET", url=url,headers=headers ) as response:
        result = await response.json()
        result = result.get('result')
        hits = result.get('hits').get('hit')
        publications_data = []
        if hits:
            _authors = set()
            publications_count = len(hits)
            for hit in hits:
                info = hit.get('info')
                authors = info.get('authors')
                title = info.get('title')
                year = info.get('year')
                type = info.get('type')
                doi = info.get('doi')
                ee = info.get('ee')
                url = info.get('url')
                
                # for author in authors.get('author'):
                #     _authors.add(author.get('text'))

            authors_count = len(_authors)
            publications_data.append({'publications_count': publications_count,
                              'authors_count': authors_count})

                # hits_data.append({'title': title,
                #                     'authors': authors,
                #                   'year': year,
                #                   'type': type,
                #                   'doi': doi,
                #                   'ee': ee,
                #                   'url': url})
            return publications_data
        else:
            return None


async def get_author_api_json(name:str):
    base_url = 'https://dblp.org/search/author/api?q='
    url = f'{base_url}{name}&format=json'
    useragent = random.choice(useragents)
    headers = {
        "User-Agent": useragent
    }
    async with aiohttp.ClientSession() as session:
        async with session.request(method = "GET", url=url,headers=headers) as response:
            result = await response.json()
            result = result.get('result')
            hits = result.get('hits').get('hit')
            hits_data = []
            
            if hits:
                for hit in hits:
                    info = hit.get('info')
                    author = info.get('author')
                    url = info.get('url')
                    aliases = info.get('aliases')

                    links = await author_page_parser(session=session, url=url)
                    publications_data = await get_author_publications_api(session=session, name=name)
                    
                    hits_data.append({'author': author,
                                      'url': url,
                                      'aliases': aliases,
                                      'links': links,
                                      'publications_data': publications_data})
                
                return hits_data
            else:
                return None

async def author_page_parser(session, url):
        async with session.get(url) as response:
            html = await response.text()
            soup = Bs(html, 'html.parser')

            orcid = soup.select_one('#headline > nav > ul > li.orcid.drop-down > div.body > ul > li > a')
            orcid_link = soup.select_one('#headline > nav > ul > li.search.drop-down > div.body > ul:nth-child(2) > li:nth-child(6) > a').get('href')
            google_search_link = soup.select_one('#headline > nav > ul > li.search.drop-down > div.body > ul:nth-child(2) > li:nth-child(1) > a').get('href')
            google_scholar_link = soup.select_one('#headline > nav > ul > li.search.drop-down > div.body > ul:nth-child(2) > li:nth-child(2) > a').get('href')
            semantic_scholar_link = soup.select_one('#headline > nav > ul > li.search.drop-down > div.body > ul:nth-child(2) > li:nth-child(3) > a').get('href')
            ia_scholar_link = soup.select_one('#headline > nav > ul > li.search.drop-down > div.body > ul:nth-child(2) > li:nth-child(4) > a').get('href')
            citeseerx_link = soup.select_one('#headline > nav > ul > li.search.drop-down > div.body > ul:nth-child(2) > li:nth-child(5) > a').get('href')
            links = {'orcid_link': orcid_link,
                     'google_scholar_link': google_scholar_link,
                     'google_search_link': google_search_link,
                     'semantic_scholar_link': semantic_scholar_link,
                     'ia_scholar_link': ia_scholar_link,
                     'citeseerx_link': citeseerx_link,
                     }
            if orcid:
                links['orcid'] = orcid.text
            return links


async def author_find_sa(query:str):
    
    base_url = f'https://dblp.uni-trier.de/search/publ/api?callback=jQuery311020347957983698262_1663843905617&q={query}&compl=author&p=2&h=0&c=10&rw=2d&format=json&_=1663843905618'
    useragent = random.choice(useragents)
    headers = {
        "User-Agent": useragent
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.request(method="GET",url=base_url,headers=headers) as response:
            html = await response.text()
            _json = json.loads(html)
            # return _json
            tasks = []
            for author in _json['result']['completions']['c']:
                text = author["text"].replace(":facet:author:","")
                print(text)
                task = asyncio.ensure_future(get_author_api_json(name = text))
                tasks.append(task)
                
            results = await asyncio.gather(*tasks)
            return results