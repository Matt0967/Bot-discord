import discord
from discord.ext import commands
import random  
from discord import app_commands
import asyncio
from discord import ButtonStyle, ui

token = "MTI4NzA4ODYxODM2MzY4Njk3Mg.GJHyfW.7oGzMiBeJG5vHChVAPEksB2Nx3JvACqAnrwp9M"

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.tree.command(name="pomodoro", description="Démarrer un timer Pomodoro")
async def pomodoro(interaction: discord.Interaction):
    class PomodoroView(ui.View):
        def __init__(self):
            super().__init__(timeout=180)  # Timeout de 3 minutes
            self.choice = None

        @ui.button(label="25-5", style=ButtonStyle.primary)
        async def pomodoro_25(self, button: ui.Button, button_interaction: discord.Interaction):
            self.choice = (25, 5)
            # Désactiver tous les boutons après le choix
            for item in self.children:
                item.disabled = True
            await button_interaction.response.edit_message(view=self)
            self.stop()

        @ui.button(label="50-10", style=ButtonStyle.primary)
        async def pomodoro_50(self, button: ui.Button, button_interaction: discord.Interaction):
            self.choice = (50, 10)
            # Désactiver tous les boutons après le choix
            for item in self.children:
                item.disabled = True
            await button_interaction.response.edit_message(view=self)
            self.stop()

        async def on_timeout(self):
            # Désactiver les boutons si l'utilisateur ne répond pas
            for item in self.children:
                item.disabled = True
            try:
                await self.message.edit(content="Le temps de sélection est écoulé.", view=self)
            except:
                pass

    async def start_timer(duration_minutes: int, message: str, interaction: discord.Interaction):
        remaining_minutes = duration_minutes
        
        # Envoyer le message initial
        timer_message = await interaction.followup.send(
            f"⏱️ {message}\nTemps restant: {remaining_minutes} minutes",
            ephemeral=True
        )

        # Mettre à jour toutes les minutes
        while remaining_minutes > 0:
            await asyncio.sleep(60)  # Attendre 1 minute
            remaining_minutes -= 1
            
            if remaining_minutes > 0:
                try:
                    await timer_message.edit(
                        content=f"⏱️ {message}\nTemps restant: {remaining_minutes} minutes"
                    )
                except discord.NotFound:
                    break  # Message supprimé, arrêter le timer

    # Créer et envoyer la vue avec les boutons
    view = PomodoroView()
    initial_message = await interaction.response.send_message(
        "🍅 Choisissez votre timer Pomodoro :",
        view=view,
        ephemeral=True
    )
    
    # Attendre le choix de l'utilisateur
    await view.wait()
    
    if view.choice is None:
        await interaction.followup.send(
            "❌ Vous n'avez pas fait de choix dans le temps imparti.",
            ephemeral=True
        )
        return

    work_time, break_time = view.choice

    # Démarrer la session Pomodoro
    await interaction.followup.send(
        f"🎯 Session Pomodoro {work_time}-{break_time} démarrée !",
        ephemeral=True
    )

    # Phase de travail
    await start_timer(work_time, "📚 Phase de travail en cours", interaction)
    await interaction.followup.send("⏰ Temps de travail terminé !", ephemeral=True)

    # Phase de pause
    await start_timer(break_time, "☕ Phase de pause en cours", interaction)
    await interaction.followup.send(
        "✨ Session Pomodoro terminée ! Vous pouvez en démarrer une nouvelle avec /pomodoro",
        ephemeral=True
    )

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