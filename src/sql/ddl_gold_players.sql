-- ===========================================================================
-- Gold Layer — DDL Players (One Big Table)
-- ===========================================================================
-- gold.player_statistics     : OBT outfield (attacking + defending + passing + carrying)
-- gold.goalkeeper_statistics  : OBT goalkeeper (terpisah karena beda populasi)
--
-- Jalankan script ini sekali untuk membuat struktur tabel.
-- ===========================================================================

CREATE SCHEMA IF NOT EXISTS gold;

-- ---------------------------------------------------------------------------
-- gold.player_statistics (outfield — 323 pemain)
-- ---------------------------------------------------------------------------
-- Gabungan: attacking + defending + passing + carrying
-- Kolom stat NULLable karena ada 1 pemain (Javi Lopez/López) dengan
-- inkonsistensi nama aksen antar tabel silver.
-- ---------------------------------------------------------------------------
DROP TABLE IF EXISTS gold.player_statistics;

CREATE TABLE gold.player_statistics (
    player_name                 VARCHAR(150)   NOT NULL,
    club                        VARCHAR(100)   NOT NULL,
    apps                        INTEGER        NOT NULL,
    mins                        INTEGER        NOT NULL,

    -- ===== ATTACKING =====
    att_goals                   INTEGER,
    att_xg                      NUMERIC(10,2),
    att_goals_vs_xg             NUMERIC(10,2),
    att_shots                   INTEGER,
    att_sot                     INTEGER,
    att_conv_pct                NUMERIC(5,2),
    att_xg_per_shot             NUMERIC(5,2),

    -- ===== DEFENDING =====
    def_tackles                 INTEGER,
    def_interceptions           INTEGER,
    def_possession_won          INTEGER,
    def_blocks                  INTEGER,
    def_clearances              INTEGER,
    def_ground_duels_total      INTEGER,
    def_ground_duels_won        INTEGER,
    def_ground_duels_pct        NUMERIC(5,2),
    def_aerial_duels_total      INTEGER,
    def_aerial_duels_won        INTEGER,
    def_aerial_duels_pct        NUMERIC(5,2),

    -- ===== PASSING =====
    pas_open_play_total         INTEGER,
    pas_open_play_successful    INTEGER,
    pas_open_play_pct           NUMERIC(5,2),
    pas_final_third_total       INTEGER,
    pas_final_third_successful  INTEGER,
    pas_final_third_pct         NUMERIC(5,2),
    pas_crosses_total           INTEGER,
    pas_crosses_successful      INTEGER,
    pas_crosses_pct             NUMERIC(5,2),
    pas_through_balls           INTEGER,

    -- ===== CARRYING =====
    car_carries_total           INTEGER,
    car_carries_distance        NUMERIC(10,2),
    car_carries_avg             NUMERIC(5,2),
    car_progressive_total       INTEGER,
    car_progressive_distance    NUMERIC(10,2),
    car_progressive_avg         NUMERIC(5,2),
    car_ended_with_shot         INTEGER,
    car_ended_with_goal         INTEGER,
    car_ended_with_chance       INTEGER,
    car_ended_with_assist       INTEGER,

    PRIMARY KEY (player_name, club)
);

-- ---------------------------------------------------------------------------
-- gold.goalkeeper_statistics (23 kiper)
-- ---------------------------------------------------------------------------
DROP TABLE IF EXISTS gold.goalkeeper_statistics;

CREATE TABLE gold.goalkeeper_statistics (
    player_name             VARCHAR(150)   NOT NULL,
    club                    VARCHAR(100)   NOT NULL,
    apps                    INTEGER        NOT NULL,
    mins                    INTEGER        NOT NULL,

    -- ===== GOALKEEPING =====
    gk_goals_conceded       INTEGER        NOT NULL,
    gk_saves_made           INTEGER        NOT NULL,
    gk_save_percentage      NUMERIC(5,2)   NOT NULL,
    gk_xgot_conceded        NUMERIC(10,2)  NOT NULL,
    gk_goals_prevented      NUMERIC(10,2)  NOT NULL,
    gk_gp_rate              NUMERIC(5,2)   NOT NULL,

    PRIMARY KEY (player_name, club)
);
