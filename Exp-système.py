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
token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Dictionary to store user experience points
user_exp = {}
activities_exp = {
    "coding": 30,
    "muscu": 40,
    "dessiner": 20,
    "lire": 15,
    "langague": 25,
}

class ActivitySelect(ui.Select):
    def __init__(self, user: discord.User):
        options = [
            discord.SelectOption(label=activity, description=f"Ajouter {points} points", value=activity)
            for activity, points in activities_exp.items()
        ]
        super().__init__(placeholder="Choisissez une activité...", min_values=1, max_values=1, options=options)
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.user:
            await interaction.response.send_message("Vous ne pouvez pas utiliser ce menu.", ephemeral=True)
            return
        activity = self.values[0]
        points = activities_exp.get(activity, 0)
        if self.user.id not in user_exp:
            user_exp[self.user.id] = 0
        user_exp[self.user.id] += points
        await interaction.response.edit_message(content=f"{points} points d'expérience ajoutés à {self.user.mention} pour {activity}.", view=None)

class ExpView(ui.View):
    def __init__(self, user: discord.User):
        super().__init__(timeout=60)
        self.user = user

    @ui.button(label="Ajouter des points", style=ButtonStyle.primary)
    async def add_points(self, interaction: discord.Interaction, button: ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("Vous ne pouvez pas utiliser ces boutons.", ephemeral=True)
            return
        select = ActivitySelect(self.user)
        view = ui.View()
        view.add_item(select)
        await interaction.response.edit_message(content="Sélectionnez une activité pour ajouter des points :", view=view)

    @ui.button(label="Vérifier les points", style=ButtonStyle.secondary)
    async def check_points(self, interaction: discord.Interaction, button: ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("Vous ne pouvez pas utiliser ces boutons.", ephemeral=True)
            return
        exp_points = user_exp.get(self.user.id, 0)
        await interaction.response.send_message(f"{self.user.mention} a {exp_points} points d'expérience.", ephemeral=True)

    @ui.button(label="Réinitialiser", style=ButtonStyle.danger)
    async def reset_points(self, interaction: discord.Interaction, button: ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("Vous ne pouvez pas utiliser ces boutons.", ephemeral=True)
            return
        user_exp[self.user.id] = 0
        await interaction.response.send_message(f"Les points d'expérience de {self.user.mention} ont été réinitialisés.", ephemeral=True)

@bot.tree.command(name="exp", description="Gérer les points d'expérience")
async def exp(interaction: discord.Interaction):
    view = ExpView(interaction.user)
    await interaction.response.send_message("Que souhaitez-vous faire ?", view=view, ephemeral=True)

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    try:
        
        synced = await bot.tree.sync()
        print(f"{len(synced)} commandes ont été synchronisées")
    except Exception as e:
        print(f"Erreur lors de la synchronisation des commandes : {e}")

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    if message.author.id not in user_exp:
        user_exp[message.author.id] = 0
    user_exp[message.author.id] += 1
    await bot.process_commands(message)

async def main():
    await bot.start(token)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
