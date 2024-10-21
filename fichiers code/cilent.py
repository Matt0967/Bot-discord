import discord 

token = "MTI4NzA4ODYxODM2MzY4Njk3Mg.GJHyfW.7oGzMiBeJG5vHChVAPEksB2Nx3JvACqAnrwp9M"

client = discord.Client(intents=discord.Intents.all())

client.run(token=token)