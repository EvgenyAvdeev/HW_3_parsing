import aiofiles
import aiohttp
import asyncio
from bs4 import BeautifulSoup


async def get_html(session, url):
    async with session.get(url, headers={'User-Agent': 'Opera/9.80 (Macintosh; Intel Mac OS X; U; en) Presto/2.2.15 Version/10.00'}) as response:
        return await response.text()


async def find_links_in_page(session, url, file):
    html = await fetch_html(session, url)
    soup = BeautifulSoup(html, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a', href=True)]

    async with aiofiles.open(file, 'a') as f:
        for link in links:
            if link != '/' and link != '#':
                await f.write(link + '\n')


async def main(urls, output_file):
    async with aiohttp.ClientSession() as session:
        tasks = [find_links_in_page(session, url, output_file) for url in urls]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    url_list = ['https://regex101.com/',
                'https://docs.python.org/3/this-url-will-404.html',
                'https://www.nytimes.com/guides/',
                'https://www.mediamatters.org/',
                'https://1.1.1.1/',
                'https://www.politico.com/tipsheets/morning-money',
                'https://www.bloomberg.com/markets/economics',
                'https://www.ietf.org/rfc/rfc2616.txt']
    output_file = "found_links.txt"
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main(url_list, output_file))
