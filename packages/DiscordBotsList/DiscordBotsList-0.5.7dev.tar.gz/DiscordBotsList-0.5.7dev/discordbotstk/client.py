import aiohttp
import asyncio
import discord
import json

class BotInfo:
    def __init__(self, r):
        self.avatar = r['avatar']
        try:
            self.guilds = r['guilds']
        except:
            self.guilds = 0
        self.servers = self.guilds
        self.certified = r['certified']
        self.cert = self.certified
        self.description = r['description']
        self.desc = self.description
        self.prefix = r['prefix']
        self.owner_id = r['ownerID']


class client:
    def __init__(self, bot, key:str):
        """Bot: discord.Client or commands.Bot
        Key: api key for authentication."""
        self.bot = bot
        self.key = key

    async def post_gc(self):
        """Posts your guild count to the api."""
        async with aiohttp.ClientSession() as cs:
            guilds = len(self.bot.guilds) if discord.__version__ == '1.0.0a' else len(self.bot.servers)
            async with cs.post(f'http://discordbotslist.com/api/post.php', headers={'Authorization': self.key}, data=json.dumps({'guilds': guilds})) as r:
                return r.status

    async def start_loop(self):
        while True:
            await self.post_gc()
            await asyncio.sleep(18000) # 30 minutes

    async def get_bot_info(self, bot_id:int):
        """Get info about a bot."""
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'https://discordbotslist.com/api/fetch.php?botid={bot_id}') as r:
                r = await r.json()

        return BotInfo(r)