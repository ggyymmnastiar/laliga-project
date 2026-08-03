"""
Silver Layer — Transform Teams
================================
Tiga tahap transformasi:
  Step 1  json_to_csv   : Bronze JSON  →  CSV raw  (apa adanya, tanpa perubahan)
  Step 2  transform     : CSV raw      →  CSV clean (pembersihan kolom %)
  Step 3  validate      : CSV clean    →  DQ checks (11 validasi kualitas data)

Output:
  data/silver/teams/csv_raw/    ← CSV 0 (salinan mentah)
  data/silver/teams/csv_clean/  ← CSV 1 (sudah bersih + tervalidasi)

Tabel: 12 file (4 attacking, 4 defending, passing, pressing, sequences, misc)
"""

import sys
from pathlib import Path

import pandas as pd

# Tambahkan root project ke sys.path agar bisa import config & utils
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from config.config import PATHS, TEAM_FILES
from src.utils.helpers import strip_pct, json_to_csv, transform_csvs, get_logger
from src.utils.validators import run_all_validations

logger = get_logger(__name__)


# ===========================================================================
# Expected Schema per tabel (untuk DQ validation)
# ===========================================================================

TABLE_SCHEMAS = {
    "teams_attacking_overall": {
        "expected_columns": [
            "club", "played", "goals", "xg", "goals_vs_xg",
            "shots", "sot", "conversion_pct", "xg_per_shot",
        ],
        "pct_columns": ["conversion_pct"],
    },
    "teams_attacking_non_penalty": {
        "expected_columns": [
            "club", "played", "goals", "xg", "goals_vs_xg",
            "shots", "sot", "conv_pct", "xg_per_shot",
        ],
        "pct_columns": ["conv_pct"],
    },
    "teams_attacking_set_pieces": {
        "expected_columns": [
            "club", "played", "goals", "shots", "xg",
            "goal_pct", "shot_pct", "xg_pct",
        ],
        "pct_columns": ["goal_pct", "shot_pct", "xg_pct"],
    },
    "teams_attacking_misc": {
        "expected_columns": [
            "club", "played", "touches_in_box", "hit_woodwork", "offsides",
            "penalties_total", "penalties_goals",
            "free_kicks_total", "free_kicks_goals",
            "headers_total", "headers_goals",
            "fast_breaks_total", "fast_breaks_goals",
        ],
        "pct_columns": [],
    },
    "teams_defending_defensive_action": {
        "expected_columns": [
            "club", "played", "avg_possession_pct",
            "tackles", "interceptions", "possession_won",
            "blocks", "clearances",
            "ground_duels_won_pct", "aerial_duels_won_pct",
        ],
        "pct_columns": ["avg_possession_pct", "ground_duels_won_pct", "aerial_duels_won_pct"],
    },
    "teams_defending_overall": {
        "expected_columns": [
            "club", "played", "goals", "xg", "goals_vs_xg",
            "shots", "sot", "conv_pct", "xg_per_shot",
            "shots_in_box_pct", "goals_in_box_pct",
        ],
        "pct_columns": ["conv_pct", "shots_in_box_pct", "goals_in_box_pct"],
    },
    "teams_defending_set_piece": {
        "expected_columns": [
            "club", "played", "goals", "shots", "xg",
            "goal_pct", "shot_pct", "xg_pct",
        ],
        "pct_columns": ["goal_pct", "shot_pct", "xg_pct"],
    },
    "teams_defending_misc": {
        "expected_columns": [
            "club", "played", "touches_in_box", "hit_woodwork", "offsides",
            "penalties_total", "penalties_goals",
            "free_kicks_total", "free_kicks_goals",
            "headers_total", "headers_goals",
            "fast_breaks_total", "fast_breaks_goals",
        ],
        "pct_columns": [],
    },
    "teams_passing": {
        "expected_columns": [
            "club", "played", "avg_possession_pct",
            "passes_total", "passes_successful", "passes_pct",
            "final_third_total", "final_third_successful", "final_third_pct",
            "direction_fwd_pct", "direction_bwd_pct",
            "direction_left_pct", "direction_right_pct",
            "crosses_total", "crosses_successful", "crosses_pct",
            "through_balls",
        ],
        "pct_columns": [
            "avg_possession_pct", "passes_pct", "final_third_pct",
            "direction_fwd_pct", "direction_bwd_pct",
            "direction_left_pct", "direction_right_pct", "crosses_pct",
        ],
    },
    "teams_pressing": {
        "expected_columns": [
            "club", "played", "pressed_seqs", "ppda", "start_distance",
            "high_turnovers_total", "high_turnovers_shot_ending",
            "high_turnovers_goal_ending", "high_turnovers_shot_pct",
        ],
        "pct_columns": ["high_turnovers_shot_pct"],
    },
    "teams_sequences": {
        "expected_columns": [
            "club", "played", "passes_10_plus", "direct_speed",
            "passes_per_seq", "sequence_time",
            "buildups_total", "buildups_goals",
            "direct_attacks_total", "direct_attacks_goals",
        ],
        "pct_columns": [],
    },
    "teams_misc": {
        "expected_columns": [
            "club", "subs_used", "subs_goals",
            "errors_lead_to_shot", "errors_lead_to_goal",
            "fouled", "yellows", "reds", "pens_won",
            "fouls", "opp_yellows", "opp_reds", "pens_conceded",
        ],
        "pct_columns": [],
        "played_value": None,  # teams_misc tidak punya kolom 'played'
    },
}


