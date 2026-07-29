-- ===========================================================================
-- Silver Layer — Load Teams
-- ===========================================================================
-- Memuat semua 6 tabel teams dari CSV clean.
-- Pola: TRUNCATE → COPY FROM CSV (full refresh) per tabel.
--
-- CARA PAKAI:
--   Opsi 1: Jalankan statement TRUNCATE + COPY satu per satu di DBeaver.
--   Opsi 2: CALL silver.load_teams_silver();
--
-- PENTING: Ganti path '/Users/g/Desktop/Documents/LaLiga/laliga-project/data/silver/teams/csv_clean'
--          sesuai lokasi project Anda.
-- ===========================================================================


-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-- BAGIAN 1 — Statement langsung (bisa dijalankan satu per satu di DBeaver)
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-- 1) SILVER.TEAMS_ATTACKING
TRUNCATE TABLE silver.teams_attacking;

COPY silver.teams_attacking
FROM '/Users/g/Desktop/Documents/LaLiga/laliga-project/data/silver/teams/csv_clean/teams_attacking.csv'
DELIMITER ','
CSV HEADER;

-- 2) SILVER.TEAMS_DEFENDING
TRUNCATE TABLE silver.teams_defending;

COPY silver.teams_defending
FROM '/Users/g/Desktop/Documents/LaLiga/laliga-project/data/silver/teams/csv_clean/teams_defending.csv'
DELIMITER ','
CSV HEADER;

-- 3) SILVER.TEAMS_PASSING
TRUNCATE TABLE silver.teams_passing;

COPY silver.teams_passing
FROM '/Users/g/Desktop/Documents/LaLiga/laliga-project/data/silver/teams/csv_clean/teams_passing.csv'
DELIMITER ','
CSV HEADER;

-- 4) SILVER.TEAMS_PRESSING
TRUNCATE TABLE silver.teams_pressing;

COPY silver.teams_pressing
FROM '/Users/g/Desktop/Documents/LaLiga/laliga-project/data/silver/teams/csv_clean/teams_pressing.csv'
DELIMITER ','
CSV HEADER;

-- 5) SILVER.TEAMS_SEQUENCES
TRUNCATE TABLE silver.teams_sequences;

COPY silver.teams_sequences
FROM '/Users/g/Desktop/Documents/LaLiga/laliga-project/data/silver/teams/csv_clean/teams_sequences.csv'
DELIMITER ','
CSV HEADER;

-- 6) SILVER.TEAMS_MISC
TRUNCATE TABLE silver.teams_misc;

COPY silver.teams_misc
FROM '/Users/g/Desktop/Documents/LaLiga/laliga-project/data/silver/teams/csv_clean/teams_misc.csv'
DELIMITER ','
CSV HEADER;


-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-- BAGIAN 2 — Procedure (membungkus semua statement di atas)
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
