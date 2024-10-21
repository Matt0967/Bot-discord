import discord 
from discord.ext import commands 

token = "MTI4NzA4ODYxODM2MzY4Njk3Mg.GAAk2I.DPnDCNRPJWosVv5EaPpBSUfDqt-u6POnYTVD4Y"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents )

@bot.tree.command()
async def mutiplication(interaction: discord.Interaction, a: int, b: int):
    await interaction.response.send_message(f"Le résultat de {a} x {b} est {a *b}")
@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} commandes ont été synchronisées")
    except Exception as e:
        print(e)

async def main():
    await bot.start(token)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())