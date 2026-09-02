# Discord Bot

Bot Discord ecrit en Python avec `discord.py`, pense pour un deploiement sur Railway.
Trois fonctionnalites : citations motivantes, minuteur Pomodoro, points d'experience.

---

## FR

### Fonctionnalites

| Commande | Description |
| --- | --- |
| `/citation` | Envoie une citation motivante tiree au hasard (45 citations, sans repetition immediate). |
| `/pomodoro` | Lance une session Pomodoro `25-5` ou `50-10`, avec barre de progression mise a jour chaque minute, message de pause et message de fin. |
| `/exp` | Gere les points d'experience des membres du serveur. |

Details `/pomodoro` :

- une seule session active par membre a la fois
- le minuteur tourne en tache de fond : la commande ne bloque pas le bot
- horodatage Discord (`fin dans ...`) et barre de progression `🟦⬜`

Details `/exp` :

- **administrateurs** (listes dans `ADMIN_IDS` ou administrateurs du serveur) :
  choisissent un membre, ajoutent des points selon une activite, consultent, reinitialisent
- **autres membres** : consultation de leurs propres points uniquement
- les points sont **persistes** dans `DATA_DIR/exp.json`, par serveur et par membre

### Structure du projet

```text
.
├── bot/
│   ├── __init__.py
│   ├── __main__.py         # point d'entree : python -m bot
│   ├── client.py           # sous-classe commands.Bot, chargement des cogs, sync des slash
│   ├── config.py           # lecture et validation des variables d'environnement
│   ├── storage.py          # persistance JSON des points d'experience
│   ├── health.py           # serveur HTTP de healthcheck (optionnel)
│   ├── cogs/
│   │   ├── citation.py
│   │   ├── pomodoro.py
│   │   └── exp.py
│   └── resources/
│       └── quotes.json     # les citations, sorties du code
├── .env.example
├── .python-version
├── Procfile
├── railway.json
└── requirements.txt
```

Le dossier `DATA_DIR` (par defaut `data/`) est cree au premier ajout de points ; il est ignore par Git.

### Prerequis

- Python 3.9 ou plus recent (Railway utilise 3.11 via `.python-version`)
- un bot cree dans le [Discord Developer Portal](https://discord.com/developers/applications)
- les intents **Message Content** et **Server Members** actives dans l'onglet Bot

### Variables d'environnement

| Variable | Obligatoire | Defaut | Description |
| --- | --- | --- | --- |
| `DISCORD_TOKEN` | oui | — | Token du bot. |
| `ADMIN_IDS` | recommande | vide | IDs Discord des administrateurs, separes par des virgules. Les administrateurs du serveur sont reconnus automatiquement. |
| `DATA_DIR` | non | `data` | Dossier de stockage des points d'experience. |
| `PORT` | non | vide | Si defini, demarre un healthcheck HTTP sur ce port. |

### Installation locale

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # puis renseigne DISCORD_TOKEN et ADMIN_IDS
python -m bot
```

### Deploiement sur Railway

1. Pousser le depot sur GitHub.
2. Sur [railway.app](https://railway.app) : **New Project > Deploy from GitHub repo**, selectionner ce depot.
3. Onglet **Variables**, ajouter :

   ```text
   DISCORD_TOKEN=votre_token_discord
   ADMIN_IDS=123456789012345678
   ```

4. Deployer. Railway detecte Python via Nixpacks, installe `requirements.txt`
   et lance `python -m bot` (voir `railway.json` et `Procfile`).

Bon a savoir :

- Le bot est un **worker** : ni domaine public ni port expose. Ne definis `PORT`
  que si tu veux exposer le healthcheck HTTP.
- Le disque Railway est **ephemere**. Pour conserver les points d'experience entre
  deux deploiements : **Settings > Volumes**, monter un volume sur `/data`, puis
  ajouter la variable `DATA_DIR=/data`.
- En cas de crash, Railway relance automatiquement (`restartPolicyType: ON_FAILURE`).
- Les logs sont dans **Deployments > View Logs**. Les erreurs courantes (token
  invalide, intents desactives, variable manquante) affichent un message explicite.

---

## EN

### Features

| Command | Description |
| --- | --- |
| `/citation` | Sends a random motivational quote (45 quotes, no immediate repeat). |
| `/pomodoro` | Starts a `25-5` or `50-10` Pomodoro session, with a progress bar updated every minute, a break message and a completion message. |
| `/exp` | Manages experience points for server members. |

`/pomodoro` runs in a background task, one active session per member.

`/exp`: admins (listed in `ADMIN_IDS`, or server administrators) can grant, check and
reset points for any member; other members can only check their own total. Points are
persisted to `DATA_DIR/exp.json`, per guild and per member.

### Project structure

```text
.
├── bot/
│   ├── __init__.py
│   ├── __main__.py         # entry point: python -m bot
│   ├── client.py           # commands.Bot subclass, cog loading, slash sync
│   ├── config.py           # environment variables, read and validated
│   ├── storage.py          # JSON persistence for experience points
│   ├── health.py           # optional HTTP healthcheck server
│   ├── cogs/
│   │   ├── citation.py
│   │   ├── pomodoro.py
│   │   └── exp.py
│   └── resources/
│       └── quotes.json     # quotes, moved out of the code
├── .env.example
├── .python-version
├── Procfile
├── railway.json
└── requirements.txt
```

### Requirements

- Python 3.9 or newer (Railway uses 3.11 through `.python-version`)
- a bot created in the Discord Developer Portal
- **Message Content** and **Server Members** intents enabled

### Environment variables

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `DISCORD_TOKEN` | yes | — | Bot token. |
| `ADMIN_IDS` | recommended | empty | Comma-separated Discord admin IDs. Server administrators are recognized automatically. |
| `DATA_DIR` | no | `data` | Directory storing experience points. |
| `PORT` | no | empty | If set, starts an HTTP healthcheck on that port. |

### Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then fill in DISCORD_TOKEN and ADMIN_IDS
python -m bot
```

### Deploy on Railway

1. Push the repository to GitHub.
2. On [railway.app](https://railway.app): **New Project > Deploy from GitHub repo**, pick this repo.
3. In **Variables**, add `DISCORD_TOKEN` and `ADMIN_IDS`.
4. Deploy. Nixpacks detects Python, installs `requirements.txt` and runs `python -m bot`.

Notes:

- The bot runs as a **worker**: no public domain or exposed port needed. Only set
  `PORT` if you want the healthcheck exposed.
- Railway's filesystem is **ephemeral**. To keep experience points across deploys,
  mount a volume at `/data` (**Settings > Volumes**) and set `DATA_DIR=/data`.
- Railway restarts the service on crash (`restartPolicyType: ON_FAILURE`).
- Logs live under **Deployments > View Logs**; missing variables, an invalid token
  and disabled intents all produce an explicit message.
