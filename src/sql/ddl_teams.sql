-- ===========================================================================
-- Silver Layer — DDL Teams
-- ===========================================================================
-- Membuat 12 tabel di schema silver untuk data tim LaLiga.
-- Tabel dikelompokkan: 4 attacking, 4 defending, passing, pressing,
--                       sequences, misc.
-- Jalankan script ini sekali untuk membuat struktur tabel.
-- ===========================================================================

CREATE SCHEMA IF NOT EXISTS silver;


-- ===========================================================================
-- ATTACKING (4 tabel)
-- ===========================================================================

-- ---------------------------------------------------------------------------
-- 1. teams_attacking_overall
-- ---------------------------------------------------------------------------
DROP TABLE IF EXISTS silver.teams_attacking_overall;
CREATE TABLE silver.teams_attacking_overall (
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
-- 2. teams_attacking_non_penalty
-- ---------------------------------------------------------------------------
DROP TABLE IF EXISTS silver.teams_attacking_non_penalty;
CREATE TABLE silver.teams_attacking_non_penalty (
    club                VARCHAR(100)   NOT NULL,
    played              INTEGER        NOT NULL,
    goals               INTEGER        NOT NULL,
    xg                  NUMERIC(10,2)  NOT NULL,
    goals_vs_xg         NUMERIC(10,2)  NOT NULL,
    shots               INTEGER        NOT NULL,
    sot                 INTEGER        NOT NULL,
    conv_pct            NUMERIC(5,2)   NOT NULL,
    xg_per_shot         NUMERIC(5,2)   NOT NULL,
    PRIMARY KEY (club)
);

-- ---------------------------------------------------------------------------
-- 3. teams_attacking_set_pieces
-- ---------------------------------------------------------------------------
DROP TABLE IF EXISTS silver.teams_attacking_set_pieces;
CREATE TABLE silver.teams_attacking_set_pieces (
    club                VARCHAR(100)   NOT NULL,
    played              INTEGER        NOT NULL,
    goals               INTEGER        NOT NULL,
    shots               INTEGER        NOT NULL,
    xg                  NUMERIC(10,2)  NOT NULL,
    goal_pct            NUMERIC(5,2)   NOT NULL,
    shot_pct            NUMERIC(5,2)   NOT NULL,
    xg_pct              NUMERIC(5,2)   NOT NULL,
    PRIMARY KEY (club)
);

-- ---------------------------------------------------------------------------
-- 4. teams_attacking_misc
-- ---------------------------------------------------------------------------
DROP TABLE IF EXISTS silver.teams_attacking_misc;
CREATE TABLE silver.teams_attacking_misc (
    club                VARCHAR(100)   NOT NULL,
    played              INTEGER        NOT NULL,
    touches_in_box      INTEGER        NOT NULL,
    hit_woodwork        INTEGER        NOT NULL,
    offsides            INTEGER        NOT NULL,
    penalties_total     INTEGER        NOT NULL,
    penalties_goals     INTEGER        NOT NULL,
    free_kicks_total    INTEGER        NOT NULL,
    free_kicks_goals    INTEGER        NOT NULL,
    headers_total       INTEGER        NOT NULL,
    headers_goals       INTEGER        NOT NULL,
    fast_breaks_total   INTEGER        NOT NULL,
    fast_breaks_goals   INTEGER        NOT NULL,
    PRIMARY KEY (club)
);


-- ===========================================================================
-- DEFENDING (4 tabel)
-- ===========================================================================

-- ---------------------------------------------------------------------------
-- 5. teams_defending_defensive_action
-- ---------------------------------------------------------------------------
DROP TABLE IF EXISTS silver.teams_defending_defensive_action;
CREATE TABLE silver.teams_defending_defensive_action (
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
-- 6. teams_defending_overall
-- ---------------------------------------------------------------------------
DROP TABLE IF EXISTS silver.teams_defending_overall;
CREATE TABLE silver.teams_defending_overall (
    club                VARCHAR(100)   NOT NULL,
    played              INTEGER        NOT NULL,
    goals               INTEGER        NOT NULL,
    xg                  NUMERIC(10,2)  NOT NULL,
    goals_vs_xg         NUMERIC(10,2)  NOT NULL,
    shots               INTEGER        NOT NULL,
    sot                 INTEGER        NOT NULL,
    conv_pct            NUMERIC(5,2)   NOT NULL,
    xg_per_shot         NUMERIC(5,2)   NOT NULL,
    shots_in_box_pct    NUMERIC(5,2)   NOT NULL,
    goals_in_box_pct    NUMERIC(5,2)   NOT NULL,
    PRIMARY KEY (club)
);

-- ---------------------------------------------------------------------------
-- 7. teams_defending_set_piece
-- ---------------------------------------------------------------------------
DROP TABLE IF EXISTS silver.teams_defending_set_piece;
CREATE TABLE silver.teams_defending_set_piece (
    club                VARCHAR(100)   NOT NULL,
    played              INTEGER        NOT NULL,
    goals               INTEGER        NOT NULL,
    shots               INTEGER        NOT NULL,
    xg                  NUMERIC(10,2)  NOT NULL,
    goal_pct            NUMERIC(5,2)   NOT NULL,
    shot_pct            NUMERIC(5,2)   NOT NULL,
    xg_pct              NUMERIC(5,2)   NOT NULL,
    PRIMARY KEY (club)
);

-- ---------------------------------------------------------------------------
-- 8. teams_defending_misc
-- ---------------------------------------------------------------------------
DROP TABLE IF EXISTS silver.teams_defending_misc;
CREATE TABLE silver.teams_defending_misc (
    club                VARCHAR(100)   NOT NULL,
    played              INTEGER        NOT NULL,
    touches_in_box      INTEGER        NOT NULL,
    hit_woodwork        INTEGER        NOT NULL,
    offsides            INTEGER        NOT NULL,
    penalties_total     INTEGER        NOT NULL,
    penalties_goals     INTEGER        NOT NULL,
    free_kicks_total    INTEGER        NOT NULL,
    free_kicks_goals    INTEGER        NOT NULL,
    headers_total       INTEGER        NOT NULL,
    headers_goals       INTEGER        NOT NULL,
    fast_breaks_total   INTEGER        NOT NULL,
    fast_breaks_goals   INTEGER        NOT NULL,
    PRIMARY KEY (club)
);


-- ===========================================================================
-- LAINNYA (4 tabel — tidak berubah)
-- ===========================================================================

-- ---------------------------------------------------------------------------
-- 9. teams_passing
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
-- 10. teams_pressing
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
-- 11. teams_sequences
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
-- 12. teams_misc
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
