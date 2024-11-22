import discord 
from discord.ext import commands 
import random
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents )

@bot.tree.command()
async def multiplication(interaction: discord.Interaction, a: int, b: int):
    await interaction.response.send_message(f"Le résultat de {a} x {b} est {a * b}")

@bot.tree.command()
async def citation(interaction: discord.Interaction):
        quotes = [
            "La vie est un mystère qu'il faut vivre, et non un problème à résoudre. - Gandhi",
            "Le plus grand risque est de ne prendre aucun risque. - Mark Zuckerberg",
            "Le succès, c'est se promener d'échecs en échecs tout en restant motivé. - Winston Churchill",
            "Votre temps est limité, ne le gâchez pas en vivant la vie de quelqu'un d'autre. - Steve Jobs"
        ]
        quote = random.choice(quotes)
        await interaction.response.send_message(quote)
@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} commandes ont été synchronisées")
    except Exception as e:
        print(e)

async def main():
    token = os.getenv("DISCORD_TOKEN")
    await bot.start(token)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
