import discord 
from discord.ext import commands 

token = "MTI4NzA4ODYxODM2MzY4Njk3Mg.GAAk2I.DPnDCNRPJWosVv5EaPpBSUfDqt-u6POnYTVD4Y"
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents )



def main():
    bot.run(token)

if __name__ == '__main__':
    main()