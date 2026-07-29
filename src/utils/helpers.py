"""
Utils — Helper Functions
================================
Fungsi-fungsi reusable yang dipakai oleh pipeline teams dan players.
"""

import shutil
import logging
from pathlib import Path
from typing import Callable

import pandas as pd


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def get_logger(name: str) -> logging.Logger:
    """Setup dan return logger dengan format yang konsisten."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger(name)


# ---------------------------------------------------------------------------
# Data Cleaning
# ---------------------------------------------------------------------------

def strip_pct(series: pd.Series) -> pd.Series:
    """Hapus simbol '%' dan konversi ke float.

    Contoh: '13.73%' → 13.73
    """
    return series.str.replace("%", "", regex=False).astype(float)


# ---------------------------------------------------------------------------
# Bronze — Ingestion
# ---------------------------------------------------------------------------

def ingest_files(
    source_dir: Path,
    target_dir: Path,
    file_list: list[str],
    extension: str = ".json",
) -> int:
    """Salin file dari source ke target directory.

    Args:
        source_dir: Folder sumber (datasets/...).
        target_dir: Folder tujuan (data/bronze/...).
        file_list: Daftar nama file (tanpa ekstensi).
        extension: Ekstensi file (default: .json).

    Returns:
        Jumlah file yang berhasil disalin.
    """
    logger = get_logger(__name__)
    target_dir.mkdir(parents=True, exist_ok=True)
    logger.info("Target directory: %s", target_dir)

    copied = 0
    for name in file_list:
        filename = f"{name}{extension}"
        src = source_dir / filename
        dst = target_dir / filename

        if not src.exists():
            logger.warning("Source file tidak ditemukan: %s", src)
            continue

        shutil.copy2(src, dst)
        logger.info("✅  %s  →  %s", src.name, dst)
        copied += 1

    logger.info("Ingestion selesai: %d/%d file berhasil disalin.", copied, len(file_list))
    return copied


# ---------------------------------------------------------------------------
# Silver — Step 1: JSON → CSV raw
# ---------------------------------------------------------------------------

def json_to_csv(
    source_dir: Path,
    target_dir: Path,
    file_list: list[str],
) -> None:
    """Baca setiap JSON, simpan sebagai CSV apa adanya (tanpa transformasi).

    Args:
        source_dir: Folder JSON (data/bronze/...).
        target_dir: Folder CSV raw (data/silver/.../csv_raw/).
        file_list: Daftar nama file (tanpa ekstensi).
    """
    logger = get_logger(__name__)
    target_dir.mkdir(parents=True, exist_ok=True)
    logger.info("=== STEP 1: JSON → CSV raw ===")

    for name in file_list:
        src = source_dir / f"{name}.json"
        dst = target_dir / f"{name}.csv"

        if not src.exists():
            logger.warning("File tidak ditemukan: %s", src)
            continue

        df = pd.read_json(src)
        df.to_csv(dst, index=False)
        logger.info("✅  %s.json  →  %s  (%d rows, %d cols)", name, dst.name, len(df), len(df.columns))

    logger.info("Step 1 selesai.\n")


# ---------------------------------------------------------------------------
# Silver — Step 2: CSV raw → CSV clean
# ---------------------------------------------------------------------------

def transform_csvs(
    source_dir: Path,
    target_dir: Path,
    file_list: list[str],
    cleaners: dict[str, Callable[[pd.DataFrame], pd.DataFrame]],
) -> None:
    """Baca setiap CSV raw, jalankan cleaner, simpan ke CSV clean.

    Args:
        source_dir: Folder CSV raw (data/silver/.../csv_raw/).
        target_dir: Folder CSV clean (data/silver/.../csv_clean/).
        file_list: Daftar nama file (tanpa ekstensi).
        cleaners: Dict mapping nama file → fungsi pembersihan.
    """
    logger = get_logger(__name__)
    target_dir.mkdir(parents=True, exist_ok=True)
    logger.info("=== STEP 2: CSV raw → CSV clean ===")

    for name in file_list:
        src = source_dir / f"{name}.csv"
        dst = target_dir / f"{name}.csv"

        if not src.exists():
            logger.warning("File tidak ditemukan: %s", src)
            continue

        df = pd.read_csv(src)
        cleaner = cleaners.get(name)

        if cleaner:
            df = cleaner(df)

        df.to_csv(dst, index=False)
        logger.info("✅  %s (raw)  →  %s (clean)  (%d rows, %d cols)", src.name, dst.name, len(df), len(df.columns))

    logger.info("Step 2 selesai.\n")
