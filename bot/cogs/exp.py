"""/exp : gestion des points d'experience des membres."""

from __future__ import annotations

import logging

import discord
from discord import ButtonStyle, app_commands, ui
from discord.ext import commands

from ..storage import ExpStore

log = logging.getLogger(__name__)

VIEW_TIMEOUT = 180

ACTIVITIES: dict[str, int] = {
    "Coder un projet personnel": 30,
    "Faire une seance de musculation": 40,
    "Dessiner ou creer une oeuvre": 20,
    "Lire un livre": 15,
    "Etudier une langue etrangere": 25,
    "Faire ses devoirs": 20,
    "Reviser une matiere scolaire": 25,
    "Faire une promenade pour se detendre": 10,
    "Passer 2h de Pomodoro": 50,
    "Passer 4h de Pomodoro": 100,
}


def is_admin(bot: commands.Bot, user: discord.abc.User) -> bool:
    """Admin declare dans ADMIN_IDS, ou administrateur du serveur."""
    if user.id in getattr(bot, "config").admin_ids:
        return True
    return isinstance(user, discord.Member) and user.guild_permissions.administrator


class BaseView(ui.View):
    """Vue reservee a son demandeur, qui se desactive a l'expiration."""

    def __init__(self, requester_id: int) -> None:
        super().__init__(timeout=VIEW_TIMEOUT)
        self.requester_id = requester_id
        self.message: discord.InteractionMessage | None = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.requester_id:
            await interaction.response.send_message(
                "Ce menu ne t'appartient pas. Lance `/exp` de ton cote.", ephemeral=True
            )
            return False
        return True

    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True
        if self.message is not None:
            try:
                await self.message.edit(view=self)
            except discord.HTTPException:
                pass


class MemberSelectView(BaseView):
    """Etape 1 (admins) : choisir le membre a gerer."""

    def __init__(self, store: ExpStore, requester_id: int) -> None:
        super().__init__(requester_id)
        self.store = store

    @ui.select(cls=ui.UserSelect, placeholder="Choisis un membre...", min_values=1, max_values=1)
    async def pick_member(self, interaction: discord.Interaction, select: ui.UserSelect) -> None:
        member = select.values[0]
        if isinstance(member, discord.Member) and member.bot:
            await interaction.response.send_message(
                "Les bots n'ont pas de points d'experience.", ephemeral=True
            )
            return

        view = ExpView(self.store, requester_id=self.requester_id, member=member, can_edit=True)
        total = self.store.get(interaction.guild_id, member.id)
        await interaction.response.edit_message(
            content=f"Points d'experience de {member.mention} : **{total}**", view=view
        )
        view.message = await interaction.original_response()


class ActivitySelect(ui.Select):
    """Etape 2 : choisir l'activite qui rapporte les points."""

    def __init__(self, store: ExpStore, member: discord.abc.User) -> None:
        super().__init__(
            placeholder="Choisis une activite...",
            min_values=1,
            max_values=1,
            options=[
                discord.SelectOption(label=name, description=f"+{points} points", value=name)
                for name, points in ACTIVITIES.items()
            ],
        )
        self.store = store
        self.member = member

    async def callback(self, interaction: discord.Interaction) -> None:
        activity = self.values[0]
        points = ACTIVITIES[activity]
        total = await self.store.add(interaction.guild_id, self.member.id, points)
        await interaction.response.edit_message(
            content=(
                f"➕ **{points} points** ajoutes a {self.member.mention} pour « {activity} ».\n"
                f"Total : **{total}** points."
            ),
            view=None,
        )


class ActivityView(BaseView):
    def __init__(self, store: ExpStore, requester_id: int, member: discord.abc.User) -> None:
        super().__init__(requester_id)
        self.add_item(ActivitySelect(store, member))


class ExpView(BaseView):
    """Panneau d'actions sur un membre."""

    def __init__(
        self,
        store: ExpStore,
        *,
        requester_id: int,
        member: discord.abc.User,
        can_edit: bool,
    ) -> None:
        super().__init__(requester_id)
        self.store = store
        self.member = member
        if not can_edit:
            # Un membre non administrateur peut seulement consulter son total.
            self.remove_item(self.add_points)
            self.remove_item(self.reset_points)

    @ui.button(label="Ajouter des points", style=ButtonStyle.primary, emoji="➕")
    async def add_points(self, interaction: discord.Interaction, _button: ui.Button) -> None:
        view = ActivityView(self.store, self.requester_id, self.member)
        await interaction.response.edit_message(
            content=f"Selectionne une activite pour {self.member.mention} :", view=view
        )
        view.message = await interaction.original_response()

    @ui.button(label="Verifier les points", style=ButtonStyle.secondary, emoji="🔎")
    async def check_points(self, interaction: discord.Interaction, _button: ui.Button) -> None:
        total = self.store.get(interaction.guild_id, self.member.id)
        await interaction.response.send_message(
            f"{self.member.mention} a **{total}** points d'experience.", ephemeral=True
        )

    @ui.button(label="Reinitialiser", style=ButtonStyle.danger, emoji="♻️")
    async def reset_points(self, interaction: discord.Interaction, _button: ui.Button) -> None:
        await self.store.reset(interaction.guild_id, self.member.id)
        await interaction.response.edit_message(
            content=f"♻️ Points d'experience de {self.member.mention} remis a zero.", view=None
        )


class ExpSystem(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.store: ExpStore = bot.exp_store

    @app_commands.command(name="exp", description="Gerer les points d'experience")
    @app_commands.guild_only()
    async def exp(self, interaction: discord.Interaction) -> None:
        if interaction.guild is None:
            await interaction.response.send_message(
                "Cette commande doit etre utilisee dans un serveur.", ephemeral=True
            )
            return

        if is_admin(self.bot, interaction.user):
            view: BaseView = MemberSelectView(self.store, interaction.user.id)
            content = "Selectionne un membre pour gerer ses points d'experience :"
        else:
            # Sans droits d'admin : consultation de ses propres points uniquement.
            view = ExpView(
                self.store,
                requester_id=interaction.user.id,
                member=interaction.user,
                can_edit=False,
            )
            total = self.store.get(interaction.guild_id, interaction.user.id)
            content = f"Tu as **{total}** points d'experience."

        await interaction.response.send_message(content, view=view, ephemeral=True)
        view.message = await interaction.original_response()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ExpSystem(bot))
