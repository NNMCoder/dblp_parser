import asyncio
from pprint import pprint
from bs4 import BeautifulSoup as Bs
import aiohttp


async def get_author_publications_api(session, first_name, last_name):
    base_url = 'https://dblp.org/search/publ/api?q='
    url = f'{base_url}{last_name}+{first_name}&format=json'

    async with session.get(url) as response:
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

                for author in authors.get('author'):
                    _authors.add(author.get('text'))

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


async def get_author_api_json(first_name, last_name):
    base_url = 'https://dblp.org/search/author/api?q='
    url = f'{base_url}{last_name}+{first_name}&format=json'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
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
                    publications_data = await get_author_publications_api(session=session, first_name=first_name, last_name=last_name)
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





