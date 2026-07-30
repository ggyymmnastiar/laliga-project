-- ===========================================================================
-- Gold Layer — Load Players (One Big Table)
-- ===========================================================================
-- Memuat data dari Silver ke Gold:
--   1. gold.player_statistics     ← JOIN 4 tabel outfield silver
--   2. gold.goalkeeper_statistics ← silver.players_goalkeeping
--
-- CARA PAKAI:
--   Opsi 1: Jalankan statement satu per satu di DBeaver.
--   Opsi 2: CALL gold.load_players_gold();
-- ===========================================================================


-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-- BAGIAN 1 — Statement langsung (bisa dijalankan satu per satu di DBeaver)
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-- 1) GOLD.PLAYER_STATISTICS (outfield — 4 tabel di-LEFT JOIN)
TRUNCATE TABLE gold.player_statistics;

INSERT INTO gold.player_statistics (
    player_name, club, apps, mins,
    -- attacking
    att_goals, att_xg, att_goals_vs_xg, att_shots, att_sot, att_conv_pct, att_xg_per_shot,
    -- defending
    def_tackles, def_interceptions, def_possession_won, def_blocks, def_clearances,
    def_ground_duels_total, def_ground_duels_won, def_ground_duels_pct,
    def_aerial_duels_total, def_aerial_duels_won, def_aerial_duels_pct,
    -- passing
    pas_open_play_total, pas_open_play_successful, pas_open_play_pct,
    pas_final_third_total, pas_final_third_successful, pas_final_third_pct,
    pas_crosses_total, pas_crosses_successful, pas_crosses_pct, pas_through_balls,
    -- carrying
    car_carries_total, car_carries_distance, car_carries_avg,
    car_progressive_total, car_progressive_distance, car_progressive_avg,
    car_ended_with_shot, car_ended_with_goal, car_ended_with_chance, car_ended_with_assist
)
SELECT
    a.name,
    a.club,
    a.apps,
    a.mins,
    -- attacking
    a.goals, a.xg, a.goals_vs_xg, a.shots, a.sot, a.conv_pct, a.xg_per_shot,
    -- defending
    df.tackles, df.interceptions, df.possession_won, df.blocks, df.clearances,
    df.ground_duels_total, df.ground_duels_won, df.ground_duels_pct,
    df.aerial_duels_total, df.aerial_duels_won, df.aerial_duels_pct,
    -- passing
    p.open_play_total, p.open_play_successful, p.open_play_pct,
    p.final_third_total, p.final_third_successful, p.final_third_pct,
    p.crosses_total, p.crosses_successful, p.crosses_pct, p.through_balls,
    -- carrying
    c.carries_total, c.carries_distance, c.carries_avg,
    c.progressive_total, c.progressive_distance, c.progressive_avg,
    c.ended_with_shot, c.ended_with_goal, c.ended_with_chance, c.ended_with_assist
FROM silver.players_attacking a
LEFT JOIN silver.players_defending df ON df.name = a.name AND df.club = a.club
LEFT JOIN silver.players_passing   p  ON p.name  = a.name AND p.club  = a.club
LEFT JOIN silver.players_carrying  c  ON c.name  = a.name AND c.club  = a.club;

-- 2) GOLD.GOALKEEPER_STATISTICS
TRUNCATE TABLE gold.goalkeeper_statistics;

INSERT INTO gold.goalkeeper_statistics (
    player_name, club, apps, mins,
    gk_goals_conceded, gk_saves_made, gk_save_percentage,
    gk_xgot_conceded, gk_goals_prevented, gk_gp_rate
)
SELECT
    gk.name,
    gk.club,
    gk.apps,
    gk.mins,
    gk.goals_conceded,
    gk.saves_made,
    gk.save_percentage,
    gk.xgot_conceded,
    gk.goals_prevented,
    gk.gp_rate
FROM silver.players_goalkeeping gk;


-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-- BAGIAN 2 — Procedure (membungkus semua statement di atas)
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CREATE OR REPLACE PROCEDURE gold.load_players_gold()
LANGUAGE plpgsql
AS $$
BEGIN
    -- 1) Player statistics (outfield)
    TRUNCATE TABLE gold.player_statistics;

    INSERT INTO gold.player_statistics (
        player_name, club, apps, mins,
        att_goals, att_xg, att_goals_vs_xg, att_shots, att_sot, att_conv_pct, att_xg_per_shot,
        def_tackles, def_interceptions, def_possession_won, def_blocks, def_clearances,
        def_ground_duels_total, def_ground_duels_won, def_ground_duels_pct,
        def_aerial_duels_total, def_aerial_duels_won, def_aerial_duels_pct,
        pas_open_play_total, pas_open_play_successful, pas_open_play_pct,
        pas_final_third_total, pas_final_third_successful, pas_final_third_pct,
        pas_crosses_total, pas_crosses_successful, pas_crosses_pct, pas_through_balls,
        car_carries_total, car_carries_distance, car_carries_avg,
        car_progressive_total, car_progressive_distance, car_progressive_avg,
        car_ended_with_shot, car_ended_with_goal, car_ended_with_chance, car_ended_with_assist
    )
    SELECT
        a.name, a.club, a.apps, a.mins,
        a.goals, a.xg, a.goals_vs_xg, a.shots, a.sot, a.conv_pct, a.xg_per_shot,
        df.tackles, df.interceptions, df.possession_won, df.blocks, df.clearances,
        df.ground_duels_total, df.ground_duels_won, df.ground_duels_pct,
        df.aerial_duels_total, df.aerial_duels_won, df.aerial_duels_pct,
        p.open_play_total, p.open_play_successful, p.open_play_pct,
        p.final_third_total, p.final_third_successful, p.final_third_pct,
        p.crosses_total, p.crosses_successful, p.crosses_pct, p.through_balls,
        c.carries_total, c.carries_distance, c.carries_avg,
        c.progressive_total, c.progressive_distance, c.progressive_avg,
        c.ended_with_shot, c.ended_with_goal, c.ended_with_chance, c.ended_with_assist
    FROM silver.players_attacking a
    LEFT JOIN silver.players_defending df ON df.name = a.name AND df.club = a.club
    LEFT JOIN silver.players_passing   p  ON p.name  = a.name AND p.club  = a.club
    LEFT JOIN silver.players_carrying  c  ON c.name  = a.name AND c.club  = a.club;

    RAISE NOTICE 'gold.player_statistics loaded';

    -- 2) Goalkeeper statistics
    TRUNCATE TABLE gold.goalkeeper_statistics;

    INSERT INTO gold.goalkeeper_statistics (
        player_name, club, apps, mins,
        gk_goals_conceded, gk_saves_made, gk_save_percentage,
        gk_xgot_conceded, gk_goals_prevented, gk_gp_rate
    )
    SELECT
        gk.name, gk.club, gk.apps, gk.mins,
        gk.goals_conceded, gk.saves_made, gk.save_percentage,
        gk.xgot_conceded, gk.goals_prevented, gk.gp_rate
    FROM silver.players_goalkeeping gk;

    RAISE NOTICE 'gold.goalkeeper_statistics loaded';
    RAISE NOTICE 'Gold players load complete';
END;
$$;
