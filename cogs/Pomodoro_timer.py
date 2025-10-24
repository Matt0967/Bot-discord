import discord
from discord.ext import commands
import random  
from discord import app_commands
import asyncio
from discord import ButtonStyle, ui
import datetime
import os 
from dotenv import load_dotenv

class Pomodoro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    @app_commands.command(name="pomodoro", description="Démarrer un timer Pomodoro")
    async def pomodoro(self, interaction: discord.Interaction):
        class PomodoroView(ui.View):
            def __init__(self):
                super().__init__(timeout=3)  # 3 secondes pour choisir
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
                    f"""{"🎯 C'est l'heure de la pause!" if is_work else "☕ Fin de la pause!"}
"""
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
    # Dictionary to store experience points for activities

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

async def setup(bot):
    await bot.add_cog(Pomodoro(bot))
