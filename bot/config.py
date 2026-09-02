"""Configuration lue depuis l'environnement (fichier .env en local)."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


class ConfigError(RuntimeError):
    """Configuration absente ou invalide."""


def _parse_ids(raw: str) -> frozenset[int]:
    """\"123, 456;789\" -> {123, 456, 789}."""
    ids = set()
    for part in raw.replace(";", ",").split(","):
        part = part.strip()
        if part.isdigit():
            ids.add(int(part))
    return frozenset(ids)


@dataclass(frozen=True)
class Config:
    token: str
    admin_ids: frozenset[int]
    data_dir: Path
    port: int | None

    @classmethod
    def from_env(cls) -> "Config":
        load_dotenv()

        token = os.getenv("DISCORD_TOKEN", "").strip()
        if not token:
            raise ConfigError(
                "DISCORD_TOKEN manquant. En local, renseigne-le dans .env ; "
                "sur Railway, ajoute-le dans l'onglet Variables du service."
            )

        raw_port = os.getenv("PORT", "").strip()
        if raw_port and not raw_port.isdigit():
            raise ConfigError(f"PORT invalide : {raw_port!r} (entier attendu).")

        return cls(
            token=token,
            admin_ids=_parse_ids(os.getenv("ADMIN_IDS", "")),
            data_dir=Path(os.getenv("DATA_DIR", "data")),
            port=int(raw_port) if raw_port else None,
        )
