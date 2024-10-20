import discord
from discord.ext import commands 
token = "MTI4NzA4ODYxODM2MzY4Njk3Mg.GAAk2I.DPnDCNRPJWosVv5EaPpBSUfDqt-u6POnYTVD4Y"

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
    bot.run(token=token)