"""
Silver Layer — Transform Teams
================================
Dua tahap transformasi:
  Step 1  json_to_csv()   : Bronze JSON  →  CSV raw  (apa adanya, tanpa perubahan)
  Step 2  transform()     : CSV raw      →  CSV clean (pembersihan kolom %)

Output:
  data/silver/teams/csv_raw/    ← CSV 0 (salinan mentah)
  data/silver/teams/csv_clean/  ← CSV 1 (sudah bersih)
"""

import logging
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # root project
BRONZE_DIR = BASE_DIR / "data" / "bronze" / "teams"
SILVER_RAW_DIR = BASE_DIR / "data" / "silver" / "teams" / "csv_raw"
SILVER_CLEAN_DIR = BASE_DIR / "data" / "silver" / "teams" / "csv_clean"

TEAM_FILES = [
    "teams_attacking",
    "teams_defending",
    "teams_passing",
    "teams_pressing",
    "teams_sequences",
    "teams_misc",
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


# ===========================================================================
# Step 1 — JSON → CSV raw (apa adanya)
# ===========================================================================

def json_to_csv() -> None:
    """Baca setiap JSON dari Bronze, simpan sebagai CSV apa adanya (tanpa transformasi)."""

    SILVER_RAW_DIR.mkdir(parents=True, exist_ok=True)
    logger.info("=== STEP 1: JSON → CSV raw ===")

    for name in TEAM_FILES:
        src = BRONZE_DIR / f"{name}.json"
        dst = SILVER_RAW_DIR / f"{name}.csv"

        if not src.exists():
            logger.warning("File tidak ditemukan: %s", src)
            continue

        df = pd.read_json(src)
        df.to_csv(dst, index=False)
        logger.info("✅  %s.json  →  %s  (%d rows, %d cols)", name, dst.name, len(df), len(df.columns))

    logger.info("Step 1 selesai.\n")


# ===========================================================================
# Step 2 — CSV raw → CSV clean
# ===========================================================================

def _strip_pct(series: pd.Series) -> pd.Series:
    """Hapus simbol '%' dan konversi ke float. Contoh: '13.73%' → 13.73"""
    return series.str.replace("%", "", regex=False).astype(float)


def _clean_attacking(df: pd.DataFrame) -> pd.DataFrame:
    """Bersihkan teams_attacking: konversi conversion_pct."""
    df = df.copy()
    df["conversion_pct"] = _strip_pct(df["conversion_pct"])
    return df


def _clean_defending(df: pd.DataFrame) -> pd.DataFrame:
    """Bersihkan teams_defending: konversi 3 kolom pct."""
    df = df.copy()
    for col in ["avg_possession_pct", "ground_duels_won_pct", "aerial_duels_won_pct"]:
        df[col] = _strip_pct(df[col])
    return df


def _clean_passing(df: pd.DataFrame) -> pd.DataFrame:
    """Bersihkan teams_passing: konversi 7 kolom pct."""
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
        df[col] = _strip_pct(df[col])
    return df


def _clean_pressing(df: pd.DataFrame) -> pd.DataFrame:
    """Bersihkan teams_pressing: konversi high_turnovers_shot_pct."""
    df = df.copy()
    df["high_turnovers_shot_pct"] = _strip_pct(df["high_turnovers_shot_pct"])
    return df


def _clean_sequences(df: pd.DataFrame) -> pd.DataFrame:
    """teams_sequences: semua kolom sudah numerik, tidak perlu perubahan."""
    return df.copy()


def _clean_misc(df: pd.DataFrame) -> pd.DataFrame:
    """teams_misc: semua kolom sudah integer, tidak perlu perubahan."""
    return df.copy()


# Mapping nama file → fungsi pembersihan
CLEANERS = {
    "teams_attacking": _clean_attacking,
    "teams_defending": _clean_defending,
    "teams_passing": _clean_passing,
    "teams_pressing": _clean_pressing,
    "teams_sequences": _clean_sequences,
    "teams_misc": _clean_misc,
}


def transform() -> None:
    """Baca setiap CSV raw, bersihkan, dan simpan ke CSV clean."""

    SILVER_CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    logger.info("=== STEP 2: CSV raw → CSV clean ===")

    for name in TEAM_FILES:
        src = SILVER_RAW_DIR / f"{name}.csv"
        dst = SILVER_CLEAN_DIR / f"{name}.csv"

        if not src.exists():
            logger.warning("File tidak ditemukan: %s", src)
            continue

        df = pd.read_csv(src)
        cleaner = CLEANERS.get(name)

        if cleaner:
            df = cleaner(df)

        df.to_csv(dst, index=False)
        logger.info("✅  %s (raw)  →  %s (clean)  (%d rows, %d cols)", src.name, dst.name, len(df), len(df.columns))

    logger.info("Step 2 selesai.\n")


# ===========================================================================
# Main
# ===========================================================================

if __name__ == "__main__":
    json_to_csv()
    transform()
