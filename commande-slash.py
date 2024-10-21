import discord
from discord.ext import commands
import random  # L'import de random doit être au début

# Remplace ton token par une variable d'environnement pour plus de sécurité
token = "MTI4NzA4ODYxODM2MzY4Njk3Mg.GJHyfW.7oGzMiBeJG5vHChVAPEksB2Nx3JvACqAnrwp9M"

# Utilisation des intents par défaut, ou change selon tes besoins
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Commande slash pour la multiplication
@bot.tree.command(name="multiplication")
async def multiplication(interaction: discord.Interaction, a: int, b: int):
    await interaction.response.send_message(f"Le résultat de {a} x {b} est {a * b}")

# Commande slash pour afficher une citation aléatoire
@bot.tree.command(name="citation")
async def citation(interaction: discord.Interaction):
    quotes = [
        "La vie est un mystère qu'il faut vivre, et non un problème à résoudre. - Gandhi",
        "Le plus grand risque est de ne prendre aucun risque. - Mark Zuckerberg",
        "Le succès, c'est se promener d'échecs en échecs tout en restant motivé. - Winston Churchill",
        "Votre temps est limité, ne le gâchez pas en vivant la vie de quelqu'un d'autre. - Steve Jobs"
    ]
    quote = random.choice(quotes)
    await interaction.response.send_message(quote)

# Quand le bot est prêt et connecté à Discord
@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    try:
        # Synchroniser les commandes avec Discord
        synced = await bot.tree.sync()
        print(f"{len(synced)} commandes ont été synchronisées")
    except Exception as e:
        print(f"Erreur lors de la synchronisation des commandes : {e}")

# Fonction principale pour démarrer le bot
async def main():
    await bot.start(token)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
