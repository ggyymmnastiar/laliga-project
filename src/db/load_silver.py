"""
Database — Load Silver to PostgreSQL
================================
Eksekusi DDL dan procedure silver.load_teams_silver() terhadap PostgreSQL.
Urutan:
  1. CREATE/REPLACE tabel silver  (ddl_teams.sql)
  2. CREATE/REPLACE procedure     (proc_load_teams.sql)
  3. CALL silver.load_teams_silver()

CARA PAKAI:
  python src/db/load_silver.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from config.config import PATHS
from src.utils.helpers import execute_sql_file, execute_sql, get_logger

logger = get_logger(__name__)


def load_silver_teams() -> None:
    """Jalankan DDL + load procedure untuk silver teams."""
    sql_dir = PATHS["sql_dir"]

    logger.info("=== DB LOAD: Silver Teams ===")

    # 1. DDL — buat/replace tabel
    execute_sql_file(sql_dir / "ddl_teams.sql")

    # 2. Procedure — buat/replace
    execute_sql_file(sql_dir / "proc_load_teams.sql")

    # 3. CALL procedure (TRUNCATE + COPY)
    execute_sql("CALL silver.load_teams_silver()")

    logger.info("Silver teams → PostgreSQL selesai ✅\n")


def load_silver_players() -> None:
    """Jalankan DDL + load procedure untuk silver players."""
    sql_dir = PATHS["sql_dir"]

    logger.info("=== DB LOAD: Silver Players ===")

    execute_sql_file(sql_dir / "ddl_players.sql")
    execute_sql_file(sql_dir / "proc_load_players.sql")
    execute_sql("CALL silver.load_players_silver()")

    logger.info("Silver players → PostgreSQL selesai ✅\n")


if __name__ == "__main__":
    load_silver_teams()
    # load_silver_players()  # uncomment jika players sudah siap
