"""
Bronze Layer — Ingestion Teams
================================
Menyalin 6 file JSON dari datasets/teams/ (Source) ke data/bronze/teams/ (Bronze).
Script ini idempotent — bisa dijalankan berulang kali tanpa efek samping.
"""

import sys
from pathlib import Path

# Tambahkan root project ke sys.path agar bisa import config & utils
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from config.config import PATHS, TEAM_FILES
from src.utils.helpers import ingest_files, get_logger

logger = get_logger(__name__)


def ingest_teams() -> None:
    """Salin semua file JSON teams dari Source ke Bronze."""
    logger.info("=== BRONZE INGESTION: Teams ===")
    ingest_files(
        source_dir=PATHS["source_teams"],
        target_dir=PATHS["bronze_teams"],
        file_list=TEAM_FILES,
        extension=".json",
    )


if __name__ == "__main__":
    ingest_teams()
