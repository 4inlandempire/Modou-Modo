import discord
import os
from discord.ext import commands 
from dotenv import load_dotenv

load_dotenv()

class MyBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def setup_hook(self):
        for extension in ['popcorn_cmds']:
            await self.load_extension(f'cogs.{extension}')
            print(f"{extension} chargée.")

intents = discord.Intents.all()
bot = MyBot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user.name}.")
    await bot.tree.sync()
bot.run(os.getenv('DISCORD_TOKEN'))