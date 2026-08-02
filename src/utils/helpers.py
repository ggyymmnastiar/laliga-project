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


# ---------------------------------------------------------------------------
# Database — PostgreSQL
# ---------------------------------------------------------------------------

def get_connection():
    """Buat koneksi psycopg2 ke PostgreSQL menggunakan config dari .env.

    Returns:
        psycopg2 connection object (auto-commit OFF).
    """
    import psycopg2
    from config.config import DB_CONFIG

    return psycopg2.connect(**DB_CONFIG)


def get_engine():
    """Buat SQLAlchemy engine ke PostgreSQL.

    Returns:
        sqlalchemy.Engine — untuk pd.read_sql(), df.to_sql(), dll.
    """
    from sqlalchemy import create_engine
    from config.config import DB_URL

    return create_engine(DB_URL)


def execute_sql_file(filepath: str | Path, *, autocommit: bool = True) -> None:
    """Baca dan eksekusi seluruh isi file .sql terhadap PostgreSQL.

    Args:
        filepath: Path ke file .sql.
        autocommit: Jika True, setiap statement langsung di-commit.
    """
    logger = get_logger(__name__)
    filepath = Path(filepath)

    if not filepath.exists():
        logger.error("SQL file tidak ditemukan: %s", filepath)
        raise FileNotFoundError(filepath)

    sql = filepath.read_text(encoding="utf-8")
    conn = get_connection()

    try:
        conn.autocommit = autocommit
        with conn.cursor() as cur:
            cur.execute(sql)
        logger.info("✅  Executed: %s", filepath.name)
    except Exception as e:
        logger.error("❌  Error executing %s: %s", filepath.name, e)
        raise
    finally:
        conn.close()


def execute_sql(sql: str, *, autocommit: bool = True) -> None:
    """Eksekusi SQL string langsung terhadap PostgreSQL.

    Args:
        sql: SQL statement(s) untuk dieksekusi.
        autocommit: Jika True, langsung di-commit.
    """
    logger = get_logger(__name__)
    conn = get_connection()

    try:
        conn.autocommit = autocommit
        with conn.cursor() as cur:
            cur.execute(sql)
        logger.info("✅  SQL executed successfully")
    except Exception as e:
        logger.error("❌  SQL error: %s", e)
        raise
    finally:
        conn.close()

