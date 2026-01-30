import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import json

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

load_dotenv()

def load_data():
    with open("watchlist.json", 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open("watchlist.json", 'w', encoding='utf-8') as f:
        return json.dump(data, f, indent=4, ensure_ascii=False)

@bot.tree.command(name="add-to-watchlist", description="Categories: films, cartoons or anime.", nsfw=False)
async def add_movie(interaction: discord.interactions, category: str, name: str):
    await interaction.response.defer()
    category = category.lower()
    data = load_data()

    if category in data:
        if name.title() not in data[category]:
            data[category].append(name.title())
            save_data(data)

            embed = discord.Embed(title="Nouvel Ajout !",
                                  description=f"**{name.title()}** a rejoint la watchlist {category.title()}!",
                                  color=0x800020)
            embed.add_field(name="Category", value=category.title(), inline=True)
            embed.add_field(name="Added by", value= interaction.user.display_name, inline=True)

            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            embed.set_footer(text="Modou.Modo--V1.0 | Mais say namnaleu, sérieux.")
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(f"{name.title()} est déja dans la liste {category.title()}.")
            return
    else:
        await interaction.followup.send(f"Y a pas de catégorie {category.upper()} mais sinon namnaleu, ça dit quoi ?")

@bot.tree.command(name="remove-from-watchlist", description="Categories: films, cartoons or anime.")
async def remove_movie(interaction: discord.interactions, category: str, name: str):
    await interaction.response.defer()
    category = category.lower()
    data = load_data()
    name = name.title()

    if category in data:
        if name in data[category]:
            data[category].remove(name)
            save_data(data)
            await interaction.followup.send(f"{interaction.user.display_name} a supprimé {name.title()} de la watchlist {category.title()}")
            return
        else:
            await interaction.followup.send(f"{name.title()} n'est pas dans la watchlist {category.title()}.")
            return
    else:
        await interaction.followup.send(f"Y a pas de catégorie {category.upper()} mais sinon namnaleu, ça dit quoi ?")

@bot.hybrid_command(name="watchlist", aliases=["ls", "pop"], description="watchlists: films, cartoons or anime.")
async def show_watchlist(ctx, category: str =None):
    data = load_data()

    response = '## ▶️ WATCHLISTS\n'

    emojis={"films":"🎬", 
            "cartoons":"📺",
            "anime":"⛩️"}
    default_emoji = "🔁"

    if category and category not in data:
        await ctx.send(f"Y a pas de catégorie {category.upper()}, mais sinon namnaleu ça dit quoi ?")
        return 
    
    elif category == None:

        for list_n, list in data.items():
            if list_n == 'history': continue 
            icon = emojis.get(list_n.lower(), default_emoji)
            response += f"## {icon}  {list_n.upper()}  {icon} \n\n"
            if not list:
                response += "Vide."

            for item in list:
                response += f"🔸\t{item.title()}\n"
        await ctx.send(response)

    elif category in data:
        category = category.lower()
        items = data[category]
        response = ''

        icon = emojis.get(category.lower(), default_emoji)
        response += f"## {icon}  Watchlist {category.title()}  {icon}\n\n"

        for item in items:
            response += f"🔸\t{item.title()}\n"
        await ctx.send(response)



@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(f"Connecté en tant que {bot.user}, {len(synced)} commande(s) synchronisée(s).")

def main():
    bot.run(os.getenv('DISCORD_TOKEN'))

if __name__ == '__main__':
    main()
