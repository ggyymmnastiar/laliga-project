-- ===========================================================================
-- Silver Layer — Procedure Load Players
-- ===========================================================================
-- Satu procedure untuk memuat semua 5 tabel players dari CSV clean.
-- Pola: TRUNCATE → COPY FROM CSV (full refresh) per tabel.
--
-- Cara pakai:
--   CALL silver.load_players_silver('/absolute/path/to/data/silver/players/csv_clean');
-- ===========================================================================

CREATE OR REPLACE PROCEDURE silver.load_players_silver(p_csv_dir TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    -- 1. players_attacking
    TRUNCATE TABLE silver.players_attacking;
    EXECUTE format(
        'COPY silver.players_attacking FROM %L WITH (FORMAT csv, HEADER true)',
        p_csv_dir || '/players_attacking.csv'
    );
    RAISE NOTICE 'silver.players_attacking loaded';

    -- 2. players_defending
    TRUNCATE TABLE silver.players_defending;
    EXECUTE format(
        'COPY silver.players_defending FROM %L WITH (FORMAT csv, HEADER true)',
        p_csv_dir || '/players_defending.csv'
    );
    RAISE NOTICE 'silver.players_defending loaded';

    -- 3. players_passing
    TRUNCATE TABLE silver.players_passing;
    EXECUTE format(
        'COPY silver.players_passing FROM %L WITH (FORMAT csv, HEADER true)',
        p_csv_dir || '/players_passing.csv'
    );
    RAISE NOTICE 'silver.players_passing loaded';

    -- 4. players_carrying
    TRUNCATE TABLE silver.players_carrying;
    EXECUTE format(
        'COPY silver.players_carrying FROM %L WITH (FORMAT csv, HEADER true)',
        p_csv_dir || '/players_carrying.csv'
    );
    RAISE NOTICE 'silver.players_carrying loaded';

    -- 5. players_goalkeeping
    TRUNCATE TABLE silver.players_goalkeeping;
    EXECUTE format(
        'COPY silver.players_goalkeeping FROM %L WITH (FORMAT csv, HEADER true)',
        p_csv_dir || '/players_goalkeeping.csv'
    );
    RAISE NOTICE 'silver.players_goalkeeping loaded';

    RAISE NOTICE 'All 5 players tables loaded from %', p_csv_dir;
END;
$$;
