import discord
import os
from discord.ext import commands 
from dotenv import load_dotenv

load_dotenv()

class MyBot(commands.Bot):
    async def setup_hook(self):
        for extension in ['popcorn_cmds']:
            await self.load_extension(f'cogs.{extension}')
            
intents = discord.Intents.all()
bot = MyBot(command_prefix="!", intents=intents)

bot.run(os.getenv('DISCORD_TOKEN'))