"""Point d'entree : `python -m bot`."""

from __future__ import annotations

import asyncio
import logging
import sys

import discord

from .client import StudyBot
from .config import Config, ConfigError
from .health import start_health_server

log = logging.getLogger("bot")


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stdout,
    )
    logging.getLogger("discord").setLevel(logging.WARNING)


async def run() -> None:
    config = Config.from_env()
    if not config.admin_ids:
        log.warning("ADMIN_IDS est vide : /exp restera limite au demandeur.")

    runner = await start_health_server(config.port)
    bot = StudyBot(config)
    try:
        async with bot:
            await bot.start(config.token)
    finally:
        if runner is not None:
            await runner.cleanup()


def main() -> int:
    configure_logging()
    try:
        asyncio.run(run())
    except ConfigError as error:
        log.error("%s", error)
        return 1
    except discord.LoginFailure:
        log.error("Token Discord refuse. Verifie DISCORD_TOKEN.")
        return 1
    except discord.PrivilegedIntentsRequired:
        log.error(
            "Intents privilegies desactives. Active 'Server Members' et "
            "'Message Content' dans le Developer Portal > Bot."
        )
        return 1
    except KeyboardInterrupt:
        log.info("Arret demande.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
