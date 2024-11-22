import discord
from discord.ext import commands 
import os

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="$", intents=intents)

@bot.command(name="hello", alliases=['hw', 'hello_world'])
async def hello_world(context):
    await context.send("Hello, world")

@bot.command()
async def decompte(context, delai: int):
    await context.send("Dépat dans ...")
    for i in range(delai, 0, -1):
        await context.send(i)
    await context.send("C'est parti !")
@bot.command()
async def repeter(context, message):
    await context.send(message)

if __name__ == '__main__':
    token = os.getenv("DISCORD_TOKEN")
    bot.run(token)
