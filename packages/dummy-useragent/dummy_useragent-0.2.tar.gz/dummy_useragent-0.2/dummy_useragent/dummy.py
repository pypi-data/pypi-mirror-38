import aiohttp
import asyncio
from lxml import etree
import tempfile
import os
import json
DB = os.path.join(tempfile.gettempdir(), "dummy_useragent.json")
from .dummy_useragent import DUMMY_AGENT
import random


class Agent(object):
    def __init__(self, lst=[]):
        self.lst = lst

    def choice(self):
        return random.choice(self.lst)


class UserAgent(object):
    def __init__(self):
        self.start_urls = [
            'http://www.useragentstring.com/pages/useragentstring.php?name=Chrome',
            'http://www.useragentstring.com/pages/useragentstring.php?name=Edge',
            'http://www.useragentstring.com/pages/useragentstring.php?name=Opera+Mini',
            'http://www.useragentstring.com/pages/useragentstring.php?name=Opera+Mobile',
            'http://www.useragentstring.com/pages/useragentstring.php?name=IE+Mobile',
            'http://www.useragentstring.com/pages/useragentstring.php?name=Opera',
            'http://www.useragentstring.com/pages/useragentstring.php?name=Firefox',
            'http://www.useragentstring.com/pages/useragentstring.php?name=Safari'
        ]
        self.map = {}
        self.Chrome = Agent()
        self.Edge = Agent()
        self.Firefox = Agent()
        self.Ie_Mobile = Agent()
        self.Opera = Agent()
        self.Opera_Mini = Agent()
        self.Opera_Mobile = Agent()
        self.Safari = Agent()
        if not os.path.exists(DB):
            with open(DB, 'w') as f:
                json.dump(DUMMY_AGENT, f)
            self.cache = DUMMY_AGENT
        else:
            with open(DB, 'r') as f:
                self.cache = json.load(f)
        for browser in self.cache:
            setattr(self, browser.title(), Agent(self.cache[browser]))

    def random(self):
        key = random.choice(list(self.cache.keys()))
        return random.choice(self.cache[key])

    async def get(self, url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, proxy='http://127.0.0.1:1080') as res:
                    content = await res.read()
                    return content
        except Exception as e:
            return ''

    async def run(self):
        tasks = []
        for url in self.start_urls:
            tasks.append(self.crawl(url))
        await asyncio.gather(*tasks)
        await self.save_cache()

    async def save_cache(self):
        with open(DB, 'w') as f:
            json.dump(self.map, f)

    def refresh(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(self.run()))

    async def crawl(self, url):
        content = await self.get(url)
        name = url.split('=')[-1].replace('+', '_')
        if not content:
            return
        doc = etree.HTML(content)
        useragents = doc.xpath('//div[@id="liste"]//li/a/text()')[:100]
        self.map[name] = useragents
