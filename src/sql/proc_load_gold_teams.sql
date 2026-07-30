-- ===========================================================================
-- Gold Layer — Load Teams (One Big Table)
-- ===========================================================================
-- Memuat data dari Silver ke Gold:
--   gold.teams_statistics ← JOIN 6 tabel silver + derived per-game
--
-- CARA PAKAI:
--   Opsi 1: Jalankan statement satu per satu di DBeaver.
--   Opsi 2: CALL gold.load_teams_gold();
-- ===========================================================================


-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-- BAGIAN 1 — Statement langsung (bisa dijalankan satu per satu di DBeaver)
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TRUNCATE TABLE gold.teams_statistics;

INSERT INTO gold.teams_statistics (
    club, played,
    -- attacking
    att_goals, att_xg, att_goals_vs_xg, att_shots, att_sot, att_conversion_pct, att_xg_per_shot,
    -- defending
    def_avg_possession_pct, def_tackles, def_interceptions, def_possession_won,
    def_blocks, def_clearances, def_ground_duels_won_pct, def_aerial_duels_won_pct,
    -- passing
    pas_passes_total, pas_passes_successful, pas_passes_pct,
    pas_final_third_total, pas_final_third_successful, pas_final_third_pct,
    pas_direction_fwd_pct, pas_direction_bwd_pct, pas_direction_left_pct, pas_direction_right_pct,
    pas_crosses_total, pas_crosses_successful, pas_crosses_pct, pas_through_balls,
    -- pressing
    prs_pressed_seqs, prs_ppda, prs_start_distance,
    prs_high_turnovers_total, prs_high_turnovers_shot_ending, prs_high_turnovers_goal_ending, prs_high_turnovers_shot_pct,
    -- sequences
    seq_passes_10_plus, seq_direct_speed, seq_passes_per_seq, seq_sequence_time,
    seq_buildups_total, seq_buildups_goals, seq_direct_attacks_total, seq_direct_attacks_goals,
    -- misc
    msc_subs_used, msc_subs_goals, msc_errors_lead_to_shot, msc_errors_lead_to_goal,
    msc_fouled, msc_yellows, msc_reds, msc_pens_won,
    msc_fouls, msc_opp_yellows, msc_opp_reds, msc_pens_conceded,
    -- derived per-game
    att_goals_per_game, att_shots_per_game, att_xg_per_game,
    def_tackles_per_game, def_interceptions_per_game,
    pas_passes_per_game, pas_crosses_per_game, pas_through_balls_per_game,
    prs_pressed_seqs_per_game,
    seq_buildups_per_game, seq_direct_attacks_per_game,
    msc_fouls_per_game, msc_yellows_per_game
)
SELECT
    a.club,
    a.played,
    -- attacking
    a.goals, a.xg, a.goals_vs_xg, a.shots, a.sot, a.conversion_pct, a.xg_per_shot,
    -- defending
    df.avg_possession_pct, df.tackles, df.interceptions, df.possession_won,
    df.blocks, df.clearances, df.ground_duels_won_pct, df.aerial_duels_won_pct,
    -- passing
    p.passes_total, p.passes_successful, p.passes_pct,
    p.final_third_total, p.final_third_successful, p.final_third_pct,
    p.direction_fwd_pct, p.direction_bwd_pct, p.direction_left_pct, p.direction_right_pct,
    p.crosses_total, p.crosses_successful, p.crosses_pct, p.through_balls,
    -- pressing
    pr.pressed_seqs, pr.ppda, pr.start_distance,
    pr.high_turnovers_total, pr.high_turnovers_shot_ending, pr.high_turnovers_goal_ending, pr.high_turnovers_shot_pct,
    -- sequences
    s.passes_10_plus, s.direct_speed, s.passes_per_seq, s.sequence_time,
    s.buildups_total, s.buildups_goals, s.direct_attacks_total, s.direct_attacks_goals,
    -- misc
    m.subs_used, m.subs_goals, m.errors_lead_to_shot, m.errors_lead_to_goal,
    m.fouled, m.yellows, m.reds, m.pens_won,
    m.fouls, m.opp_yellows, m.opp_reds, m.pens_conceded,
    -- derived per-game
    ROUND(a.goals::NUMERIC     / a.played, 2),
    ROUND(a.shots::NUMERIC     / a.played, 2),
    ROUND(a.xg::NUMERIC        / a.played, 2),
    ROUND(df.tackles::NUMERIC  / a.played, 2),
    ROUND(df.interceptions::NUMERIC / a.played, 2),
    ROUND(p.passes_total::NUMERIC   / a.played, 2),
    ROUND(p.crosses_total::NUMERIC  / a.played, 2),
    ROUND(p.through_balls::NUMERIC  / a.played, 2),
    ROUND(pr.pressed_seqs::NUMERIC  / a.played, 2),
    ROUND(s.buildups_total::NUMERIC      / a.played, 2),
    ROUND(s.direct_attacks_total::NUMERIC / a.played, 2),
    ROUND(m.fouls::NUMERIC   / a.played, 2),
    ROUND(m.yellows::NUMERIC / a.played, 2)
