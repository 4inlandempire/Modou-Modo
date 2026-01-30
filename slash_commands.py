import asyncio
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands 
import json

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

def load_data():
    try:
        with open("watchlist.json", 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    
def write_data(data):
    with open("watchlist.json", 'w', encoding='utf-8') as f:
        return json.dump(data, f, indent=4, ensure_ascii=False)


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
        await interaction.response.send_message("Mets entre 1 et 20 secondes.")
        return 
    else:
        await interaction.response.defer()
        await asyncio.sleep(secondes)
        await interaction.followup.send("I'm done waiting!")

@bot.tree.command()
async def add(interaction: discord.Interaction, catégorie: str, nom: str):
    # Permet de donner du temps au bot d'executer la commande et non l'utilisateur d'ecrire plus longtemps
    await interaction.response.defer()
    catégorie = catégorie.lower()
    data = load_data()


    if catégorie in data:
        if nom.title() not in data[catégorie]:
            data[catégorie].append(nom.title())
            write_data(data)
            await interaction.followup.send(f"{nom.title()} a été ajouté à la watchlist {catégorie.title()}")
        else:
            await interaction.followup.send(f"{nom.title()} est déja dans la liste.")
            return
    else:
        await interaction.followup.send(f"Y a pas de catégorie {catégorie}, mais sinon namnaleu ça dit quoi?")


      

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