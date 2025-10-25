import discord
from discord.ext import commands
import random  
from discord import app_commands

class Citation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="citation", description="une Citation Motivante - Inspirante")
    async def citation(self, interaction: discord.Interaction):
        quotes = [
            "La vie est un mystère qu'il faut vivre, et non un problème à résoudre. - Gandhi",
            "Le plus grand risque est de ne prendre aucun risque. - Mark Zuckerberg",
            "Le succès, c'est se promener d'échecs en échecs tout en restant motivé. - Winston Churchill",
            "Votre temps est limité, ne le gâchez pas en vivant la vie de quelqu'un d'autre. - Steve Jobs",
            "Le succès n'est pas la clé du bonheur. Le bonheur est la clé du succès. Si vous aimez ce que vous faites, vous réussirez. – Albert Schweitzer",
            "Le seul endroit où le succès vient avant le travail est dans le dictionnaire – Vidal Sassoon",
            "Ne rêve pas ta vie, vis ton rêve – Anonyme",
            "Les grandes choses ne sont jamais faites par une seule personne, elles sont faites par une équipe – Steve Jobs",
            "Le plus grand échec est de ne pas avoir le courage d'oser – Abbé Pierre",
            "Il ne s’agit pas d’être le meilleur, mais d’être meilleur que la personne que nous étions hier – Anonyme",
            "La seule limite à notre épanouissement de demain sera nos doutes d’aujourd’hui – Franklin D. Roosevelt",
            "Le succès consiste à aller d'échec en échec sans perdre son enthousiasme – Winston Churchill",
            "Vous ne pouvez pas changer votre passé, mais vous pouvez ruiner le présent en vous inquiétant de l'avenir – Anonyme",
            "Les difficultés préparent les gens ordinaires à un destin extraordinaire – C.S. Lewis",
            "Le courage n'est pas l'absence de peur, mais la capacité de vaincre ce qui fait peur – Nelson Mandela",
        ]
        quote = random.choice(quotes)
        await interaction.response.send_message(quote)

async def setup(bot):
    await bot.add_cog(Citation(bot))