FROM silver.teams_attacking  a
JOIN silver.teams_defending  df ON df.club = a.club
JOIN silver.teams_passing    p  ON p.club  = a.club
JOIN silver.teams_pressing   pr ON pr.club = a.club
JOIN silver.teams_sequences  s  ON s.club  = a.club
JOIN silver.teams_misc       m  ON m.club  = a.club;


-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-- BAGIAN 2 — Procedure (membungkus semua statement di atas)
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CREATE OR REPLACE PROCEDURE gold.load_teams_gold()
LANGUAGE plpgsql
AS $$
BEGIN
    TRUNCATE TABLE gold.teams_statistics;

    INSERT INTO gold.teams_statistics (
        club, played,
        att_goals, att_xg, att_goals_vs_xg, att_shots, att_sot, att_conversion_pct, att_xg_per_shot,
        def_avg_possession_pct, def_tackles, def_interceptions, def_possession_won,
        def_blocks, def_clearances, def_ground_duels_won_pct, def_aerial_duels_won_pct,
        pas_passes_total, pas_passes_successful, pas_passes_pct,
        pas_final_third_total, pas_final_third_successful, pas_final_third_pct,
        pas_direction_fwd_pct, pas_direction_bwd_pct, pas_direction_left_pct, pas_direction_right_pct,
        pas_crosses_total, pas_crosses_successful, pas_crosses_pct, pas_through_balls,
        prs_pressed_seqs, prs_ppda, prs_start_distance,
        prs_high_turnovers_total, prs_high_turnovers_shot_ending, prs_high_turnovers_goal_ending, prs_high_turnovers_shot_pct,
        seq_passes_10_plus, seq_direct_speed, seq_passes_per_seq, seq_sequence_time,
        seq_buildups_total, seq_buildups_goals, seq_direct_attacks_total, seq_direct_attacks_goals,
        msc_subs_used, msc_subs_goals, msc_errors_lead_to_shot, msc_errors_lead_to_goal,
        msc_fouled, msc_yellows, msc_reds, msc_pens_won,
        msc_fouls, msc_opp_yellows, msc_opp_reds, msc_pens_conceded,
        att_goals_per_game, att_shots_per_game, att_xg_per_game,
        def_tackles_per_game, def_interceptions_per_game,
        pas_passes_per_game, pas_crosses_per_game, pas_through_balls_per_game,
        prs_pressed_seqs_per_game,
        seq_buildups_per_game, seq_direct_attacks_per_game,
        msc_fouls_per_game, msc_yellows_per_game
    )
    SELECT
        a.club,
        a.played,
        a.goals, a.xg, a.goals_vs_xg, a.shots, a.sot, a.conversion_pct, a.xg_per_shot,
        df.avg_possession_pct, df.tackles, df.interceptions, df.possession_won,
        df.blocks, df.clearances, df.ground_duels_won_pct, df.aerial_duels_won_pct,
        p.passes_total, p.passes_successful, p.passes_pct,
        p.final_third_total, p.final_third_successful, p.final_third_pct,
        p.direction_fwd_pct, p.direction_bwd_pct, p.direction_left_pct, p.direction_right_pct,
        p.crosses_total, p.crosses_successful, p.crosses_pct, p.through_balls,
        pr.pressed_seqs, pr.ppda, pr.start_distance,
        pr.high_turnovers_total, pr.high_turnovers_shot_ending, pr.high_turnovers_goal_ending, pr.high_turnovers_shot_pct,
        s.passes_10_plus, s.direct_speed, s.passes_per_seq, s.sequence_time,
        s.buildups_total, s.buildups_goals, s.direct_attacks_total, s.direct_attacks_goals,
        m.subs_used, m.subs_goals, m.errors_lead_to_shot, m.errors_lead_to_goal,
        m.fouled, m.yellows, m.reds, m.pens_won,
        m.fouls, m.opp_yellows, m.opp_reds, m.pens_conceded,
        ROUND(a.goals::NUMERIC     / a.played, 2),
        ROUND(a.shots::NUMERIC     / a.played, 2),
        ROUND(a.xg::NUMERIC        / a.played, 2),
        ROUND(df.tackles::NUMERIC  / a.played, 2),
        ROUND(df.interceptions::NUMERIC / a.played, 2),
        ROUND(p.passes_total::NUMERIC   / a.played, 2),
        ROUND(p.crosses_total::NUMERIC  / a.played, 2),
        ROUND(p.through_balls::NUMERIC  / a.played, 2),
        ROUND(pr.pressed_seqs::NUMERIC  / a.played, 2),
        ROUND(s.buildups_total::NUMERIC      / a.played, 2),
        ROUND(s.direct_attacks_total::NUMERIC / a.played, 2),
        ROUND(m.fouls::NUMERIC   / a.played, 2),
        ROUND(m.yellows::NUMERIC / a.played, 2)
    FROM silver.teams_attacking  a
    JOIN silver.teams_defending  df ON df.club = a.club
    JOIN silver.teams_passing    p  ON p.club  = a.club
    JOIN silver.teams_pressing   pr ON pr.club = a.club
    JOIN silver.teams_sequences  s  ON s.club  = a.club
    JOIN silver.teams_misc       m  ON m.club  = a.club;

    RAISE NOTICE 'gold.teams_statistics loaded';
END;
$$;