# ===========================================================================
# Cleaner functions (spesifik per tabel)
# ===========================================================================

# ---- ATTACKING ----

def _clean_attacking_overall(df: pd.DataFrame) -> pd.DataFrame:
    """Bersihkan teams_attacking_overall: konversi conversion_pct."""
    df = df.copy()
    df["conversion_pct"] = strip_pct(df["conversion_pct"])
    df = run_all_validations(df, "teams_attacking_overall",
                             **TABLE_SCHEMAS["teams_attacking_overall"])
    return df


def _clean_attacking_non_penalty(df: pd.DataFrame) -> pd.DataFrame:
    """Bersihkan teams_attacking_non_penalty: konversi conv_pct."""
    df = df.copy()
    df["conv_pct"] = strip_pct(df["conv_pct"])
    df = run_all_validations(df, "teams_attacking_non_penalty",
                             **TABLE_SCHEMAS["teams_attacking_non_penalty"])
    return df


def _clean_attacking_set_pieces(df: pd.DataFrame) -> pd.DataFrame:
    """Bersihkan teams_attacking_set_pieces: konversi 3 kolom pct."""
    df = df.copy()
    for col in ["goal_pct", "shot_pct", "xg_pct"]:
        df[col] = strip_pct(df[col])
    df = run_all_validations(df, "teams_attacking_set_pieces",
                             **TABLE_SCHEMAS["teams_attacking_set_pieces"])
    return df


def _clean_attacking_misc(df: pd.DataFrame) -> pd.DataFrame:
    """teams_attacking_misc: semua kolom sudah integer."""
    df = df.copy()
    df = run_all_validations(df, "teams_attacking_misc",
                             **TABLE_SCHEMAS["teams_attacking_misc"])
    return df


# ---- DEFENDING ----

def _clean_defending_defensive_action(df: pd.DataFrame) -> pd.DataFrame:
    """Bersihkan teams_defending_defensive_action: konversi 3 kolom pct."""
    df = df.copy()
    for col in ["avg_possession_pct", "ground_duels_won_pct", "aerial_duels_won_pct"]:
        df[col] = strip_pct(df[col])
    df = run_all_validations(df, "teams_defending_defensive_action",
                             **TABLE_SCHEMAS["teams_defending_defensive_action"])
    return df


def _clean_defending_overall(df: pd.DataFrame) -> pd.DataFrame:
    """Bersihkan teams_defending_overall: konversi 3 kolom pct."""
    df = df.copy()
    for col in ["conv_pct", "shots_in_box_pct", "goals_in_box_pct"]:
        df[col] = strip_pct(df[col])
    df = run_all_validations(df, "teams_defending_overall",
                             **TABLE_SCHEMAS["teams_defending_overall"])
    return df


def _clean_defending_set_piece(df: pd.DataFrame) -> pd.DataFrame:
    """Bersihkan teams_defending_set_piece: konversi 3 kolom pct."""
    df = df.copy()
    for col in ["goal_pct", "shot_pct", "xg_pct"]:
        df[col] = strip_pct(df[col])
    df = run_all_validations(df, "teams_defending_set_piece",
                             **TABLE_SCHEMAS["teams_defending_set_piece"])
    return df


def _clean_defending_misc(df: pd.DataFrame) -> pd.DataFrame:
    """teams_defending_misc: semua kolom sudah integer."""
    df = df.copy()
    df = run_all_validations(df, "teams_defending_misc",
                             **TABLE_SCHEMAS["teams_defending_misc"])
    return df


# ---- LAINNYA ----

def _clean_passing(df: pd.DataFrame) -> pd.DataFrame:
    """Bersihkan teams_passing: konversi 8 kolom pct."""
    df = df.copy()
    pct_cols = [
        "avg_possession_pct", "passes_pct", "final_third_pct",
        "direction_fwd_pct", "direction_bwd_pct",
        "direction_left_pct", "direction_right_pct", "crosses_pct",
    ]
    for col in pct_cols:
        df[col] = strip_pct(df[col])
    df = run_all_validations(df, "teams_passing",
                             **TABLE_SCHEMAS["teams_passing"])
    return df


def _clean_pressing(df: pd.DataFrame) -> pd.DataFrame:
    """Bersihkan teams_pressing: konversi high_turnovers_shot_pct."""
    df = df.copy()
    df["high_turnovers_shot_pct"] = strip_pct(df["high_turnovers_shot_pct"])
    df = run_all_validations(df, "teams_pressing",
                             **TABLE_SCHEMAS["teams_pressing"])
    return df


def _clean_sequences(df: pd.DataFrame) -> pd.DataFrame:
    """teams_sequences: semua kolom sudah numerik."""
    df = df.copy()
    df = run_all_validations(df, "teams_sequences",
                             **TABLE_SCHEMAS["teams_sequences"])
    return df


def _clean_misc(df: pd.DataFrame) -> pd.DataFrame:
    """teams_misc: semua kolom sudah integer. Tidak ada kolom 'played'."""
    df = df.copy()
    df = run_all_validations(df, "teams_misc",
                             **TABLE_SCHEMAS["teams_misc"])
    return df


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

    # Step 2 + 3: CSV raw → CSV clean (cleaning + DQ validation)
    transform_csvs(
        source_dir=PATHS["silver_teams_raw"],
        target_dir=PATHS["silver_teams_clean"],
        file_list=TEAM_FILES,
        cleaners=CLEANERS,
    )


if __name__ == "__main__":
    run_transform_teams()
