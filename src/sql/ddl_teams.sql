-- ===========================================================================
-- Silver Layer — DDL Teams
-- ===========================================================================
-- Membuat 6 tabel di schema silver untuk data tim LaLiga.
-- Jalankan script ini sekali untuk membuat struktur tabel.
-- ===========================================================================

CREATE SCHEMA IF NOT EXISTS silver;

-- ---------------------------------------------------------------------------
-- 1. teams_attacking
-- ---------------------------------------------------------------------------
DROP TABLE IF EXISTS silver.teams_attacking;
CREATE TABLE silver.teams_attacking (
    club                VARCHAR(100)   NOT NULL,
    played              INTEGER        NOT NULL,
    goals               INTEGER        NOT NULL,
    xg                  NUMERIC(10,2)  NOT NULL,
    goals_vs_xg         NUMERIC(10,2)  NOT NULL,
    shots               INTEGER        NOT NULL,
    sot                 INTEGER        NOT NULL,
    conversion_pct      NUMERIC(5,2)   NOT NULL,
    xg_per_shot         NUMERIC(5,2)   NOT NULL,
    PRIMARY KEY (club)
);

-- ---------------------------------------------------------------------------
-- 2. teams_defending
-- ---------------------------------------------------------------------------
DROP TABLE IF EXISTS silver.teams_defending;
CREATE TABLE silver.teams_defending (
    club                    VARCHAR(100)   NOT NULL,
    played                  INTEGER        NOT NULL,
    avg_possession_pct      NUMERIC(5,2)   NOT NULL,
    tackles                 INTEGER        NOT NULL,
    interceptions           INTEGER        NOT NULL,
    possession_won          INTEGER        NOT NULL,
    blocks                  INTEGER        NOT NULL,
    clearances              INTEGER        NOT NULL,
    ground_duels_won_pct    NUMERIC(5,2)   NOT NULL,
    aerial_duels_won_pct    NUMERIC(5,2)   NOT NULL,
    PRIMARY KEY (club)
);

-- ---------------------------------------------------------------------------
-- 3. teams_passing
-- ---------------------------------------------------------------------------
DROP TABLE IF EXISTS silver.teams_passing;
CREATE TABLE silver.teams_passing (
    club                    VARCHAR(100)   NOT NULL,
    played                  INTEGER        NOT NULL,
    avg_possession_pct      NUMERIC(5,2)   NOT NULL,
    passes_total            INTEGER        NOT NULL,
    passes_successful       INTEGER        NOT NULL,
    passes_pct              NUMERIC(5,2)   NOT NULL,
    final_third_total       INTEGER        NOT NULL,
    final_third_successful  INTEGER        NOT NULL,
    final_third_pct         NUMERIC(5,2)   NOT NULL,
    direction_fwd_pct       NUMERIC(5,2)   NOT NULL,
    direction_bwd_pct       NUMERIC(5,2)   NOT NULL,
    direction_left_pct      NUMERIC(5,2)   NOT NULL,
    direction_right_pct     NUMERIC(5,2)   NOT NULL,
    crosses_total           INTEGER        NOT NULL,
    crosses_successful      INTEGER        NOT NULL,
    crosses_pct             NUMERIC(5,2)   NOT NULL,
    through_balls           INTEGER        NOT NULL,
    PRIMARY KEY (club)
);

-- ---------------------------------------------------------------------------
-- 4. teams_pressing
-- ---------------------------------------------------------------------------
DROP TABLE IF EXISTS silver.teams_pressing;
CREATE TABLE silver.teams_pressing (
    club                        VARCHAR(100)   NOT NULL,
    played                      INTEGER        NOT NULL,
    pressed_seqs                INTEGER        NOT NULL,
    ppda                        NUMERIC(5,2)   NOT NULL,
    start_distance              NUMERIC(5,2)   NOT NULL,
    high_turnovers_total        INTEGER        NOT NULL,
    high_turnovers_shot_ending  INTEGER        NOT NULL,
    high_turnovers_goal_ending  INTEGER        NOT NULL,
    high_turnovers_shot_pct     NUMERIC(5,2)   NOT NULL,
    PRIMARY KEY (club)
);

-- ---------------------------------------------------------------------------
-- 5. teams_sequences
-- ---------------------------------------------------------------------------
DROP TABLE IF EXISTS silver.teams_sequences;
CREATE TABLE silver.teams_sequences (
    club                    VARCHAR(100)   NOT NULL,
    played                  INTEGER        NOT NULL,
    passes_10_plus          INTEGER        NOT NULL,
    direct_speed            NUMERIC(5,2)   NOT NULL,
    passes_per_seq          NUMERIC(5,2)   NOT NULL,
    sequence_time           NUMERIC(6,2)   NOT NULL,
    buildups_total          INTEGER        NOT NULL,
    buildups_goals          INTEGER        NOT NULL,
    direct_attacks_total    INTEGER        NOT NULL,
    direct_attacks_goals    INTEGER        NOT NULL,
    PRIMARY KEY (club)
);

-- ---------------------------------------------------------------------------
-- 6. teams_misc
-- ---------------------------------------------------------------------------
DROP TABLE IF EXISTS silver.teams_misc;
CREATE TABLE silver.teams_misc (
    club                VARCHAR(100)   NOT NULL,
    subs_used           INTEGER        NOT NULL,
    subs_goals          INTEGER        NOT NULL,
    errors_lead_to_shot INTEGER        NOT NULL,
    errors_lead_to_goal INTEGER        NOT NULL,
    fouled              INTEGER        NOT NULL,
    yellows             INTEGER        NOT NULL,
    reds                INTEGER        NOT NULL,
    pens_won            INTEGER        NOT NULL,
    fouls               INTEGER        NOT NULL,
    opp_yellows         INTEGER        NOT NULL,
    opp_reds            INTEGER        NOT NULL,
    pens_conceded       INTEGER        NOT NULL,
    PRIMARY KEY (club)
);
