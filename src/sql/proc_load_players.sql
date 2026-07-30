-- ===========================================================================
-- Silver Layer — Load Players
-- ===========================================================================
-- Memuat semua 5 tabel players dari CSV clean.
-- Pola: TRUNCATE → COPY FROM CSV (full refresh) per tabel.
--
-- CARA PAKAI:
--   CALL silver.load_players_silver();
--
-- PENTING: Ganti path v_csv_dir di dalam procedure
--          sesuai lokasi project Anda.
-- ===========================================================================


-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-- PROCEDURE
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CREATE OR REPLACE PROCEDURE silver.load_players_silver()
LANGUAGE plpgsql
AS $$
DECLARE
    v_csv_dir TEXT := '/Users/g/Desktop/Documents/LaLiga/laliga-project/data/silver/players/csv_clean';
BEGIN
    -- 1) SILVER.PLAYERS_ATTACKING
    TRUNCATE TABLE silver.players_attacking;
    EXECUTE format(
        'COPY silver.players_attacking FROM %L DELIMITER '','' CSV HEADER',
        v_csv_dir || '/players_attacking.csv'
    );

    -- 2) SILVER.PLAYERS_DEFENDING
    TRUNCATE TABLE silver.players_defending;
    EXECUTE format(
        'COPY silver.players_defending FROM %L DELIMITER '','' CSV HEADER',
        v_csv_dir || '/players_defending.csv'
    );

    -- 3) SILVER.PLAYERS_PASSING
    TRUNCATE TABLE silver.players_passing;
    EXECUTE format(
        'COPY silver.players_passing FROM %L DELIMITER '','' CSV HEADER',
        v_csv_dir || '/players_passing.csv'
    );

    -- 4) SILVER.PLAYERS_CARRYING
    TRUNCATE TABLE silver.players_carrying;
    EXECUTE format(
        'COPY silver.players_carrying FROM %L DELIMITER '','' CSV HEADER',
        v_csv_dir || '/players_carrying.csv'
    );

    -- 5) SILVER.PLAYERS_GOALKEEPING
    TRUNCATE TABLE silver.players_goalkeeping;
    EXECUTE format(
        'COPY silver.players_goalkeeping FROM %L DELIMITER '','' CSV HEADER',
        v_csv_dir || '/players_goalkeeping.csv'
    );

    RAISE NOTICE 'All 5 players tables loaded from %', v_csv_dir;
END;
$$;


-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-- REFERENSI DBEAVER — Statement manual (opsional, untuk test/debug)
-- Ganti path sesuai lokasi project.
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-- TRUNCATE TABLE silver.players_attacking;
-- COPY silver.players_attacking
-- FROM '/Users/g/.../csv_clean/players_attacking.csv'
-- DELIMITER ',' CSV HEADER;

-- (ulangi untuk players_defending, players_passing, players_carrying,
--  players_goalkeeping)
--
-- Atau cukup panggil:
-- CALL silver.load_players_silver();
