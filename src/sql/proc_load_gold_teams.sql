-- ===========================================================================
-- Gold Layer — Load Teams (One Big Table)
-- ===========================================================================
-- Memuat data dari Silver ke Gold:
--   gold.teams_statistics ← JOIN 12 tabel silver + derived per-game
--
-- CARA PAKAI:
--   CALL gold.load_teams_gold();
-- ===========================================================================


-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-- PROCEDURE
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CREATE OR REPLACE PROCEDURE gold.load_teams_gold()
LANGUAGE plpgsql
AS $$
BEGIN
    TRUNCATE TABLE gold.teams_statistics;

    INSERT INTO gold.teams_statistics (
        club, played,
        -- attacking overall
        att_goals, att_xg, att_goals_vs_xg, att_shots, att_sot, att_conversion_pct, att_xg_per_shot,
        -- attacking non-penalty
        att_np_goals, att_np_xg, att_np_goals_vs_xg, att_np_shots, att_np_sot, att_np_conv_pct, att_np_xg_per_shot,
        -- attacking set-pieces
        att_sp_goals, att_sp_shots, att_sp_xg, att_sp_goal_pct, att_sp_shot_pct, att_sp_xg_pct,
        -- attacking misc
        att_touches_in_box, att_hit_woodwork, att_offsides,
        att_penalties_total, att_penalties_goals,
        att_free_kicks_total, att_free_kicks_goals,
        att_headers_total, att_headers_goals,
        att_fast_breaks_total, att_fast_breaks_goals,
        -- defending defensive action
        def_avg_possession_pct, def_tackles, def_interceptions, def_possession_won,
        def_blocks, def_clearances, def_ground_duels_won_pct, def_aerial_duels_won_pct,
        -- defending overall
        def_goals_conceded, def_xg_against, def_goals_vs_xg_against,
        def_shots_against, def_sot_against, def_conv_pct_against, def_xg_per_shot_against,
        def_shots_in_box_pct, def_goals_in_box_pct,
        -- defending set-piece
        def_sp_goals, def_sp_shots, def_sp_xg, def_sp_goal_pct, def_sp_shot_pct, def_sp_xg_pct,
        -- defending misc
        def_touches_in_box, def_hit_woodwork, def_offsides,
        def_penalties_total, def_penalties_goals,
        def_free_kicks_total, def_free_kicks_goals,
        def_headers_total, def_headers_goals,
        def_fast_breaks_total, def_fast_breaks_goals,
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
        att_fast_breaks_per_game, att_touches_in_box_per_game,
        def_tackles_per_game, def_interceptions_per_game, def_goals_conceded_per_game,
        pas_passes_per_game, pas_crosses_per_game, pas_through_balls_per_game,
        prs_pressed_seqs_per_game,
        seq_buildups_per_game, seq_direct_attacks_per_game,
        msc_fouls_per_game, msc_yellows_per_game
    )
    SELECT
        a.club,
        a.played,
        -- attacking overall
        a.goals, a.xg, a.goals_vs_xg, a.shots, a.sot, a.conversion_pct, a.xg_per_shot,
        -- attacking non-penalty
        anp.goals, anp.xg, anp.goals_vs_xg, anp.shots, anp.sot, anp.conv_pct, anp.xg_per_shot,
        -- attacking set-pieces
        asp.goals, asp.shots, asp.xg, asp.goal_pct, asp.shot_pct, asp.xg_pct,
        -- attacking misc
        am.touches_in_box, am.hit_woodwork, am.offsides,
        am.penalties_total, am.penalties_goals,
        am.free_kicks_total, am.free_kicks_goals,
        am.headers_total, am.headers_goals,
        am.fast_breaks_total, am.fast_breaks_goals,
        -- defending defensive action
        dda.avg_possession_pct, dda.tackles, dda.interceptions, dda.possession_won,
        dda.blocks, dda.clearances, dda.ground_duels_won_pct, dda.aerial_duels_won_pct,
        -- defending overall
        do2.goals, do2.xg, do2.goals_vs_xg, do2.shots, do2.sot, do2.conv_pct, do2.xg_per_shot,
        do2.shots_in_box_pct, do2.goals_in_box_pct,
        -- defending set-piece
        dsp.goals, dsp.shots, dsp.xg, dsp.goal_pct, dsp.shot_pct, dsp.xg_pct,
        -- defending misc
        dm.touches_in_box, dm.hit_woodwork, dm.offsides,
        dm.penalties_total, dm.penalties_goals,
        dm.free_kicks_total, dm.free_kicks_goals,
        dm.headers_total, dm.headers_goals,
        dm.fast_breaks_total, dm.fast_breaks_goals,
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
        ROUND(a.goals::NUMERIC              / a.played, 2),
        ROUND(a.shots::NUMERIC              / a.played, 2),
        ROUND(a.xg::NUMERIC                 / a.played, 2),
        ROUND(am.fast_breaks_total::NUMERIC / a.played, 2),
        ROUND(am.touches_in_box::NUMERIC    / a.played, 2),
        ROUND(dda.tackles::NUMERIC          / a.played, 2),
        ROUND(dda.interceptions::NUMERIC    / a.played, 2),
        ROUND(do2.goals::NUMERIC            / a.played, 2),
        ROUND(p.passes_total::NUMERIC       / a.played, 2),
        ROUND(p.crosses_total::NUMERIC      / a.played, 2),
        ROUND(p.through_balls::NUMERIC      / a.played, 2),
        ROUND(pr.pressed_seqs::NUMERIC      / a.played, 2),
        ROUND(s.buildups_total::NUMERIC          / a.played, 2),
        ROUND(s.direct_attacks_total::NUMERIC    / a.played, 2),
        ROUND(m.fouls::NUMERIC   / a.played, 2),
        ROUND(m.yellows::NUMERIC / a.played, 2)
    FROM silver.teams_attacking_overall            a
    JOIN silver.teams_attacking_non_penalty         anp ON anp.club = a.club
    JOIN silver.teams_attacking_set_pieces          asp ON asp.club = a.club
    JOIN silver.teams_attacking_misc                am  ON am.club  = a.club
    JOIN silver.teams_defending_defensive_action    dda ON dda.club = a.club
    JOIN silver.teams_defending_overall             do2 ON do2.club = a.club
    JOIN silver.teams_defending_set_piece           dsp ON dsp.club = a.club
    JOIN silver.teams_defending_misc                dm  ON dm.club  = a.club
    JOIN silver.teams_passing                       p   ON p.club   = a.club
    JOIN silver.teams_pressing                      pr  ON pr.club  = a.club
    JOIN silver.teams_sequences                     s   ON s.club   = a.club
    JOIN silver.teams_misc                          m   ON m.club   = a.club;

    RAISE NOTICE 'gold.teams_statistics loaded (12 silver tables joined)';
