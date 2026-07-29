"""
Bronze Layer — Ingestion Players
================================
Menyalin 5 file JSON dari datasets/players/ (Source) ke data/bronze/players/ (Bronze).
Script ini idempotent — bisa dijalankan berulang kali tanpa efek samping.
"""

import sys
from pathlib import Path

# Tambahkan root project ke sys.path agar bisa import config & utils
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from config.config import PATHS, PLAYER_FILES
from src.utils.helpers import ingest_files, get_logger

logger = get_logger(__name__)


def ingest_players() -> None:
    """Salin semua file JSON players dari Source ke Bronze."""
    logger.info("=== BRONZE INGESTION: Players ===")
    ingest_files(
        source_dir=PATHS["source_players"],
        target_dir=PATHS["bronze_players"],
        file_list=PLAYER_FILES,
        extension=".json",
    )


if __name__ == "__main__":
    ingest_players()
