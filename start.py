import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from keep_alive import keep_alive

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Charger les extensions
@bot.event
async def on_ready():
    for extension in ['commande-slash']:
        try:
            await bot.load_extension(f'cogs.{extension}')
        except Exception as e:
            print(f'Une erreur est survenue lors du chargement de l\'extension {extension}: {type(e).__name__} - {e}')

@bot.event
async def on_ready():
    print(f'{bot.user.name} a rejoint le serveur !')

keep_alive()
bot.run(token=token)