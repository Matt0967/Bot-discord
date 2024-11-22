import discord 
import os

token = os.getenv("DISCORD_TOKEN")

client = discord.Client(intents=discord.Intents.all())

client.run(token)