END;
$$;


-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-- PROCEDURE — gold.teams_ml_features (52 ML features)
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-- Subset 52 kolom untuk ML Clustering.
-- JOIN langsung dari silver layer (bukan dari OBT).
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CREATE OR REPLACE PROCEDURE gold.load_teams_ml_features()
LANGUAGE plpgsql
AS $$
BEGIN
    TRUNCATE TABLE gold.teams_ml_features;

    INSERT INTO gold.teams_ml_features (
        club,
        -- attacking overall (7)
        att_goals, att_xg, att_goals_vs_xg,
        att_shots, att_sot, att_conversion_pct, att_xg_per_shot,
        -- attacking non-penalty (3)
        att_np_goals, att_np_xg, att_np_goals_vs_xg,
        -- attacking set-pieces (4)
        att_sp_goals, att_sp_xg, att_sp_goal_pct, att_sp_shot_pct,
        -- attacking misc (3)
        att_touches_in_box, att_fast_breaks_total, att_fast_breaks_goals,
        -- defending action (6)
        def_tackles, def_interceptions, def_possession_won,
        def_blocks, def_clearances, def_avg_possession_pct,
        -- defending overall (5)
        def_goals_conceded, def_xg_against, def_goals_vs_xg_against,
        def_shots_against, def_shots_in_box_pct,
        -- passing (6)
        pas_passes_total, pas_passes_successful, pas_passes_pct,
        pas_final_third_pct, pas_direction_fwd_pct, pas_through_balls,
        -- pressing (6)
        prs_ppda, prs_pressed_seqs, prs_high_turnovers_total,
        prs_high_turnovers_shot_ending, prs_high_turnovers_goal_ending,
        prs_high_turnovers_shot_pct,
        -- sequences (6)
        seq_direct_speed, seq_passes_per_seq, seq_sequence_time,
        seq_buildups_total, seq_direct_attacks_total, seq_direct_attacks_goals,
        -- misc / discipline (6)
        msc_fouls, msc_yellows, msc_reds,
        msc_errors_lead_to_shot, msc_errors_lead_to_goal, msc_pens_conceded
    )
    SELECT
        a.club,
        -- attacking overall
        a.goals, a.xg, a.goals_vs_xg,
        a.shots, a.sot, a.conversion_pct, a.xg_per_shot,
        -- attacking non-penalty
        anp.goals, anp.xg, anp.goals_vs_xg,
        -- attacking set-pieces
        asp.goals, asp.xg, asp.goal_pct, asp.shot_pct,
        -- attacking misc
        am.touches_in_box, am.fast_breaks_total, am.fast_breaks_goals,
        -- defending action
        dda.tackles, dda.interceptions, dda.possession_won,
        dda.blocks, dda.clearances, dda.avg_possession_pct,
        -- defending overall
        do2.goals, do2.xg, do2.goals_vs_xg,
        do2.shots, do2.shots_in_box_pct,
        -- passing
        p.passes_total, p.passes_successful, p.passes_pct,
        p.final_third_pct, p.direction_fwd_pct, p.through_balls,
        -- pressing
        pr.ppda, pr.pressed_seqs, pr.high_turnovers_total,
        pr.high_turnovers_shot_ending, pr.high_turnovers_goal_ending, pr.high_turnovers_shot_pct,
        -- sequences
        s.direct_speed, s.passes_per_seq, s.sequence_time,
        s.buildups_total, s.direct_attacks_total, s.direct_attacks_goals,
        -- misc / discipline
        m.fouls, m.yellows, m.reds,
        m.errors_lead_to_shot, m.errors_lead_to_goal, m.pens_conceded
    FROM silver.teams_attacking_overall            a
    JOIN silver.teams_attacking_non_penalty         anp ON anp.club = a.club
    JOIN silver.teams_attacking_set_pieces          asp ON asp.club = a.club
    JOIN silver.teams_attacking_misc                am  ON am.club  = a.club
    JOIN silver.teams_defending_defensive_action    dda ON dda.club = a.club
    JOIN silver.teams_defending_overall             do2 ON do2.club = a.club
    JOIN silver.teams_passing                       p   ON p.club   = a.club
    JOIN silver.teams_pressing                      pr  ON pr.club  = a.club
    JOIN silver.teams_sequences                     s   ON s.club   = a.club
    JOIN silver.teams_misc                          m   ON m.club   = a.club;

    RAISE NOTICE 'gold.teams_ml_features loaded (10 silver tables joined, 52 features)';
