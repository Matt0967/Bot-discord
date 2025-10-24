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
token = os.getenv('DISCORD_TOKEN')

ADMIN_IDS = [802925075535495177]  # Remplacer par ton ID Discord

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Dictionary to store user experience points
user_exp = {}
activities_exp = {
    "Coder un projet personnel": 30,
    "Faire une séance de musculation": 40,
    "Dessiner ou créer une œuvre": 20,
    "Lire un livre": 15,
    "Étudier une langue étrangère": 25,
    "Faire ses devoirs": 20,
    "Réviser une matière scolaire": 25,
    "Faire une promenade pour se détendre": 10,
    "Passer 2h de Pomodoro": 50,
    "Passer 4h de Pomodoro": 100,
}

class UserSelect(ui.Select):
    def __init__(self, members: list[discord.Member], requester: discord.User):
        options = [
            discord.SelectOption(label=member.display_name, description=f"ID: {member.id}", value=str(member.id))
            for member in members
        ]
        super().__init__(placeholder="Choisissez un utilisateur...", min_values=1, max_values=1, options=options)
        self.requester = requester

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id not in ADMIN_IDS and interaction.user != self.requester:
            await interaction.response.send_message("Vous ne pouvez pas utiliser ce menu.", ephemeral=True)
            return
        member_id = int(self.values[0])
        guild = interaction.guild
        member = guild.get_member(member_id)
        if member is None:
            await interaction.response.send_message("Utilisateur non trouvé.", ephemeral=True)
            return
        view = ExpView(member)
        await interaction.response.edit_message(content=f"Gérer les points d'expérience pour {member.mention} :", view=view)

class UserSelectView(ui.View):
    def __init__(self, members: list[discord.Member], requester: discord.User):
        super().__init__(timeout=60)
        self.add_item(UserSelect(members, requester))

class ActivitySelect(ui.Select):
    def __init__(self, user: discord.User):
        options = [
            discord.SelectOption(label=activity, description=f"Ajouter {points} points", value=activity)
            for activity, points in activities_exp.items()
        ]
        super().__init__(placeholder="Choisissez une activité...", min_values=1, max_values=1, options=options)
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id not in ADMIN_IDS and interaction.user != self.user:
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
        if interaction.user.id not in ADMIN_IDS and interaction.user != self.user:
            await interaction.response.send_message("Vous ne pouvez pas utiliser ces boutons.", ephemeral=True)
            return
        select = ActivitySelect(self.user)
        view = ui.View()
        view.add_item(select)
        await interaction.response.edit_message(content="Sélectionnez une activité pour ajouter des points :", view=view)

    @ui.button(label="Vérifier les points", style=ButtonStyle.secondary)
    async def check_points(self, interaction: discord.Interaction, button: ui.Button):
        if interaction.user.id not in ADMIN_IDS and interaction.user != self.user:
            await interaction.response.send_message("Vous ne pouvez pas utiliser ces boutons.", ephemeral=True)
            return
        exp_points = user_exp.get(self.user.id, 0)
        await interaction.response.send_message(f"{self.user.mention} a {exp_points} points d'expérience.", ephemeral=True)

    @ui.button(label="Réinitialiser", style=ButtonStyle.danger)
    async def reset_points(self, interaction: discord.Interaction, button: ui.Button):
        if interaction.user.id not in ADMIN_IDS and interaction.user != self.user:
            await interaction.response.send_message("Vous ne pouvez pas utiliser ces boutons.", ephemeral=True)
            return
        user_exp[self.user.id] = 0
        await interaction.response.send_message(f"Les points d'expérience de {self.user.mention} ont été réinitialisés.", ephemeral=True)

@bot.tree.command(name="exp", description="Gérer les points d'expérience")
async def exp(interaction: discord.Interaction):
    guild = interaction.guild
    if guild is None:
        await interaction.response.send_message("Cette commande doit être utilisée dans un serveur.", ephemeral=True)
        return
    members = [member for member in guild.members if not member.bot][:25]
    if not members:
        await interaction.response.send_message("Aucun utilisateur disponible pour la sélection.", ephemeral=True)
        return
    view = UserSelectView(members, interaction.user)
    await interaction.response.send_message("Sélectionnez un utilisateur pour gérer ses points d’expérience :", view=view, ephemeral=True)

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
