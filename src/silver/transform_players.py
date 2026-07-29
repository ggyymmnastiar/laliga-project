"""
Silver Layer — Transform Players
================================
Dua tahap transformasi:
  Step 1  json_to_csv   : Bronze JSON  →  CSV raw  (apa adanya, tanpa perubahan)
  Step 2  transform     : CSV raw      →  CSV clean (pembersihan kolom %)

Output:
  data/silver/players/csv_raw/    ← CSV 0 (salinan mentah)
  data/silver/players/csv_clean/  ← CSV 1 (sudah bersih)
"""

import sys
from pathlib import Path

import pandas as pd

# Tambahkan root project ke sys.path agar bisa import config & utils
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from config.config import PATHS, PLAYER_FILES
from src.utils.helpers import strip_pct, json_to_csv, transform_csvs, get_logger

logger = get_logger(__name__)


# ===========================================================================
# Cleaner functions (spesifik per tabel)
# ===========================================================================

def _clean_attacking(df: pd.DataFrame) -> pd.DataFrame:
    """Bersihkan players_attacking: konversi conv_pct."""
    df = df.copy()
    df["conv_pct"] = strip_pct(df["conv_pct"])
    return df


def _clean_defending(df: pd.DataFrame) -> pd.DataFrame:
    """Bersihkan players_defending: konversi ground_duels_pct, aerial_duels_pct.
    Drop kolom 'open_play_total' yang 100% null (artifact dari JSON parsing).
    """
    df = df.copy()
    # Drop kolom stray yang muncul dari JSON parsing
    cols_to_drop = [c for c in ["open_play_total"] if c in df.columns]
    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)
    for col in ["ground_duels_pct", "aerial_duels_pct"]:
        df[col] = strip_pct(df[col])
    return df


def _clean_passing(df: pd.DataFrame) -> pd.DataFrame:
    """Bersihkan players_passing: konversi 3 kolom pct."""
    df = df.copy()
    for col in ["open_play_pct", "final_third_pct", "crosses_pct"]:
        df[col] = strip_pct(df[col])
    return df


def _clean_carrying(df: pd.DataFrame) -> pd.DataFrame:
    """players_carrying: semua kolom sudah numerik, tidak perlu perubahan."""
    return df.copy()


def _clean_goalkeeping(df: pd.DataFrame) -> pd.DataFrame:
    """players_goalkeeping: save_percentage sudah float, tidak perlu perubahan."""
    return df.copy()


# Mapping nama file → fungsi pembersihan
CLEANERS = {
    "players_attacking": _clean_attacking,
    "players_defending": _clean_defending,
    "players_passing": _clean_passing,
    "players_carrying": _clean_carrying,
    "players_goalkeeping": _clean_goalkeeping,
}


# ===========================================================================
# Main
# ===========================================================================

def run_transform_players() -> None:
    """Jalankan seluruh pipeline Silver untuk players."""
    logger.info("=== SILVER TRANSFORM: Players ===\n")

    # Step 1: JSON → CSV raw
    json_to_csv(
        source_dir=PATHS["bronze_players"],
        target_dir=PATHS["silver_players_raw"],
        file_list=PLAYER_FILES,
    )

    # Step 2: CSV raw → CSV clean
    transform_csvs(
        source_dir=PATHS["silver_players_raw"],
        target_dir=PATHS["silver_players_clean"],
        file_list=PLAYER_FILES,
        cleaners=CLEANERS,
    )


if __name__ == "__main__":
    run_transform_players()
