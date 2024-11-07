import discord 
import os 
from dotenv import load_dotenv

load_dotenv()
token=os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_message(message: discord.Message):
   if message.author == client.user:
       return
   elif message.content.lower().startswith("hello"):
        await message.channel.send("bonjour, c'est le bot de test")


@client.event
async def on_message_delete(message: discord.Message):
    await message.channel.send(f"{message.author.name} a supprimé {message.content}") 

client.run(token=token)