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

W = 62  # lebar garis dekoratif


def _header(text: str) -> None:
    """Print header box untuk section utama."""
    logger.info("")
    logger.info("╔" + "═" * W + "╗")
    logger.info("║  %-*s║", W - 2, text)
    logger.info("╚" + "═" * W + "╝")


def _step_header(num: int, title: str, desc: str) -> None:
    """Print header untuk setiap step pipeline."""
    logger.info("")
    logger.info("┌" + "─" * W + "┐")
    logger.info("│  STEP %d: %-*s│", num, W - 11, title)
    logger.info("│  %-*s│", W - 2, desc)
    logger.info("└" + "─" * W + "┘")


def main() -> None:
    """Jalankan seluruh pipeline end-to-end."""

    start = time.time()
    step_times: list[tuple[str, float]] = []

    _header("LALIGA DATA PIPELINE — START")

    # ------------------------------------------------------------------
    # Step 1: Bronze Ingestion (datasets → bronze)
    # ------------------------------------------------------------------
    _step_header(1, "Bronze Ingestion", "datasets/JSON → data/bronze/JSON")
    t0 = time.time()
    from src.bronze.ingestion_teams import ingest_teams
    ingest_teams()
    step_times.append(("Bronze Ingestion", time.time() - t0))

    # ------------------------------------------------------------------
    # Step 2: Silver Transform + DQ Validation (bronze → silver csv)
    # ------------------------------------------------------------------
    _step_header(2, "Silver Transform", "bronze/JSON → silver/csv_clean (+ DQ Validation)")
    t0 = time.time()
    from src.silver.transform_teams import run_transform_teams
    run_transform_teams()
    step_times.append(("Silver Transform", time.time() - t0))

    # ------------------------------------------------------------------
    # Step 3: Load Silver
    # ------------------------------------------------------------------
    _step_header(3, "Load Silver", "csv_clean → silver schema + local CSV")
    t0 = time.time()
    from src.db.load_silver import load_silver_teams
    load_silver_teams()
    step_times.append(("Load Silver", time.time() - t0))

    # ------------------------------------------------------------------
    # Step 4: Load Gold
    # ------------------------------------------------------------------
    _step_header(4, "Load Gold", "silver schema → gold schema (OBT) + local CSV")
    t0 = time.time()
    from src.db.load_gold import load_gold_teams
    load_gold_teams()
    step_times.append(("Load Gold", time.time() - t0))

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    elapsed = time.time() - start

    logger.info("")
    logger.info("╔" + "═" * W + "╗")
    logger.info("║  %-*s║", W - 2, "PIPELINE SUMMARY")
    logger.info("╠" + "═" * W + "╣")
    for i, (name, t) in enumerate(step_times, 1):
        logger.info("║  Step %d  %-30s  %8.2fs  ✅  ║", i, name, t)
    logger.info("╠" + "═" * W + "╣")
    logger.info("║  %-30s  %8.2fs       ║", "TOTAL", elapsed)
    logger.info("╚" + "═" * W + "╝")
    logger.info("")


if __name__ == "__main__":
    main()
