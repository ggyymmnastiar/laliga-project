-- ===========================================================================
-- Silver Layer — Load Teams
-- ===========================================================================
-- Memuat semua 6 tabel teams dari CSV clean.
-- Pola: TRUNCATE → COPY FROM CSV (full refresh) per tabel.
--
-- CARA PAKAI:
--   CALL silver.load_teams_silver();
--
-- PENTING: Ganti path v_csv_dir di dalam procedure
--          sesuai lokasi project Anda.
-- ===========================================================================


-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-- PROCEDURE
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CREATE OR REPLACE PROCEDURE silver.load_teams_silver()
LANGUAGE plpgsql
AS $$
DECLARE
    v_csv_dir TEXT := '/Users/g/Desktop/Documents/LaLiga/laliga-project/data/silver/teams/csv_clean';
BEGIN
    -- 1) SILVER.TEAMS_ATTACKING
    TRUNCATE TABLE silver.teams_attacking;
    EXECUTE format(
        'COPY silver.teams_attacking FROM %L DELIMITER '','' CSV HEADER',
        v_csv_dir || '/teams_attacking.csv'
    );

    -- 2) SILVER.TEAMS_DEFENDING
    TRUNCATE TABLE silver.teams_defending;
    EXECUTE format(
        'COPY silver.teams_defending FROM %L DELIMITER '','' CSV HEADER',
        v_csv_dir || '/teams_defending.csv'
    );

    -- 3) SILVER.TEAMS_PASSING
    TRUNCATE TABLE silver.teams_passing;
    EXECUTE format(
        'COPY silver.teams_passing FROM %L DELIMITER '','' CSV HEADER',
        v_csv_dir || '/teams_passing.csv'
    );

    -- 4) SILVER.TEAMS_PRESSING
    TRUNCATE TABLE silver.teams_pressing;
    EXECUTE format(
        'COPY silver.teams_pressing FROM %L DELIMITER '','' CSV HEADER',
        v_csv_dir || '/teams_pressing.csv'
    );

    -- 5) SILVER.TEAMS_SEQUENCES
    TRUNCATE TABLE silver.teams_sequences;
    EXECUTE format(
        'COPY silver.teams_sequences FROM %L DELIMITER '','' CSV HEADER',
        v_csv_dir || '/teams_sequences.csv'
    );

    -- 6) SILVER.TEAMS_MISC
    TRUNCATE TABLE silver.teams_misc;
    EXECUTE format(
        'COPY silver.teams_misc FROM %L DELIMITER '','' CSV HEADER',
        v_csv_dir || '/teams_misc.csv'
    );

    RAISE NOTICE 'All 6 teams tables loaded from %', v_csv_dir;
END;
$$;


-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-- REFERENSI DBEAVER — Statement manual (opsional, untuk test/debug)
-- Ganti path sesuai lokasi project.
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-- TRUNCATE TABLE silver.teams_attacking;
-- COPY silver.teams_attacking
-- FROM '/Users/g/.../csv_clean/teams_attacking.csv'
-- DELIMITER ',' CSV HEADER;

-- (ulangi untuk teams_defending, teams_passing, teams_pressing,
--  teams_sequences, teams_misc)
--
-- Atau cukup panggil:
-- CALL silver.load_teams_silver();
