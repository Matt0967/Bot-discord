import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

extensions = [
    "Pomodoro_timer",
    "exp_system",
    "citation"
]

@bot.event
async def on_ready():
    print(f"{bot.user.name} est connecté.")
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} commandes slash synchronisées.")
    except Exception as e:
        print(f"Erreur de synchronisation : {e}")

async def load_extensions():
    for extension in extensions:
        try:
            await bot.load_extension(f"cogs.{extension}")
            print(f"Extension cogs.{extension} chargée.")
        except Exception as e:
            print(f"Erreur de chargement de {extension}: {e}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

import asyncio
asyncio.run(main())