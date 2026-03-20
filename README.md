# Discord Bot

## FR

### Description

Ce projet est un bot Discord ecrit en Python avec `discord.py`. Il charge plusieurs cogs au demarrage et propose actuellement trois fonctionnalites principales :

- des citations motivantes
- un minuteur Pomodoro interactif
- un systeme simple de points d'experience

### Fonctionnalites

#### `/citation`

Envoie une citation motivante choisie aleatoirement.

#### `/pomodoro`

Lance une session Pomodoro avec un choix entre :

- `25-5` : 25 minutes de travail, 5 minutes de pause
- `50-10` : 50 minutes de travail, 10 minutes de pause

Le bot envoie ensuite :

- un message de demarrage
- une mise a jour de progression chaque minute
- une notification de passage en pause
- un message de fin de session

#### `/exp`

Ouvre une interface pour gerer les points d'experience des membres du serveur :

- selection d'un membre
- ajout de points selon une activite predefinie
- consultation du total actuel
- reinitialisation des points

Important : les points sont stockes en memoire dans un dictionnaire Python. Ils sont donc perdus lorsque le bot redemarre.

### Structure du projet

```text
.
├── start.py
├── keep_alive.py
├── requirements.txt
└── cogs/
    ├── Pomodoro_timer.py
    ├── citation.py
    └── exp_system.py
```

### Prerequis

- Python 3.9 ou plus recent
- un bot Discord cree dans le Developer Portal
- les intents `Message Content` et `Server Members` actives pour le bot

### Installation

1. Cloner le depot.
2. Creer un environnement virtuel.
3. Installer les dependances.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Si `requirements.txt` pose un probleme d'encodage, reenregistrez-le en UTF-8 puis relancez l'installation.

### Configuration

Creez un fichier `.env` a la racine du projet :

```env
DISCORD_TOKEN=votre_token_discord
```

### Configuration supplementaire pour `/exp`

Le fichier `cogs/exp_system.py` contient actuellement cette ligne :

```python
ADMIN_IDS = [ADMIN_IDS]
```

Elle doit etre remplacee par une vraie liste d'identifiants Discord administrateurs, par exemple :

```python
ADMIN_IDS = [123456789012345678, 987654321098765432]
```

Sans cette modification, le module d'experience ne fonctionnera pas correctement.

### Lancer le bot

```bash
python3 start.py
```

Au demarrage, le bot :

- charge les extensions depuis `cogs/`
- se connecte a Discord
- synchronise les commandes slash

### Notes

- Le prefixe `!` est defini dans le code, mais les fonctionnalites actuelles utilisent des commandes slash.
- `keep_alive.py` demarre un petit serveur Flask sur le port `8080`. Ce fichier peut etre utile pour certains hebergements, mais il n'est pas appele dans `start.py`.

---

## EN

### Description

This project is a Discord bot written in Python with `discord.py`. It loads multiple cogs on startup and currently provides three main features:

- motivational quotes
- an interactive Pomodoro timer
- a simple experience points system

### Features

#### `/citation`

Sends a random motivational quote.

#### `/pomodoro`

Starts a Pomodoro session with two presets:

- `25-5`: 25 minutes of work, 5 minutes of break
- `50-10`: 50 minutes of work, 10 minutes of break

The bot then sends:

- a start message
- a progress update every minute
- a break transition message
- a completion message

#### `/exp`

Opens an interface to manage experience points for server members:

- select a member
- add points based on a predefined activity
- check the current total
- reset points

Important: points are stored in memory in a Python dictionary, so they are lost when the bot restarts.

### Project structure

```text
.
├── start.py
├── keep_alive.py
├── requirements.txt
└── cogs/
    ├── Pomodoro_timer.py
    ├── citation.py
    └── exp_system.py
```

### Requirements

- Python 3.9 or newer
- a Discord bot created in the Developer Portal
- `Message Content` and `Server Members` intents enabled for the bot

### Installation

1. Clone the repository.
2. Create a virtual environment.
3. Install the dependencies.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

If `requirements.txt` causes an encoding issue, save it again as UTF-8 and rerun the install command.

### Configuration

Create a `.env` file at the root of the project:

```env
DISCORD_TOKEN=your_discord_token
```

### Additional setup for `/exp`

The file `cogs/exp_system.py` currently contains this line:

```python
ADMIN_IDS = [ADMIN_IDS]
```

You need to replace it with real Discord administrator IDs, for example:

```python
ADMIN_IDS = [123456789012345678, 987654321098765432]
```

Without this change, the experience system will not work correctly.

### Run the bot

```bash
python3 start.py
```

On startup, the bot:

- loads extensions from `cogs/`
- connects to Discord
- syncs slash commands

### Notes

- The `!` prefix is defined in the code, but the current features use slash commands.
- `keep_alive.py` starts a small Flask server on port `8080`. It may be useful for some hosting platforms, but it is not called from `start.py`.
