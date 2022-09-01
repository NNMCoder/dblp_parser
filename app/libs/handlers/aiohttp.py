import aiohttp


async def get_author_api_json(first_name, last_name):
    base_url = 'https://dblp.org/search/author/api?q='
    url = f'{base_url}{last_name}+{first_name}&format=json'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.json()
            return result