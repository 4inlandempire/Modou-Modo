import discord
import os
from dotenv import load_dotenv
import json

def load_data():
    try:
        with open('watchlist.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"anime":[], "cartoons":[], "films":[], "history":[]}
    
def save_data(data):
    with open('watchlist.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

load_dotenv()

# On demande le minimum vital pour ne pas faire planter Discord
intents = discord.Intents.default()
intents.message_content = True 

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ EN LIGNE : {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(f"Message vu : {message.content}")
    if message.content == '!test':
        await message.channel.send('Le test fonctionne !')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Commande !add [catégorie] [nom]
    if message.content.startswith('!add'):
        parts = message.content.split(' ', 2) # Sépare "!add", "catégorie" et "le reste"
        
        if len(parts) < 3:
            await message.channel.send("Usage: `!add [anime/films/cartoons] [nom]`")
            return

        category = parts[1].lower()
        item_name = parts[2]

        # 1. Charger les données actuelles
        data = load_data()

        # 2. Vérifier si la catégorie existe et ajouter l'item
        if category in data:
            data[category].append(item_name)
            # 3. Sauvegarder dans le fichier JSON
            save_data(data)
            await message.channel.send(f"✅ **{item_name}** ajouté à la liste **{category}** !")
        else:
            await message.channel.send("❌ Catégorie invalide. Choisis : anime, films ou cartoons.")

client.run(os.getenv('DISCORD_TOKEN'))