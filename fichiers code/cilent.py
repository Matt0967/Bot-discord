import discord 
import os 
from dotenv import load_dotenv
load_dotenv()
token=os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=discord.Intents.all())

client.run(token=token)