import discord
from discord.ext import commands
import random  
from discord import app_commands
import asyncio
from discord import ButtonStyle, ui
import datetime
import os 
from dotenv import load_dotenv
load_dotenv()
token=os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.tree.command(name="pomodoro", description="Démarrer un timer Pomodoro")
async def pomodoro(interaction: discord.Interaction):
    class PomodoroView(ui.View):
        def __init__(self):
            super().__init__(timeout=5)  # 5 secondes pour choisir
            self.choice = None

        @ui.button(label="25-5", style=ButtonStyle.primary, emoji="⏱️")
        async def pomodoro_25(self, button: ui.Button, button_interaction: discord.Interaction):
            self.choice = (25, 5)  # 25 minutes travail, 5 minutes pause
            for item in self.children:
                item.disabled = True
            await button_interaction.response.defer()
            await self.message.edit(view=self)
            self.stop()

        @ui.button(label="50-10", style=ButtonStyle.primary, emoji="⌚")
        async def pomodoro_50(self, button: ui.Button, button_interaction: discord.Interaction):
            self.choice = (50, 10)  # 50 minutes travail, 10 minutes pause
            for item in self.children:
                item.disabled = True
            await button_interaction.response.defer()
            await self.message.edit(view=self)
            self.stop()

    async def create_progress_bar(current, total):
        filled = "🟦"
        empty = "⬜"
        progress = int((current / total) * 10)
        return filled * progress + empty * (10 - progress)

    async def start_timer(duration_minutes: int, message: str, interaction: discord.Interaction, is_work=True):
        remaining_minutes = duration_minutes
        
        # Message initial
        status_message = await interaction.channel.send(
            f"{'🎯' if is_work else '☕'} **Session {message}**\n"
            f"⏱️ Durée : {duration_minutes} minutes\n"
            f"{await create_progress_bar(duration_minutes, duration_minutes)}\n"
            f"👤 Session de {interaction.user.mention}"
        )

        # Boucle de mise à jour (toutes les minutes)
        while remaining_minutes > 0:
            await asyncio.sleep(60)  # Attendre 1 minute
            remaining_minutes -= 1
            
            # Mettre à jour le message toutes les minutes
            if remaining_minutes > 0:
                try:
                    progress_bar = await create_progress_bar(remaining_minutes, duration_minutes)
                    await status_message.edit(content=(
                        f"{'🎯' if is_work else '☕'} **Session {message}**\n"
                        f"⏱️ Il reste : {remaining_minutes} minutes\n"
                        f"{progress_bar}\n"
                        f"👤 Session de {interaction.user.mention}"
                    ))
                except discord.NotFound:
                    break

        # Message de fin de phase
        try:
            await status_message.edit(content=(
                f"{'✅' if is_work else '🔔'} **{message.capitalize()} terminé !**\n"
                f"{'🎯 C\'est l\'heure de la pause!' if is_work else '☕ Fin de la pause!'}\n"
                f"👤 Session de {interaction.user.mention}"
            ))
        except:
            pass

    # Interface initiale
    view = PomodoroView()
    initial_response = await interaction.response.send_message(
        "🍅 Choisissez votre timer Pomodoro :",
        view=view,
        ephemeral=True
    )
    
    view.message = await interaction.original_response()
    await view.wait()
    
    if view.choice is None:
        await interaction.followup.send(
            "❌ Temps de sélection écoulé. Réessayez avec /pomodoro",
            ephemeral=True
        )
        return

    work_time, break_time = view.choice

    # Annonce de début de session
    await interaction.channel.send(
        f"🎯 **Nouvelle session Pomodoro {work_time}-{break_time}**\n"
        f"👤 {interaction.user.mention} démarre une session !\n"
        f"💪 Bon courage !"
    )

    # Timer de travail
    await start_timer(work_time, "travail", interaction, True)

    # Notification de transition
    await interaction.channel.send(
        f"⏰ **Transition !**\n"
        f"👤 {interaction.user.mention}, la phase de travail est terminée.\n"
        f"☕ Début de la pause de {break_time} minutes."
    )

    # Timer de pause
    await start_timer(break_time, "pause", interaction, False)

    # Message de fin de session
    await interaction.channel.send(
        f"✨ **Session Pomodoro complétée !**\n"
        f"👏 Bravo {interaction.user.mention} !\n"
        f"🆕 Tapez `/pomodoro` pour une nouvelle session"
    )

@bot.tree.command(name="citation", description="une Citation Motivante - Inspirante")
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