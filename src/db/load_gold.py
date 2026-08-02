"""
Database — Load Gold to PostgreSQL
================================
Eksekusi DDL dan procedure gold.load_teams_gold() terhadap PostgreSQL.
Urutan:
  1. CREATE/REPLACE tabel gold  (ddl_gold_teams.sql)
  2. CREATE/REPLACE procedure   (proc_load_gold_teams.sql)
  3. CALL gold.load_teams_gold()

CARA PAKAI:
  python src/db/load_gold.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from config.config import PATHS
from src.utils.helpers import execute_sql_file, execute_sql, get_logger

logger = get_logger(__name__)


def load_gold_teams() -> None:
    """Jalankan DDL + load procedure untuk gold teams."""
    sql_dir = PATHS["sql_dir"]

    logger.info("=== DB LOAD: Gold Teams ===")

    # 1. DDL — buat/replace tabel
    execute_sql_file(sql_dir / "ddl_gold_teams.sql")

    # 2. Procedure — buat/replace
    execute_sql_file(sql_dir / "proc_load_gold_teams.sql")

    # 3. CALL procedure (TRUNCATE + INSERT ... SELECT)
    execute_sql("CALL gold.load_teams_gold()")

    logger.info("Gold teams → PostgreSQL selesai ✅\n")


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
