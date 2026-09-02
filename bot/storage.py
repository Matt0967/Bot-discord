"""Persistance simple des points d'experience dans un fichier JSON.

Le fichier est ecrit de maniere atomique (fichier temporaire + os.replace) et
les acces sont serialises par un verrou asyncio.

Attention : sur Railway le disque est ephemere. Pour conserver les points entre
deux deploiements, monte un volume et pointe DATA_DIR dessus (ex. /data).
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from pathlib import Path

log = logging.getLogger(__name__)


class ExpStore:
    """Points d'experience, indexes par serveur puis par membre."""

    def __init__(self, path: Path) -> None:
        self._path = path
        self._lock = asyncio.Lock()
        self._data: dict[str, dict[str, int]] = {}

    async def load(self) -> None:
        async with self._lock:
            self._data = await asyncio.to_thread(self._read)
        total = sum(len(members) for members in self._data.values())
        log.info("Points d'experience charges : %d membre(s) depuis %s.", total, self._path)

    def _read(self) -> dict[str, dict[str, int]]:
        try:
            raw = json.loads(self._path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return {}
        except (OSError, json.JSONDecodeError):
            log.exception("Fichier %s illisible, on repart d'un etat vide.", self._path)
            return {}
        if not isinstance(raw, dict):
            return {}
        return {
            str(guild): {str(user): int(points) for user, points in members.items()}
            for guild, members in raw.items()
            if isinstance(members, dict)
        }

    def _write(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self._path.with_suffix(self._path.suffix + ".tmp")
        tmp.write_text(json.dumps(self._data, indent=2), encoding="utf-8")
        os.replace(tmp, self._path)

    def get(self, guild_id: int, user_id: int) -> int:
        return self._data.get(str(guild_id), {}).get(str(user_id), 0)

    async def add(self, guild_id: int, user_id: int, points: int) -> int:
        """Ajoute des points et renvoie le nouveau total."""
        async with self._lock:
            members = self._data.setdefault(str(guild_id), {})
            total = members.get(str(user_id), 0) + points
            members[str(user_id)] = total
            await asyncio.to_thread(self._write)
            return total

    async def reset(self, guild_id: int, user_id: int) -> None:
        async with self._lock:
            self._data.setdefault(str(guild_id), {})[str(user_id)] = 0
            await asyncio.to_thread(self._write)
