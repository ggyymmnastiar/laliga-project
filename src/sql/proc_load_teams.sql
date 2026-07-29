-- ===========================================================================
-- Silver Layer — Procedure Load Teams
-- ===========================================================================
-- Satu procedure untuk memuat semua 6 tabel teams dari CSV clean.
-- Pola: TRUNCATE → COPY FROM CSV (full refresh) per tabel.
--
-- Cara pakai:
--   CALL silver.load_teams_silver('/absolute/path/to/data/silver/teams/csv_clean');
-- ===========================================================================

CREATE OR REPLACE PROCEDURE silver.load_teams_silver(p_csv_dir TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    -- 1. teams_attacking
    TRUNCATE TABLE silver.teams_attacking;
    EXECUTE format(
        'COPY silver.teams_attacking FROM %L WITH (FORMAT csv, HEADER true)',
        p_csv_dir || '/teams_attacking.csv'
    );
    RAISE NOTICE 'silver.teams_attacking loaded';

    -- 2. teams_defending
    TRUNCATE TABLE silver.teams_defending;
    EXECUTE format(
        'COPY silver.teams_defending FROM %L WITH (FORMAT csv, HEADER true)',
        p_csv_dir || '/teams_defending.csv'
    );
    RAISE NOTICE 'silver.teams_defending loaded';

    -- 3. teams_passing
    TRUNCATE TABLE silver.teams_passing;
    EXECUTE format(
        'COPY silver.teams_passing FROM %L WITH (FORMAT csv, HEADER true)',
        p_csv_dir || '/teams_passing.csv'
    );
    RAISE NOTICE 'silver.teams_passing loaded';

    -- 4. teams_pressing
    TRUNCATE TABLE silver.teams_pressing;
    EXECUTE format(
        'COPY silver.teams_pressing FROM %L WITH (FORMAT csv, HEADER true)',
        p_csv_dir || '/teams_pressing.csv'
    );
    RAISE NOTICE 'silver.teams_pressing loaded';

    -- 5. teams_sequences
    TRUNCATE TABLE silver.teams_sequences;
    EXECUTE format(
        'COPY silver.teams_sequences FROM %L WITH (FORMAT csv, HEADER true)',
        p_csv_dir || '/teams_sequences.csv'
    );
    RAISE NOTICE 'silver.teams_sequences loaded';

    -- 6. teams_misc
    TRUNCATE TABLE silver.teams_misc;
    EXECUTE format(
        'COPY silver.teams_misc FROM %L WITH (FORMAT csv, HEADER true)',
        p_csv_dir || '/teams_misc.csv'
    );
    RAISE NOTICE 'silver.teams_misc loaded';

    RAISE NOTICE 'All 6 teams tables loaded from %', p_csv_dir;
END;
$$;
