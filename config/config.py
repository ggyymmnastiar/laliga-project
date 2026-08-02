"""
Config — Path, File Registry & Database
================================
Satu tempat untuk semua path, daftar file, dan koneksi database proyek.
Digunakan oleh semua script di src/ agar tidak ada hardcode tersebar.

Credential database dibaca dari file .env di root project.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Base Directory (root project)
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Load .env
# ---------------------------------------------------------------------------
load_dotenv(BASE_DIR / ".env")

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "laliga"),
    "user": os.getenv("DB_USER", "g"),
    "password": os.getenv("DB_PASSWORD", ""),
}

# SQLAlchemy connection string
DB_URL = (
    f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PATHS = {
    # Source (datasets)
    "source_teams": BASE_DIR / "datasets" / "teams",
    "source_players": BASE_DIR / "datasets" / "players",

    # Bronze
    "bronze_teams": BASE_DIR / "data" / "bronze" / "teams",
    "bronze_players": BASE_DIR / "data" / "bronze" / "players",

    # Silver — Teams
    "silver_teams_raw": BASE_DIR / "data" / "silver" / "teams" / "csv_raw",
    "silver_teams_clean": BASE_DIR / "data" / "silver" / "teams" / "csv_clean",

    # Silver — Players
    "silver_players_raw": BASE_DIR / "data" / "silver" / "players" / "csv_raw",
    "silver_players_clean": BASE_DIR / "data" / "silver" / "players" / "csv_clean",

    # SQL scripts
    "sql_dir": BASE_DIR / "src" / "sql",
}

# ---------------------------------------------------------------------------
# File Lists (tanpa ekstensi)
# ---------------------------------------------------------------------------
TEAM_FILES = [
    # Attacking (4 sub-kategori)
    "teams_attacking_overall",
    "teams_attacking_non_penalty",
    "teams_attacking_set_pieces",
    "teams_attacking_misc",
    # Defending (4 sub-kategori)
    "teams_defending_defensive_action",
    "teams_defending_overall",
    "teams_defending_set_piece",
    "teams_defending_misc",
    # Lainnya (tetap)
    "teams_passing",
    "teams_pressing",
    "teams_sequences",
    "teams_misc",
]

PLAYER_FILES = [
    "players_attacking",
    "players_defending",
    "players_passing",
    "players_carrying",
    "players_goalkeeping",
]
