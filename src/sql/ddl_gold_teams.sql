-- ===========================================================================
-- Gold Layer — DDL Teams (One Big Table)
-- ===========================================================================
-- gold.teams_statistics : Satu tabel gabungan 6 kategori statistik tim
--                         + derived per-game metrics
--
-- Jalankan script ini sekali untuk membuat struktur tabel.
-- ===========================================================================

CREATE SCHEMA IF NOT EXISTS gold;

-- ---------------------------------------------------------------------------
-- gold.teams_statistics
-- ---------------------------------------------------------------------------
DROP TABLE IF EXISTS gold.teams_statistics;

CREATE TABLE gold.teams_statistics (
    club                            VARCHAR(100)   NOT NULL PRIMARY KEY,
    played                          INTEGER        NOT NULL,

    -- ===== ATTACKING =====
    att_goals                       INTEGER        NOT NULL,
    att_xg                          NUMERIC(10,2)  NOT NULL,
    att_goals_vs_xg                 NUMERIC(10,2)  NOT NULL,
    att_shots                       INTEGER        NOT NULL,
    att_sot                         INTEGER        NOT NULL,
    att_conversion_pct              NUMERIC(5,2)   NOT NULL,
    att_xg_per_shot                 NUMERIC(5,2)   NOT NULL,

    -- ===== DEFENDING =====
    def_avg_possession_pct          NUMERIC(5,2)   NOT NULL,
    def_tackles                     INTEGER        NOT NULL,
    def_interceptions               INTEGER        NOT NULL,
    def_possession_won              INTEGER        NOT NULL,
    def_blocks                      INTEGER        NOT NULL,
    def_clearances                  INTEGER        NOT NULL,
    def_ground_duels_won_pct        NUMERIC(5,2)   NOT NULL,
    def_aerial_duels_won_pct        NUMERIC(5,2)   NOT NULL,

    -- ===== PASSING =====
    pas_passes_total                INTEGER        NOT NULL,
    pas_passes_successful           INTEGER        NOT NULL,
    pas_passes_pct                  NUMERIC(5,2)   NOT NULL,
    pas_final_third_total           INTEGER        NOT NULL,
    pas_final_third_successful      INTEGER        NOT NULL,
    pas_final_third_pct             NUMERIC(5,2)   NOT NULL,
    pas_direction_fwd_pct           NUMERIC(5,2)   NOT NULL,
    pas_direction_bwd_pct           NUMERIC(5,2)   NOT NULL,
    pas_direction_left_pct          NUMERIC(5,2)   NOT NULL,
    pas_direction_right_pct         NUMERIC(5,2)   NOT NULL,
    pas_crosses_total               INTEGER        NOT NULL,
    pas_crosses_successful          INTEGER        NOT NULL,
    pas_crosses_pct                 NUMERIC(5,2)   NOT NULL,
    pas_through_balls               INTEGER        NOT NULL,

    -- ===== PRESSING =====
    prs_pressed_seqs                INTEGER        NOT NULL,
    prs_ppda                        NUMERIC(5,2)   NOT NULL,
    prs_start_distance              NUMERIC(5,2)   NOT NULL,
    prs_high_turnovers_total        INTEGER        NOT NULL,
    prs_high_turnovers_shot_ending  INTEGER        NOT NULL,
    prs_high_turnovers_goal_ending  INTEGER        NOT NULL,
    prs_high_turnovers_shot_pct     NUMERIC(5,2)   NOT NULL,

    -- ===== SEQUENCES =====
    seq_passes_10_plus              INTEGER        NOT NULL,
    seq_direct_speed                NUMERIC(5,2)   NOT NULL,
    seq_passes_per_seq              NUMERIC(5,2)   NOT NULL,
    seq_sequence_time               NUMERIC(6,2)   NOT NULL,
    seq_buildups_total              INTEGER        NOT NULL,
    seq_buildups_goals              INTEGER        NOT NULL,
    seq_direct_attacks_total        INTEGER        NOT NULL,
    seq_direct_attacks_goals        INTEGER        NOT NULL,

    -- ===== MISC =====
    msc_subs_used                   INTEGER        NOT NULL,
    msc_subs_goals                  INTEGER        NOT NULL,
    msc_errors_lead_to_shot         INTEGER        NOT NULL,
    msc_errors_lead_to_goal         INTEGER        NOT NULL,
    msc_fouled                      INTEGER        NOT NULL,
    msc_yellows                     INTEGER        NOT NULL,
    msc_reds                        INTEGER        NOT NULL,
    msc_pens_won                    INTEGER        NOT NULL,
    msc_fouls                       INTEGER        NOT NULL,
    msc_opp_yellows                 INTEGER        NOT NULL,
    msc_opp_reds                    INTEGER        NOT NULL,
    msc_pens_conceded               INTEGER        NOT NULL,

    -- ===== DERIVED PER-GAME METRICS =====
    att_goals_per_game              NUMERIC(5,2)   NOT NULL,
    att_shots_per_game              NUMERIC(5,2)   NOT NULL,
    att_xg_per_game                 NUMERIC(5,2)   NOT NULL,
    def_tackles_per_game            NUMERIC(5,2)   NOT NULL,
    def_interceptions_per_game      NUMERIC(5,2)   NOT NULL,
    pas_passes_per_game             NUMERIC(7,2)   NOT NULL,
    pas_crosses_per_game            NUMERIC(5,2)   NOT NULL,
    pas_through_balls_per_game      NUMERIC(5,2)   NOT NULL,
    prs_pressed_seqs_per_game       NUMERIC(5,2)   NOT NULL,
    seq_buildups_per_game           NUMERIC(5,2)   NOT NULL,
    seq_direct_attacks_per_game     NUMERIC(5,2)   NOT NULL,
    msc_fouls_per_game              NUMERIC(5,2)   NOT NULL,
    msc_yellows_per_game            NUMERIC(5,2)   NOT NULL
);
