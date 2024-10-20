import discord 

token = "MTI4NzA4ODYxODM2MzY4Njk3Mg.GAAk2I.DPnDCNRPJWosVv5EaPpBSUfDqt-u6POnYTVD4Y"

client = discord.Client(intents=discord.Intents.all())

client.run(token=token)