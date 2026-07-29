"""
Bronze Layer — Ingestion Teams
================================
Menyalin 6 file JSON dari datasets/teams/ (Source) ke data/bronze/teams/ (Bronze).
Script ini idempotent — bisa dijalankan berulang kali tanpa efek samping.
"""

import shutil
import logging
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # root project
SOURCE_DIR = BASE_DIR / "datasets" / "teams"
BRONZE_DIR = BASE_DIR / "data" / "bronze" / "teams"

TEAM_FILES = [
    "teams_attacking.json",
    "teams_defending.json",
    "teams_passing.json",
    "teams_pressing.json",
    "teams_sequences.json",
    "teams_misc.json",
]

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def ingest_teams() -> None:
    """Salin semua file JSON teams dari Source ke Bronze."""

    # Pastikan folder tujuan ada
    BRONZE_DIR.mkdir(parents=True, exist_ok=True)
    logger.info("Bronze directory: %s", BRONZE_DIR)

    copied = 0
    for filename in TEAM_FILES:
        src = SOURCE_DIR / filename
        dst = BRONZE_DIR / filename

        if not src.exists():
            logger.warning("Source file tidak ditemukan: %s", src)
            continue

        shutil.copy2(src, dst)
        logger.info("✅  %s  →  %s", src.name, dst)
        copied += 1

    logger.info("Ingestion selesai: %d/%d file berhasil disalin.", copied, len(TEAM_FILES))


if __name__ == "__main__":
    ingest_teams()
