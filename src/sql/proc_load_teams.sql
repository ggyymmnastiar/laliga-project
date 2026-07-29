-- ===========================================================================
-- Silver Layer — Procedure Load Teams
-- ===========================================================================
-- Stored procedures untuk memuat data dari CSV clean ke tabel PostgreSQL.
-- Pola: TRUNCATE → COPY FROM CSV (full refresh).
--
-- Cara pakai:
--   CALL silver.load_teams_attacking('/absolute/path/to/csv_clean/teams_attacking.csv');
--   CALL silver.load_teams_defending('/absolute/path/to/csv_clean/teams_defending.csv');
--   ... dst
--
-- Atau jalankan semua sekaligus:
--   CALL silver.load_all_teams('/absolute/path/to/csv_clean');
-- ===========================================================================

-- ---------------------------------------------------------------------------
-- 1. load_teams_attacking
-- ---------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE silver.load_teams_attacking(p_csv_path TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    TRUNCATE TABLE silver.teams_attacking;
    EXECUTE format(
        'COPY silver.teams_attacking FROM %L WITH (FORMAT csv, HEADER true)',
        p_csv_path
    );
    RAISE NOTICE 'silver.teams_attacking loaded from %', p_csv_path;
END;
$$;

-- ---------------------------------------------------------------------------
-- 2. load_teams_defending
-- ---------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE silver.load_teams_defending(p_csv_path TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    TRUNCATE TABLE silver.teams_defending;
    EXECUTE format(
        'COPY silver.teams_defending FROM %L WITH (FORMAT csv, HEADER true)',
        p_csv_path
    );
    RAISE NOTICE 'silver.teams_defending loaded from %', p_csv_path;
END;
$$;

-- ---------------------------------------------------------------------------
-- 3. load_teams_passing
-- ---------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE silver.load_teams_passing(p_csv_path TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    TRUNCATE TABLE silver.teams_passing;
    EXECUTE format(
        'COPY silver.teams_passing FROM %L WITH (FORMAT csv, HEADER true)',
        p_csv_path
    );
    RAISE NOTICE 'silver.teams_passing loaded from %', p_csv_path;
END;
$$;

-- ---------------------------------------------------------------------------
-- 4. load_teams_pressing
-- ---------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE silver.load_teams_pressing(p_csv_path TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    TRUNCATE TABLE silver.teams_pressing;
    EXECUTE format(
        'COPY silver.teams_pressing FROM %L WITH (FORMAT csv, HEADER true)',
        p_csv_path
    );
    RAISE NOTICE 'silver.teams_pressing loaded from %', p_csv_path;
END;
$$;

-- ---------------------------------------------------------------------------
-- 5. load_teams_sequences
-- ---------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE silver.load_teams_sequences(p_csv_path TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    TRUNCATE TABLE silver.teams_sequences;
    EXECUTE format(
        'COPY silver.teams_sequences FROM %L WITH (FORMAT csv, HEADER true)',
        p_csv_path
    );
    RAISE NOTICE 'silver.teams_sequences loaded from %', p_csv_path;
END;
$$;

-- ---------------------------------------------------------------------------
-- 6. load_teams_misc
-- ---------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE silver.load_teams_misc(p_csv_path TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    TRUNCATE TABLE silver.teams_misc;
    EXECUTE format(
        'COPY silver.teams_misc FROM %L WITH (FORMAT csv, HEADER true)',
        p_csv_path
    );
    RAISE NOTICE 'silver.teams_misc loaded from %', p_csv_path;
END;
$$;

-- ---------------------------------------------------------------------------
-- 7. load_all_teams — Jalankan semua procedure sekaligus
-- ---------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE silver.load_all_teams(p_csv_dir TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    CALL silver.load_teams_attacking(p_csv_dir || '/teams_attacking.csv');
    CALL silver.load_teams_defending(p_csv_dir || '/teams_defending.csv');
    CALL silver.load_teams_passing(p_csv_dir || '/teams_passing.csv');
    CALL silver.load_teams_pressing(p_csv_dir || '/teams_pressing.csv');
    CALL silver.load_teams_sequences(p_csv_dir || '/teams_sequences.csv');
    CALL silver.load_teams_misc(p_csv_dir || '/teams_misc.csv');
    RAISE NOTICE 'All 6 teams tables loaded from %', p_csv_dir;
END;
$$;
