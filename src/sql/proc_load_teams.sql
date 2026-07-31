-- ===========================================================================
-- Silver Layer — Load Teams
-- ===========================================================================
-- Memuat semua 12 tabel teams dari CSV clean.
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
    -- ===== ATTACKING (4 tabel) =====

    -- 1) SILVER.TEAMS_ATTACKING_OVERALL
    TRUNCATE TABLE silver.teams_attacking_overall;
    EXECUTE format(
        'COPY silver.teams_attacking_overall FROM %L DELIMITER '','' CSV HEADER',
        v_csv_dir || '/teams_attacking_overall.csv'
    );

    -- 2) SILVER.TEAMS_ATTACKING_NON_PENALTY
    TRUNCATE TABLE silver.teams_attacking_non_penalty;
    EXECUTE format(
        'COPY silver.teams_attacking_non_penalty FROM %L DELIMITER '','' CSV HEADER',
        v_csv_dir || '/teams_attacking_non_penalty.csv'
    );

    -- 3) SILVER.TEAMS_ATTACKING_SET_PIECES
    TRUNCATE TABLE silver.teams_attacking_set_pieces;
    EXECUTE format(
        'COPY silver.teams_attacking_set_pieces FROM %L DELIMITER '','' CSV HEADER',
        v_csv_dir || '/teams_attacking_set_pieces.csv'
    );

    -- 4) SILVER.TEAMS_ATTACKING_MISC
    TRUNCATE TABLE silver.teams_attacking_misc;
    EXECUTE format(
        'COPY silver.teams_attacking_misc FROM %L DELIMITER '','' CSV HEADER',
        v_csv_dir || '/teams_attacking_misc.csv'
    );

    -- ===== DEFENDING (4 tabel) =====

    -- 5) SILVER.TEAMS_DEFENDING_DEFENSIVE_ACTION
    TRUNCATE TABLE silver.teams_defending_defensive_action;
    EXECUTE format(
        'COPY silver.teams_defending_defensive_action FROM %L DELIMITER '','' CSV HEADER',
        v_csv_dir || '/teams_defending_defensive_action.csv'
    );

    -- 6) SILVER.TEAMS_DEFENDING_OVERALL
    TRUNCATE TABLE silver.teams_defending_overall;
    EXECUTE format(
        'COPY silver.teams_defending_overall FROM %L DELIMITER '','' CSV HEADER',
        v_csv_dir || '/teams_defending_overall.csv'
    );

    -- 7) SILVER.TEAMS_DEFENDING_SET_PIECE
    TRUNCATE TABLE silver.teams_defending_set_piece;
    EXECUTE format(
        'COPY silver.teams_defending_set_piece FROM %L DELIMITER '','' CSV HEADER',
        v_csv_dir || '/teams_defending_set_piece.csv'
    );

    -- 8) SILVER.TEAMS_DEFENDING_MISC
    TRUNCATE TABLE silver.teams_defending_misc;
    EXECUTE format(
        'COPY silver.teams_defending_misc FROM %L DELIMITER '','' CSV HEADER',
        v_csv_dir || '/teams_defending_misc.csv'
    );

    -- ===== LAINNYA (4 tabel) =====

    -- 9) SILVER.TEAMS_PASSING
    TRUNCATE TABLE silver.teams_passing;
    EXECUTE format(
        'COPY silver.teams_passing FROM %L DELIMITER '','' CSV HEADER',
        v_csv_dir || '/teams_passing.csv'
    );

    -- 10) SILVER.TEAMS_PRESSING
    TRUNCATE TABLE silver.teams_pressing;
    EXECUTE format(
        'COPY silver.teams_pressing FROM %L DELIMITER '','' CSV HEADER',
        v_csv_dir || '/teams_pressing.csv'
    );

    -- 11) SILVER.TEAMS_SEQUENCES
    TRUNCATE TABLE silver.teams_sequences;
    EXECUTE format(
        'COPY silver.teams_sequences FROM %L DELIMITER '','' CSV HEADER',
        v_csv_dir || '/teams_sequences.csv'
    );

    -- 12) SILVER.TEAMS_MISC
    TRUNCATE TABLE silver.teams_misc;
    EXECUTE format(
        'COPY silver.teams_misc FROM %L DELIMITER '','' CSV HEADER',
        v_csv_dir || '/teams_misc.csv'
    );

    RAISE NOTICE 'All 12 teams tables loaded from %', v_csv_dir;
END;
$$;


-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-- REFERENSI DBEAVER — Statement manual (opsional, untuk test/debug)
-- Ganti path sesuai lokasi project.
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-- TRUNCATE TABLE silver.teams_attacking_overall;
-- COPY silver.teams_attacking_overall
-- FROM '/Users/g/.../csv_clean/teams_attacking_overall.csv'
-- DELIMITER ',' CSV HEADER;
--
-- (ulangi untuk 11 tabel lainnya)
--
-- Atau cukup panggil:
-- CALL silver.load_teams_silver();
