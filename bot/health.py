"""Serveur HTTP de healthcheck, optionnel.

Il ne demarre que si la variable d'environnement PORT est definie. Un bot
Discord tourne tres bien en service worker Railway, sans port expose.
"""

from __future__ import annotations

import logging

from aiohttp import web

log = logging.getLogger(__name__)


async def _ok(_request: web.Request) -> web.Response:
    return web.Response(text="Le bot est en ligne !")


async def start_health_server(port: int | None) -> web.AppRunner | None:
    if port is None:
        log.info("PORT non defini : serveur de healthcheck desactive.")
        return None

    app = web.Application()
    app.router.add_get("/", _ok)
    app.router.add_get("/health", _ok)

    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", port).start()
    log.info("Healthcheck HTTP disponible sur le port %d.", port)
    return runner
