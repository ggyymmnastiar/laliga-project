"""
Main Pipeline — LaLiga Data Engineering (Prefect Orchestrated)
================================================================
Entry point tunggal untuk menjalankan seluruh pipeline secara berurutan,
di-orchestrate menggunakan Prefect 3.x.

Fitur Prefect yang digunakan:
  - @task          : unit kerja atomik per step
  - @flow          : orkestrasi antar task (sub-flow per layer + master flow)
  - States         : penanganan eksplisit jika step gagal
  - Logging        : Prefect built-in logger (get_run_logger)
  - Runtime Context: metadata run (flow_run.id, flow_run.name, dll.)
  - Retries        : retry otomatis untuk task yang melibatkan koneksi DB
  - Tags           : pengelompokan task per layer (bronze, silver, gold)
  - Deployment     : .serve() untuk penjadwalan pipeline

CARA PAKAI:
  python main_prefect.py              # langsung jalankan pipeline
  python main_prefect.py --deploy     # jalankan sebagai deployment (serve)

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

from prefect import task, flow, get_run_logger
from prefect.runtime import flow_run


W = 62  # lebar garis dekoratif


# ===========================================================================
# Helper — Decorative Headers (menggunakan Prefect logger)
# ===========================================================================

def _header(logger, text: str) -> None:
    """Print header box untuk section utama."""
    logger.info("")
    logger.info("╔" + "═" * W + "╗")
    logger.info("║  %-*s║", W - 2, text)
    logger.info("╚" + "═" * W + "╝")


def _step_header(logger, num: int, title: str, desc: str) -> None:
    """Print header untuk setiap step pipeline."""
    logger.info("")
    logger.info("┌" + "─" * W + "┐")
    logger.info("│  STEP %d: %-*s│", num, W - 11, title)
    logger.info("│  %-*s│", W - 2, desc)
    logger.info("└" + "─" * W + "┘")


# ===========================================================================
# Tasks — Setiap step pipeline dibungkus sebagai Prefect Task
# ===========================================================================

@task(
    name="bronze-ingestion",
    tags=["bronze", "ingestion"],
    retries=0,
    log_prints=True,
)
def task_bronze_ingestion() -> str:
    """Step 1: Salin 12 file JSON dari datasets → bronze."""
    logger = get_run_logger()
    _step_header(logger, 1, "Bronze Ingestion", "datasets/JSON → data/bronze/JSON")

    from src.bronze.ingestion_teams import ingest_teams
    ingest_teams()

    logger.info("✅ Bronze Ingestion selesai")
    return "bronze_done"


@task(
    name="silver-transform",
    tags=["silver", "transform"],
    retries=0,
    log_prints=True,
)
def task_silver_transform() -> str:
    """Step 2: Transform bronze JSON → silver CSV clean + DQ validation."""
    logger = get_run_logger()
    _step_header(logger, 2, "Silver Transform", "bronze/JSON → silver/csv_clean (+ DQ Validation)")

    from src.silver.transform_teams import run_transform_teams
    run_transform_teams()

    logger.info("✅ Silver Transform selesai")
    return "silver_transform_done"


@task(
    name="load-silver-to-db",
    tags=["silver", "database"],
    retries=2,
    retry_delay_seconds=10,
    log_prints=True,
)
def task_load_silver() -> str:
    """Step 3: Load CSV clean → PostgreSQL silver schema."""
    logger = get_run_logger()
    _step_header(logger, 3, "Load Silver", "csv_clean → silver schema + local CSV")

    from src.db.load_silver import load_silver_teams
    load_silver_teams()

    logger.info("✅ Load Silver selesai")
    return "silver_load_done"


@task(
    name="load-gold-to-db",
    tags=["gold", "database"],
    retries=2,
    retry_delay_seconds=10,
    log_prints=True,
)
def task_load_gold() -> str:
    """Step 4: Load silver schema → gold schema (OBT) + export CSV."""
    logger = get_run_logger()
    _step_header(logger, 4, "Load Gold", "silver schema → gold schema (OBT) + local CSV")

    from src.db.load_gold import load_gold_teams
    load_gold_teams()

    logger.info("✅ Load Gold selesai")
    return "gold_done"


# ===========================================================================
# Sub-Flows — Satu flow per layer
# ===========================================================================

@flow(
    name="bronze-pipeline",
    log_prints=True,
)
def bronze_flow() -> str:
    """Sub-flow untuk Bronze layer."""
    logger = get_run_logger()
    logger.info("🟤 Bronze Pipeline dimulai")

    result = task_bronze_ingestion()
    return result


@flow(
    name="silver-pipeline",
    log_prints=True,
)
def silver_flow() -> str:
    """Sub-flow untuk Silver layer (transform + load ke DB)."""
    logger = get_run_logger()
    logger.info("⚪ Silver Pipeline dimulai")

    # Step 2: Transform
    transform_result = task_silver_transform()

    # Step 3: Load to DB (bergantung pada transform selesai)
    load_result = task_load_silver(wait_for=[transform_result])

    return load_result


@flow(
    name="gold-pipeline",
    log_prints=True,
)
def gold_flow() -> str:
    """Sub-flow untuk Gold layer."""
    logger = get_run_logger()
    logger.info("🟡 Gold Pipeline dimulai")

    result = task_load_gold()
    return result


# ===========================================================================
# Master Flow — Orkestrasi seluruh pipeline
# ===========================================================================

@flow(
    name="laliga-master-pipeline",
    log_prints=True,
)
def master_pipeline() -> None:
    """Jalankan seluruh pipeline end-to-end."""
    logger = get_run_logger()

    # Runtime Context — metadata eksekusi
    run_id   = flow_run.get_id()
    run_name = flow_run.get_name()

    start = time.time()
    step_times: list[tuple[str, float]] = []

    _header(logger, "LALIGA DATA PIPELINE — START")
    logger.info("  Flow Run ID   : %s", run_id)
    logger.info("  Flow Run Name : %s", run_name)

    # ------------------------------------------------------------------
    # Step 1: Bronze
    # ------------------------------------------------------------------
    try:
        t0 = time.time()
        bronze_flow()
        step_times.append(("Bronze Ingestion", time.time() - t0))
    except Exception as e:
        logger.error("❌ Bronze Pipeline GAGAL — pipeline dihentikan: %s", e)
        raise

    # ------------------------------------------------------------------
    # Step 2 + 3: Silver (Transform + Load)
    # ------------------------------------------------------------------
    try:
        t0 = time.time()
        silver_flow()
        step_times.append(("Silver (Transform + Load)", time.time() - t0))
    except Exception as e:
        logger.error("❌ Silver Pipeline GAGAL — pipeline dihentikan: %s", e)
        raise

    # ------------------------------------------------------------------
    # Step 4: Gold
    # ------------------------------------------------------------------
    try:
        t0 = time.time()
        gold_flow()
        step_times.append(("Gold (OBT + Export)", time.time() - t0))
    except Exception as e:
        logger.error("❌ Gold Pipeline GAGAL: %s", e)
        raise

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
    logger.info("  Flow Run ID   : %s", run_id)
    logger.info("  Flow Run Name : %s", run_name)
    logger.info("✅ Pipeline selesai dalam %.2fs", elapsed)


# ===========================================================================
# Entry Point
# ===========================================================================

if __name__ == "__main__":
    if "--deploy" in sys.argv:
        # Deployment mode: serve sebagai scheduled deployment
        master_pipeline.serve(
            name="laliga-daily-pipeline",
            tags=["production", "laliga"],
            parameters={},
        )
    else:
        # Direct run mode: jalankan sekali
        master_pipeline()

