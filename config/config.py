"""
Config — Path & File Registry
================================
Satu tempat untuk semua path dan daftar file proyek.
Digunakan oleh semua script di src/ agar tidak ada hardcode tersebar.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Base Directory (root project)
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

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
}

# ---------------------------------------------------------------------------
# File Lists (tanpa ekstensi)
# ---------------------------------------------------------------------------
TEAM_FILES = [
    "teams_attacking",
    "teams_defending",
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
