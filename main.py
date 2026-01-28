import discord
import os
from dotenv import load_dotenv
from discord.ext import commands 
import json

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

def load_data():
    try:
        with open('watchlist.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"anime":[], "films":[], "cartoons":[], "history":[]}
    
def save_data(data):
    with open("watchlist.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@bot.event
async def on_ready():
    print(f"En ligne: {bot.user}")

@bot.command(help="Ajoute un nouvel éléments aux watchlists.")
async def add(ctx, category: str, *, item_name: str):

    category = category.lower()
    data = load_data()

    if category in data:
        data[category].append(item_name.tile())
        save_data(data)
        await ctx.send(f"{item_name.title()} a été ajouté {category}!")
    else:
        await ctx.send("Catégories valides: Anime, Cartoons, films.")

@bot.command(name="list")   
async def show_list(ctx, category:str =None):
    data = load_data()

    if category is not None and category not in data:
        await ctx.send(f"Y a pas de watchlist de {category}, mais sinon namnaleu, ça dit quoi ?")
        return

    if category in data:
        items = data[category]
        reponse = ''

        for item in items:
            reponse += f"- {item.title()}\n"
        await ctx.send(reponse)
    elif category == None:
       all_data = data 
       reponse = ''

       for category, list in data.items():
           if category == "history": continue 

           reponse += f"**\n-- {category.upper()} --**\n"
           
           if list:
                for _ in list:
                   reponse += f"- {_.upper()}\n"
    await ctx.send(reponse)            
    
bot.run(os.getenv('DISCORD_TOKEN'))