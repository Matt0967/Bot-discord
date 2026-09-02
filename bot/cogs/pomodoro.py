"""/pomodoro : minuteur Pomodoro avec barre de progression."""

from __future__ import annotations

import asyncio
import logging
import time

import discord
from discord import ButtonStyle, app_commands, ui
from discord.ext import commands

log = logging.getLogger(__name__)

PRESETS: dict[str, tuple[int, int]] = {
    "25-5": (25, 5),
    "50-10": (50, 10),
}
CHOICE_TIMEOUT = 120  # secondes pour choisir un preset
BAR_LENGTH = 10
UPDATE_INTERVAL = 60  # secondes entre deux mises a jour du message


def progress_bar(elapsed: float, total: float) -> str:
    ratio = 0.0 if total <= 0 else min(max(elapsed / total, 0.0), 1.0)
    filled = round(ratio * BAR_LENGTH)
    return "🟦" * filled + "⬜" * (BAR_LENGTH - filled)


def format_remaining(seconds: float) -> str:
    minutes, secs = divmod(max(int(seconds), 0), 60)
    if minutes and secs:
        return f"{minutes} min {secs:02d} s"
    if minutes:
        return f"{minutes} min"
    return f"{secs} s"


class PresetView(ui.View):
    """Boutons de selection du preset. `choice` est rempli au clic."""

    def __init__(self, owner_id: int) -> None:
        super().__init__(timeout=CHOICE_TIMEOUT)
        self.owner_id = owner_id
        self.choice: tuple[int, int] | None = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message(
                "Ces boutons ne sont pas pour toi. Lance `/pomodoro` de ton cote.",
                ephemeral=True,
            )
            return False
        return True

    async def _select(self, interaction: discord.Interaction, preset: str) -> None:
        self.choice = PRESETS[preset]
        for item in self.children:
            item.disabled = True
        await interaction.response.edit_message(
            content=f"🍅 Preset **{preset}** selectionne, c'est parti !", view=self
        )
        self.stop()

    # discord.py 2.x passe (interaction, button) — dans cet ordre.
    @ui.button(label="25-5", style=ButtonStyle.primary, emoji="⏱️")
    async def preset_25(self, interaction: discord.Interaction, _button: ui.Button) -> None:
        await self._select(interaction, "25-5")

    @ui.button(label="50-10", style=ButtonStyle.primary, emoji="⌚")
    async def preset_50(self, interaction: discord.Interaction, _button: ui.Button) -> None:
        await self._select(interaction, "50-10")


class Pomodoro(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self._sessions: dict[int, asyncio.Task] = {}

    async def cog_unload(self) -> None:
        for task in list(self._sessions.values()):
            task.cancel()

    @app_commands.command(name="pomodoro", description="Demarrer un minuteur Pomodoro")
    async def pomodoro(self, interaction: discord.Interaction) -> None:
        channel = interaction.channel
        if channel is None or not isinstance(channel, discord.abc.Messageable):
            await interaction.response.send_message(
                "Cette commande doit etre utilisee dans un salon textuel.", ephemeral=True
            )
            return

        existing = self._sessions.get(interaction.user.id)
        if existing is not None and not existing.done():
            await interaction.response.send_message(
                "Tu as deja une session Pomodoro en cours. Attends la fin avant d'en lancer une autre.",
                ephemeral=True,
            )
            return

        view = PresetView(interaction.user.id)
        await interaction.response.send_message(
            "🍅 Choisis ton minuteur Pomodoro :", view=view, ephemeral=True
        )

        if await view.wait():  # True = timeout atteint
            for item in view.children:
                item.disabled = True
            await interaction.edit_original_response(
                content="❌ Temps de selection ecoule. Relance `/pomodoro`.", view=view
            )
            return

        work, rest = view.choice
        task = asyncio.create_task(
            self._run_session(channel, interaction.user, work, rest),
            name=f"pomodoro-{interaction.user.id}",
        )
        self._sessions[interaction.user.id] = task
        task.add_done_callback(lambda _: self._sessions.pop(interaction.user.id, None))

    async def _run_session(
        self,
        channel: discord.abc.Messageable,
        user: discord.abc.User,
        work: int,
        rest: int,
    ) -> None:
        try:
            await channel.send(
                f"🎯 **Nouvelle session Pomodoro {work}-{rest}**\n"
                f"👤 {user.mention} demarre une session !\n"
                f"💪 Bon courage !"
            )
            await self._run_phase(channel, user, work, is_work=True)
            await channel.send(
                f"⏰ **Transition !**\n"
                f"👤 {user.mention}, la phase de travail est terminee.\n"
                f"☕ Debut de la pause de {rest} minutes."
            )
            await self._run_phase(channel, user, rest, is_work=False)
            await channel.send(
                f"✨ **Session Pomodoro completee !**\n"
                f"👏 Bravo {user.mention} !\n"
                f"🆕 Tape `/pomodoro` pour une nouvelle session."
            )
        except asyncio.CancelledError:
            raise
        except discord.Forbidden:
            log.warning("Permissions insuffisantes pour ecrire dans %s.", channel)
        except discord.HTTPException:
            log.exception("Erreur Discord pendant la session de %s", user)

    async def _run_phase(
        self,
        channel: discord.abc.Messageable,
        user: discord.abc.User,
        minutes: int,
        *,
        is_work: bool,
    ) -> None:
        label = "travail" if is_work else "pause"
        icon = "🎯" if is_work else "☕"
        total = minutes * 60
        # Deadline monotone : pas de derive cumulee sur une longue session.
        deadline = time.monotonic() + total
        end_at = discord.utils.utcnow().timestamp() + total

        message = await channel.send(
            f"{icon} **Session {label}**\n"
            f"⏱️ Duree : {minutes} minutes — fin <t:{int(end_at)}:R>\n"
            f"{progress_bar(0, total)}\n"
            f"👤 Session de {user.mention}"
        )

        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            await asyncio.sleep(min(UPDATE_INTERVAL, remaining))

            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            try:
                await message.edit(
                    content=(
                        f"{icon} **Session {label}**\n"
                        f"⏱️ Il reste : {format_remaining(remaining)}\n"
                        f"{progress_bar(total - remaining, total)}\n"
                        f"👤 Session de {user.mention}"
                    )
                )
            except discord.NotFound:
                return  # message supprime : on laisse la session se terminer en silence
            except discord.HTTPException:
                log.warning("Mise a jour du minuteur ignoree.", exc_info=True)

        closing = "C'est l'heure de la pause !" if is_work else "Fin de la pause !"
        try:
            await message.edit(
                content=(
                    f"{'✅' if is_work else '🔔'} **{label.capitalize()} termine !**\n"
                    f"{icon} {closing}\n"
                    f"{progress_bar(total, total)}\n"
                    f"👤 Session de {user.mention}"
                )
            )
        except discord.HTTPException:
            pass


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Pomodoro(bot))
