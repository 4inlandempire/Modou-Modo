import discord
import time
import os
from dotenv import load_dotenv
from discord.ext import commands 
import json

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.tree.command()
async def multiplication(interaction: discord.Interaction, a: int, b: int):
    await interaction.response.send_message(f"{a} x {b} = {a * b}")

@bot.tree.command()
async def repeat(interaction: discord.Interaction, nombre: int, message: str):
    await interaction.response.send_message(f"{message}")
    for i in range(1, nombre):
        await interaction.followup.send(message)

@bot.tree.command()
async def wait(interaction: discord.Interaction, secondes: int):
    if secondes > 20 or secondes <= 0:
        return 
    else:
        await interaction.response.defer()
        time.sleep(secondes)
        await interaction.followup.send("I'm done waiting!")
      

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} commande(s) synchronisée(s).")
    except Exception as e:
        print(e)

def main():
    bot.run(os.getenv('DISCORD_TOKEN'))

if __name__ == '__main__':
    main()