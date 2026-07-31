"""
Silver Layer — Transform Teams
================================
Dua tahap transformasi:
  Step 1  json_to_csv   : Bronze JSON  →  CSV raw  (apa adanya, tanpa perubahan)
  Step 2  transform     : CSV raw      →  CSV clean (pembersihan kolom %)

Output:
  data/silver/teams/csv_raw/    ← CSV 0 (salinan mentah)
  data/silver/teams/csv_clean/  ← CSV 1 (sudah bersih)

Tabel: 12 file (4 attacking, 4 defending, passing, pressing, sequences, misc)
"""

import sys
from pathlib import Path

import pandas as pd

# Tambahkan root project ke sys.path agar bisa import config & utils
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from config.config import PATHS, TEAM_FILES
from src.utils.helpers import strip_pct, json_to_csv, transform_csvs, get_logger

logger = get_logger(__name__)


# ===========================================================================
# Cleaner functions (spesifik per tabel)
# ===========================================================================

# ---- ATTACKING ----

def _clean_attacking_overall(df: pd.DataFrame) -> pd.DataFrame:
    """Bersihkan teams_attacking_overall: konversi conversion_pct."""
    df = df.copy()
    df["conversion_pct"] = strip_pct(df["conversion_pct"])
    return df


def _clean_attacking_non_penalty(df: pd.DataFrame) -> pd.DataFrame:
    """Bersihkan teams_attacking_non_penalty: konversi conv_pct."""
    df = df.copy()
    df["conv_pct"] = strip_pct(df["conv_pct"])
    return df


def _clean_attacking_set_pieces(df: pd.DataFrame) -> pd.DataFrame:
    """Bersihkan teams_attacking_set_pieces: konversi 3 kolom pct."""
    df = df.copy()
    for col in ["goal_pct", "shot_pct", "xg_pct"]:
        df[col] = strip_pct(df[col])
    return df


def _clean_attacking_misc(df: pd.DataFrame) -> pd.DataFrame:
    """teams_attacking_misc: semua kolom sudah integer, tidak perlu perubahan."""
    return df.copy()


# ---- DEFENDING ----

def _clean_defending_defensive_action(df: pd.DataFrame) -> pd.DataFrame:
    """Bersihkan teams_defending_defensive_action: konversi 3 kolom pct."""
    df = df.copy()
    for col in ["avg_possession_pct", "ground_duels_won_pct", "aerial_duels_won_pct"]:
        df[col] = strip_pct(df[col])
    return df


def _clean_defending_overall(df: pd.DataFrame) -> pd.DataFrame:
    """Bersihkan teams_defending_overall: konversi 3 kolom pct."""
    df = df.copy()
    for col in ["conv_pct", "shots_in_box_pct", "goals_in_box_pct"]:
        df[col] = strip_pct(df[col])
    return df


def _clean_defending_set_piece(df: pd.DataFrame) -> pd.DataFrame:
    """Bersihkan teams_defending_set_piece: konversi 3 kolom pct."""
    df = df.copy()
    for col in ["goal_pct", "shot_pct", "xg_pct"]:
        df[col] = strip_pct(df[col])
    return df


def _clean_defending_misc(df: pd.DataFrame) -> pd.DataFrame:
    """teams_defending_misc: semua kolom sudah integer, tidak perlu perubahan."""
    return df.copy()


# ---- LAINNYA (tetap) ----

def _clean_passing(df: pd.DataFrame) -> pd.DataFrame:
    """Bersihkan teams_passing: konversi 8 kolom pct."""
    df = df.copy()
    pct_cols = [
        "avg_possession_pct",
        "passes_pct",
        "final_third_pct",
        "direction_fwd_pct",
        "direction_bwd_pct",
        "direction_left_pct",
        "direction_right_pct",
        "crosses_pct",
    ]
    for col in pct_cols:
        df[col] = strip_pct(df[col])
    return df


def _clean_pressing(df: pd.DataFrame) -> pd.DataFrame:
    """Bersihkan teams_pressing: konversi high_turnovers_shot_pct."""
    df = df.copy()
    df["high_turnovers_shot_pct"] = strip_pct(df["high_turnovers_shot_pct"])
    return df


def _clean_sequences(df: pd.DataFrame) -> pd.DataFrame:
    """teams_sequences: semua kolom sudah numerik, tidak perlu perubahan."""
    return df.copy()


def _clean_misc(df: pd.DataFrame) -> pd.DataFrame:
    """teams_misc: semua kolom sudah integer, tidak perlu perubahan."""
    return df.copy()


# Mapping nama file → fungsi pembersihan
CLEANERS = {
    # Attacking
    "teams_attacking_overall": _clean_attacking_overall,
    "teams_attacking_non_penalty": _clean_attacking_non_penalty,
    "teams_attacking_set_pieces": _clean_attacking_set_pieces,
    "teams_attacking_misc": _clean_attacking_misc,
    # Defending
    "teams_defending_defensive_action": _clean_defending_defensive_action,
    "teams_defending_overall": _clean_defending_overall,
    "teams_defending_set_piece": _clean_defending_set_piece,
    "teams_defending_misc": _clean_defending_misc,
    # Lainnya
    "teams_passing": _clean_passing,
    "teams_pressing": _clean_pressing,
    "teams_sequences": _clean_sequences,
    "teams_misc": _clean_misc,
}


# ===========================================================================
# Main
# ===========================================================================

def run_transform_teams() -> None:
    """Jalankan seluruh pipeline Silver untuk teams."""
    logger.info("=== SILVER TRANSFORM: Teams ===\n")

    # Step 1: JSON → CSV raw
    json_to_csv(
        source_dir=PATHS["bronze_teams"],
        target_dir=PATHS["silver_teams_raw"],
        file_list=TEAM_FILES,
    )

    # Step 2: CSV raw → CSV clean
    transform_csvs(
        source_dir=PATHS["silver_teams_raw"],
        target_dir=PATHS["silver_teams_clean"],
        file_list=TEAM_FILES,
        cleaners=CLEANERS,
    )


if __name__ == "__main__":
    run_transform_teams()