END;
$$;


-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-- REFERENSI DBEAVER — Statement manual (opsional, untuk test/debug)
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-- TRUNCATE TABLE gold.teams_statistics;
--
-- INSERT INTO gold.teams_statistics (...)
-- SELECT ... FROM silver.teams_attacking_overall a
-- JOIN silver.teams_attacking_non_penalty   anp ON anp.club = a.club
-- JOIN silver.teams_attacking_set_pieces    asp ON asp.club = a.club
-- JOIN silver.teams_attacking_misc          am  ON am.club  = a.club
-- JOIN silver.teams_defending_defensive_action dda ON dda.club = a.club
-- JOIN silver.teams_defending_overall       do2 ON do2.club = a.club
-- JOIN silver.teams_defending_set_piece     dsp ON dsp.club = a.club
-- JOIN silver.teams_defending_misc          dm  ON dm.club  = a.club
-- JOIN silver.teams_passing                 p   ON p.club   = a.club
-- JOIN silver.teams_pressing               pr  ON pr.club  = a.club
-- JOIN silver.teams_sequences              s   ON s.club   = a.club
-- JOIN silver.teams_misc                   m   ON m.club   = a.club;
--
-- Atau cukup panggil:
-- CALL gold.load_teams_gold();
-- CALL gold.load_teams_ml_features();

