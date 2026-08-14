"""
Database — Load Gold to PostgreSQL + Export CSV
=================================================
Eksekusi DDL dan procedure gold layer terhadap PostgreSQL,
lalu ekspor hasilnya ke CSV di data/gold/teams/.

Urutan:
  1. CREATE/REPLACE tabel gold  (ddl_gold_teams.sql)
  2. CREATE/REPLACE procedure   (proc_load_gold_teams.sql)
  3. CALL gold.load_teams_gold()
  4. CALL gold.load_teams_ml_features()
  5. Export kedua tabel ke CSV

CARA PAKAI:
  python src/db/load_gold.py
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from config.config import PATHS, BASE_DIR
from src.utils.helpers import execute_sql_file, execute_sql, get_engine, get_logger

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# Export Gold Tables → CSV
# ---------------------------------------------------------------------------

GOLD_TABLES = {
    "gold.teams_statistics":  "teams_statistics.csv",
    "gold.teams_ml_features": "teams_ml_features.csv",
}


def export_gold_csv() -> None:
    """Ekspor tabel-tabel gold ke CSV di data/gold/teams/."""
    output_dir = BASE_DIR / "data" / "gold" / "teams"
    output_dir.mkdir(parents=True, exist_ok=True)

    engine = get_engine()

    for table_name, filename in GOLD_TABLES.items():
        logger.info("Exporting %s → %s", table_name, filename)
        df = pd.read_sql(f"SELECT * FROM {table_name} ORDER BY club", engine)
        output_path = output_dir / filename
        df.to_csv(output_path, index=False)
        logger.info("  ✅ %s rows × %s cols → %s", df.shape[0], df.shape[1], filename)

    logger.info("CSV export selesai → %s ✅\n", output_dir)


# ---------------------------------------------------------------------------
# Load Gold Teams (OBT + ML Features)
# ---------------------------------------------------------------------------

def load_gold_teams() -> None:
    """Jalankan DDL + load procedure untuk gold teams."""
    sql_dir = PATHS["sql_dir"]

    logger.info("=== DB LOAD: Gold Teams ===")

    # 1. DDL — buat/replace tabel (teams_statistics + teams_ml_features)
    execute_sql_file(sql_dir / "ddl_gold_teams.sql")

    # 2. Procedure — buat/replace
    execute_sql_file(sql_dir / "proc_load_gold_teams.sql")

    # 3. CALL procedure — OBT (TRUNCATE + INSERT ... SELECT)
    execute_sql("CALL gold.load_teams_gold()")

    # 4. CALL procedure — ML Features (TRUNCATE + INSERT ... SELECT)
    execute_sql("CALL gold.load_teams_ml_features()")

    logger.info("Gold teams → PostgreSQL selesai ✅\n")

    # 5. Export ke CSV
    export_gold_csv()


def load_gold_players() -> None:
    """Jalankan DDL + load procedure untuk gold players."""
    sql_dir = PATHS["sql_dir"]

    logger.info("=== DB LOAD: Gold Players ===")

    execute_sql_file(sql_dir / "ddl_gold_players.sql")
    execute_sql_file(sql_dir / "proc_load_gold_players.sql")
    execute_sql("CALL gold.load_players_gold()")

    logger.info("Gold players → PostgreSQL selesai ✅\n")


if __name__ == "__main__":
    load_gold_teams()
    # load_gold_players()  # uncomment jika players sudah siap

