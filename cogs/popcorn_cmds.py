from discord import app_commands
import discord
from discord.ext import commands
from tools import load_data, save_data

class WatchlistCogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @app_commands.command(name="add-to-watchlist", description="Categories: films, cartoons or anime.", nsfw=False)
    async def add_movie(self, interaction: discord.interactions, category: str, name: str):
        await interaction.response.defer()
        category = category.lower()
        data = load_data()
        name = name.title()

        if category in data:
            if name not in data[category]:
                data[category][name] = {"status":"plan to watch."}

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

    @app_commands.command(name="remove-from-watchlist", description="Categories: films, cartoons or anime.")
    async def remove_movie(self, interaction: discord.interactions, category: str, name: str):
        await interaction.response.defer()
        category = category.lower()
        data = load_data()
        name = name.title()

        if category in data:
            if name in data[category]:
                data[category].remove(name)
                save_data(data)
                await interaction.followup.send(f"{interaction.user.display_name} a supprimé {name.title()} de la watchlist {category.title()}.")
                return
            else:
                await interaction.followup.send(f"{name.title()} n'est pas dans la watchlist {category.title()}.")
                return
        else:
            await interaction.followup.send(f"Y a pas de catégorie {category.upper()} mais sinon namnaleu, ça dit quoi ?")

    @commands.hybrid_command(name="watchlist", aliases=["ls", "pop"], description="watchlists: films, cartoons or anime.")
    async def show_watchlist(self, ctx, category: str =None):
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

    @app_commands.command(name="start-watching", description="Catégories: films/anime/cartoons/series" )
    async def start_watching(self, interaction: discord.interactions, category: str, 
                             name: str, episodes: int, seasons: int):
        await interaction.response.defer()

        data = load_data()
        category = category.lower()
        name = name.title()
        repertory = data[category]

        if category in data:
            if name not in category:
                repertory[name] = {"current season":1,
                                   "episodes remaining":episodes,
                                   "status":"watching",
                                   "current episode":0,
                                   "seasons":seasons}
                save_data(data)
                
                # TO-DO AJOUTER DES EMBED RENDRE LE TEXTE PLUS DIGESTE 
                await interaction.followup.send(f"{name.title()} a été ajouté à {category.title()}, il reste {repertory[name]["episodes remaining"]} épisodes.")
            else:
                await interaction.followup.send(f"Utilisez la commande /watched pour mettre à jour {name.title()}")
                return
        else:
            await interaction.followup.send(f"Désolé y a pas de catégorie {category.title()}, faut demander en fait.")
            return
        
        # TO-DO AJOUTER LA COMMANDE WATCHED QUI METS A JOUR LA COMMANDE START-WATCHING
        # TO-DO REMODELER LE NOM DES CATEGORIES AU SINGULIER PARCE QUE "filmS" et "serieS" flemme.
        # AJOUT IFCON POUR WATCHED LORSQUE LA DERNIERE SAISON EST ATTEINTE POUR TRANSITION DU NOM VERS HISTORY 
        # REFLECHIR A UNE COMMANDE POUR LE NOMBRE D'EPISODES PAR SAISON OU SAISON PUIS EPISODES DE LA SAISON TO AVOID HEAVY COMMITMENT
        # ADD A STATUS CHANGE COMMAND FOR THE ADDS TO THE JSON DICT

async def setup(bot):
    await bot.add_cog(WatchlistCogs(bot))
