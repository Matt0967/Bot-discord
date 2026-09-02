"""/citation : envoie une citation motivante."""

from __future__ import annotations

import json
import logging
import random
from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands

log = logging.getLogger(__name__)

QUOTES_FILE = Path(__file__).resolve().parent.parent / "resources" / "quotes.json"


def load_quotes() -> list[str]:
    try:
        quotes = json.loads(QUOTES_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        log.exception("Impossible de lire %s", QUOTES_FILE)
        return []
    return [quote for quote in quotes if isinstance(quote, str) and quote.strip()]


class Citation(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.quotes = load_quotes()
        self._last: str | None = None
        log.info("%d citations chargees.", len(self.quotes))

    def pick(self) -> str | None:
        """Tire une citation, en evitant de repeter la precedente."""
        if not self.quotes:
            return None
        choices = [q for q in self.quotes if q != self._last] or self.quotes
        self._last = random.choice(choices)
        return self._last

    @app_commands.command(name="citation", description="Une citation motivante et inspirante")
    async def citation(self, interaction: discord.Interaction) -> None:
        quote = self.pick()
        if quote is None:
            await interaction.response.send_message(
                "Aucune citation disponible pour le moment.", ephemeral=True
            )
            return

        embed = discord.Embed(description=f"*{quote}*", color=discord.Color.blurple())
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Citation(bot))
