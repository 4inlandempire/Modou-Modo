import discord 
import os 
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.hybrid_command()
async def ping(ctx):
    await ctx.send("pong!")

@bot.hybrid_command()
async def parle(ctx):
    await ctx.send("Lorem Ipsum")

@bot.event
async def on_ready():
    sync = await bot.tree.sync()
    print(f"En ligne en tant que: {bot.user}! {len(sync)} commandes synchronisée(s).")


def main():
    bot.run(os.getenv('DISCORD_TOKEN'))
if __name__ == '__main__':
    main()