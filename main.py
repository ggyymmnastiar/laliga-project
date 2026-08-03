"""
Main Pipeline — LaLiga Data Engineering
================================
Entry point tunggal untuk menjalankan seluruh pipeline secara berurutan.
Bukan Airflow DAG — pipeline Python biasa yang nantinya bisa di-upgrade
ke Airflow jika diperlukan.

CARA PAKAI:
  python main.py

URUTAN EKSEKUSI:
  Step 1  Bronze Ingestion   : datasets/JSON → data/bronze/JSON
  Step 2  Silver Transform   : bronze/JSON → silver/csv_clean (+ DQ validation)
  Step 3  Load Silver to DB  : csv_clean → PostgreSQL silver schema
  Step 4  Load Gold to DB    : silver schema → PostgreSQL gold schema (OBT)
"""

import sys
import time
from pathlib import Path

# Tambahkan root project ke sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.utils.helpers import get_logger

logger = get_logger(__name__)


def main() -> None:
    """Jalankan seluruh pipeline end-to-end."""

    start = time.time()
    logger.info("=" * 60)
    logger.info("  LALIGA DATA PIPELINE — START")
    logger.info("=" * 60 + "\n")

    # ------------------------------------------------------------------
    # Step 1: Bronze Ingestion (datasets → bronze)
    # ------------------------------------------------------------------
    logger.info("▶ STEP 1: Bronze Ingestion")
    from src.bronze.ingestion_teams import ingest_teams
    ingest_teams()
    logger.info("")

    # ------------------------------------------------------------------
    # Step 2: Silver Transform + DQ Validation (bronze → silver csv)
    # ------------------------------------------------------------------
    logger.info("▶ STEP 2: Silver Transform + DQ Validation")
    from src.silver.transform_teams import run_transform_teams
    run_transform_teams()
    logger.info("")

    # ------------------------------------------------------------------
    # Step 3: Load Silver → PostgreSQL
    # ------------------------------------------------------------------
    logger.info("▶ STEP 3: Load Silver → PostgreSQL")
    from src.db.load_silver import load_silver_teams
    load_silver_teams()
    logger.info("")

    # ------------------------------------------------------------------
    # Step 4: Load Gold → PostgreSQL
    # ------------------------------------------------------------------
    logger.info("▶ STEP 4: Load Gold → PostgreSQL")
    from src.db.load_gold import load_gold_teams
    load_gold_teams()
    logger.info("")

    # ------------------------------------------------------------------
    # Selesai
    # ------------------------------------------------------------------
    elapsed = time.time() - start
    logger.info("=" * 60)
    logger.info("  LALIGA DATA PIPELINE — SELESAI (%.2f detik)", elapsed)
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
