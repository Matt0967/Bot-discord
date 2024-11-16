import discord 
import os 
from dotenv import load_dotenv

load_dotenv()
token=os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=discord.Intents.all())

# Dictionary to store user experience points
user_exp = {}

@client.event
async def on_message(message: discord.Message):
   if message.author == client.user:
       return
   elif message.content.lower().startswith("hello"):
        await message.channel.send("bonjour, c'est le bot de test")
   else:
        if message.author.id not in user_exp:
            user_exp[message.author.id] = 0
        user_exp[message.author.id] += 1

@client.event
async def on_message_delete(message: discord.Message):
    await message.channel.send(f"{message.author.name} a supprimé {message.content}") 

client.run(token=token)
