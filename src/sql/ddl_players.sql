-- ===========================================================================
-- Silver Layer — DDL Players
-- ===========================================================================
-- Membuat 5 tabel di schema silver untuk data pemain LaLiga.
-- Jalankan script ini sekali untuk membuat struktur tabel.
-- ===========================================================================

CREATE SCHEMA IF NOT EXISTS silver;

-- ---------------------------------------------------------------------------
-- 1. players_attacking
-- ---------------------------------------------------------------------------
DROP TABLE IF EXISTS silver.players_attacking;
CREATE TABLE silver.players_attacking (
    name                VARCHAR(150)   NOT NULL,
    club                VARCHAR(100)   NOT NULL,
    apps                INTEGER        NOT NULL,
    mins                INTEGER        NOT NULL,
    goals               INTEGER        NOT NULL,
    xg                  NUMERIC(10,2)  NOT NULL,
    goals_vs_xg         NUMERIC(10,2)  NOT NULL,
    shots               INTEGER        NOT NULL,
    sot                 INTEGER        NOT NULL,
    conv_pct            NUMERIC(5,2)   NOT NULL,
    xg_per_shot         NUMERIC(5,2)   NOT NULL,
    PRIMARY KEY (name, club)
);

-- ---------------------------------------------------------------------------
-- 2. players_defending
-- ---------------------------------------------------------------------------
DROP TABLE IF EXISTS silver.players_defending;
CREATE TABLE silver.players_defending (
    name                    VARCHAR(150)   NOT NULL,
    club                    VARCHAR(100)   NOT NULL,
    apps                    INTEGER        NOT NULL,
    mins                    INTEGER        NOT NULL,
    tackles                 INTEGER        NOT NULL,
    interceptions           INTEGER        NOT NULL,
    possession_won          INTEGER        NOT NULL,
    blocks                  INTEGER        NOT NULL,
    clearances              INTEGER        NOT NULL,
    ground_duels_total      INTEGER        NOT NULL,
    ground_duels_won        INTEGER        NOT NULL,
    ground_duels_pct        NUMERIC(5,2)   NOT NULL,
    aerial_duels_total      INTEGER        NOT NULL,
    aerial_duels_won        INTEGER        NOT NULL,
    aerial_duels_pct        NUMERIC(5,2)   NOT NULL,
    PRIMARY KEY (name, club)
);

-- ---------------------------------------------------------------------------
-- 3. players_passing
-- ---------------------------------------------------------------------------
DROP TABLE IF EXISTS silver.players_passing;
CREATE TABLE silver.players_passing (
    name                    VARCHAR(150)   NOT NULL,
    club                    VARCHAR(100)   NOT NULL,
    apps                    INTEGER        NOT NULL,
    mins                    INTEGER        NOT NULL,
    open_play_total         INTEGER        NOT NULL,
    open_play_successful    INTEGER        NOT NULL,
    open_play_pct           NUMERIC(5,2)   NOT NULL,
    final_third_total       INTEGER        NOT NULL,
    final_third_successful  INTEGER        NOT NULL,
    final_third_pct         NUMERIC(5,2)   NOT NULL,
    crosses_total           INTEGER        NOT NULL,
    crosses_successful      INTEGER        NOT NULL,
    crosses_pct             NUMERIC(5,2)   NOT NULL,
    through_balls           INTEGER        NOT NULL,
    PRIMARY KEY (name, club)
);

-- ---------------------------------------------------------------------------
-- 4. players_carrying
-- ---------------------------------------------------------------------------
DROP TABLE IF EXISTS silver.players_carrying;
CREATE TABLE silver.players_carrying (
    name                    VARCHAR(150)   NOT NULL,
    club                    VARCHAR(100)   NOT NULL,
    apps                    INTEGER        NOT NULL,
    mins                    INTEGER        NOT NULL,
    carries_total           INTEGER        NOT NULL,
    carries_distance        NUMERIC(10,2)  NOT NULL,
    carries_avg             NUMERIC(5,2)   NOT NULL,
    progressive_total       INTEGER        NOT NULL,
    progressive_distance    NUMERIC(10,2)  NOT NULL,
    progressive_avg         NUMERIC(5,2)   NOT NULL,
    ended_with_shot         INTEGER        NOT NULL,
    ended_with_goal         INTEGER        NOT NULL,
    ended_with_chance       INTEGER        NOT NULL,
    ended_with_assist       INTEGER        NOT NULL,
    PRIMARY KEY (name, club)
);

-- ---------------------------------------------------------------------------
-- 5. players_goalkeeping
-- ---------------------------------------------------------------------------
DROP TABLE IF EXISTS silver.players_goalkeeping;
CREATE TABLE silver.players_goalkeeping (
    name                VARCHAR(150)   NOT NULL,
    club                VARCHAR(100)   NOT NULL,
    apps                INTEGER        NOT NULL,
    mins                INTEGER        NOT NULL,
    goals_conceded      INTEGER        NOT NULL,
    saves_made          INTEGER        NOT NULL,
    save_percentage     NUMERIC(5,2)   NOT NULL,
    xgot_conceded       NUMERIC(10,2)  NOT NULL,
    goals_prevented     NUMERIC(10,2)  NOT NULL,
    gp_rate             NUMERIC(5,2)   NOT NULL,
    PRIMARY KEY (name, club)
);
