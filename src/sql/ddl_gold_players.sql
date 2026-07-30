-- ===========================================================================
-- Gold Layer — DDL Players (Star Schema)
-- ===========================================================================
-- dim_player                : Dimensi pemain (Surrogate Key + FK ke dim_team)
-- fact_player_statistics    : Fact outfield (attacking + defending + passing + carrying)
-- fact_goalkeeper_statistics : Fact goalkeeper (terpisah karena beda populasi)
--
-- Jalankan script ini sekali untuk membuat struktur tabel.
-- ===========================================================================

CREATE SCHEMA IF NOT EXISTS gold;

-- ---------------------------------------------------------------------------
-- DIMENSION: dim_player
-- ---------------------------------------------------------------------------
DROP TABLE IF EXISTS gold.fact_player_statistics;
DROP TABLE IF EXISTS gold.fact_goalkeeper_statistics;
DROP TABLE IF EXISTS gold.dim_player;

CREATE TABLE gold.dim_player (
    player_id       SERIAL         PRIMARY KEY,
    player_name     VARCHAR(150)   NOT NULL,
    team_id         INTEGER        NOT NULL REFERENCES gold.dim_team(team_id),
    UNIQUE (player_name, team_id)
);

-- ---------------------------------------------------------------------------
-- FACT: fact_player_statistics (outfield — 323 pemain)
-- ---------------------------------------------------------------------------
-- Gabungan: attacking + defending + passing + carrying
-- JOIN via LEFT JOIN karena ada 1 pemain dengan inkonsistensi nama (aksen)
-- ---------------------------------------------------------------------------
CREATE TABLE gold.fact_player_statistics (
    player_id                   INTEGER        NOT NULL REFERENCES gold.dim_player(player_id),
    team_id                     INTEGER        NOT NULL REFERENCES gold.dim_team(team_id),
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

    PRIMARY KEY (player_id)
);

-- ---------------------------------------------------------------------------
-- FACT: fact_goalkeeper_statistics (23 kiper)
-- ---------------------------------------------------------------------------
CREATE TABLE gold.fact_goalkeeper_statistics (
    player_id               INTEGER        NOT NULL REFERENCES gold.dim_player(player_id),
    team_id                 INTEGER        NOT NULL REFERENCES gold.dim_team(team_id),
    apps                    INTEGER        NOT NULL,
    mins                    INTEGER        NOT NULL,

    -- ===== GOALKEEPING =====
    gk_goals_conceded       INTEGER        NOT NULL,
    gk_saves_made           INTEGER        NOT NULL,
    gk_save_percentage      NUMERIC(5,2)   NOT NULL,
    gk_xgot_conceded        NUMERIC(10,2)  NOT NULL,
    gk_goals_prevented      NUMERIC(10,2)  NOT NULL,
    gk_gp_rate              NUMERIC(5,2)   NOT NULL,

    PRIMARY KEY (player_id)
);
