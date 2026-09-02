"""Construction et demarrage du client Discord."""

from __future__ import annotations

import logging

import discord
from discord.ext import commands

from .config import Config
from .storage import ExpStore

log = logging.getLogger(__name__)

EXTENSIONS = (
    "bot.cogs.citation",
    "bot.cogs.pomodoro",
    "bot.cogs.exp",
)


class StudyBot(commands.Bot):
    def __init__(self, config: Config) -> None:
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents, help_command=None)

        self.config = config
        self.exp_store = ExpStore(config.data_dir / "exp.json")

    async def setup_hook(self) -> None:
        """Appele par discord.py avant la connexion à la gateway."""
        await self.exp_store.load()

        for extension in EXTENSIONS:
            try:
                await self.load_extension(extension)
                log.info("Extension %s chargee.", extension)
            except Exception:
                log.exception("Echec du chargement de %s", extension)

        try:
            synced = await self.tree.sync()
            log.info("%d commande(s) slash synchronisee(s).", len(synced))
        except discord.HTTPException:
            log.exception("Erreur de synchronisation des commandes slash")

    async def on_ready(self) -> None:
        log.info("Connecte en tant que %s (%d serveur(s)).", self.user, len(self.guilds))

    def is_admin(self, user: discord.abc.User) -> bool:
        return user.id in self.config.admin_ids
