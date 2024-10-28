import discord
from discord.ext import commands
import random  
from discord import app_commands
import asyncio
from discord import ButtonStyle, ui

token = "MTI4NzA4ODYxODM2MzY4Njk3Mg.GJHyfW.7oGzMiBeJG5vHChVAPEksB2Nx3JvACqAnrwp9M"

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


 
@bot.tree.command(name="pomodoro")
async def pomodoro(interaction: discord.Interaction):
    # Envoyer un message initial pour confirmer que l'interaction est en cours de traitement
    await interaction.response.send_message("Veuillez choisir un timer Pomodoro...", ephemeral=True)

    # Création des boutons pour le choix
    class PomodoroView(ui.View):
        def __init__(self):
            super().__init__()
            self.choice = None  # Initialise la variable de choix de l'utilisateur

        @ui.button(label="25-5", style=ButtonStyle.primary)
        async def pomodoro_25(self, button: ui.Button, interaction: discord.Interaction):
            self.choice = (25, 5)
            await interaction.response.send_message("Vous avez choisi le Pomodoro 25-5. Travaillez pendant 25 minutes.", ephemeral=True)
            self.stop()

        @ui.button(label="50-10", style=ButtonStyle.primary)
        async def pomodoro_50(self, button: ui.Button, interaction: discord.Interaction):
            self.choice = (50, 10)
            await interaction.response.send_message("Vous avez choisi le Pomodoro 50-10. Travaillez pendant 50 minutes.", ephemeral=True)
            self.stop()

    view = PomodoroView()
    # Envoyer un message avec les boutons pour le choix
    await interaction.followup.send("Choisissez votre timer Pomodoro :", view=view)
    await view.wait()  # Attend la réponse de l'utilisateur

    if view.choice is None:
        return await interaction.followup.send("Vous n'avez pas fait de choix. Veuillez réessayer.")

    work_time, break_time = view.choice

    async def timer(duration, message):
        for remaining in range(duration, 0, -10):
            await asyncio.sleep(600)  # 10 minutes
            await interaction.followup.send(f"{remaining} minutes restantes pour {message}.")

    # Lancer le timer de travail
    await timer(work_time, "le temps de travail")
    await interaction.followup.send("Travail terminé ! Prenez une pause.")

    # Lancer le timer de pause
    await timer(break_time, "le temps de pause")
    await interaction.followup.send("Pause terminée ! Reprenez quand vous êtes prêt.")

@bot.tree.command(name="citation")
async def citation(interaction: discord.Interaction):
    quotes = [
        "La vie est un mystère qu'il faut vivre, et non un problème à résoudre. - Gandhi",
        "Le plus grand risque est de ne prendre aucun risque. - Mark Zuckerberg",
        "Le succès, c'est se promener d'échecs en échecs tout en restant motivé. - Winston Churchill",
        "Votre temps est limité, ne le gâchez pas en vivant la vie de quelqu'un d'autre. - Steve Jobs"
        "Le succès n'est pas la clé du bonheur. Le bonheur est la clé du succès. Si vous aimez ce que vous faites, vous réussirez. – Albert Schweitzer"
        "Le seul endroit où le succès vient avant le travail est dans le dictionnaire – Vidal Sassoon"
        "Ne rêve pas ta vie, vis ton rêve – Anonyme"
        "Les grandes choses ne sont jamais faites par une seule personne, elles sont faites par une équipe – Steve Jobs"
        "Le plus grand échec est de ne pas avoir le courage d'oser – Abbé Pierre"
        "Il ne s’agit pas d’être le meilleur, mais d’être meilleur que la personne que nous étions hier – Anonyme"
        "La seule limite à notre épanouissement de demain sera nos doutes d’aujourd’hui – Franklin D. Roosevelt"
        "Le succès consiste à aller d'échec en échec sans perdre son enthousiasme – Winston Churchill"
        "Vous ne pouvez pas changer votre passé, mais vous pouvez ruiner le présent en vous inquiétant de l'avenir – Anonyme"
        "Les difficultés préparent les gens ordinaires à un destin extraordinaire – C.S. Lewis"
        "Le courage n'est pas l'absence de peur, mais la capacité de vaincre ce qui fait peur – Nelson Mandela"

    ]
    quote = random.choice(quotes)
    await interaction.response.send_message(quote)

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    try:
        
        synced = await bot.tree.sync()
        print(f"{len(synced)} commandes ont été synchronisées")
    except Exception as e:
        print(f"Erreur lors de la synchronisation des commandes : {e}")


async def main():
    await bot.start(token)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())