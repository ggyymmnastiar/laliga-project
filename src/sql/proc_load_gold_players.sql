-- ===========================================================================
-- Gold Layer — Load Players (Star Schema)
-- ===========================================================================
-- Memuat data dari Silver ke Gold:
--   1. gold.dim_player                ← DISTINCT (name, club) dari silver
--   2. gold.fact_player_statistics    ← JOIN 4 tabel outfield silver
--   3. gold.fact_goalkeeper_statistics ← silver.players_goalkeeping
--
-- CARA PAKAI:
--   Opsi 1: Jalankan statement satu per satu di DBeaver.
--   Opsi 2: CALL gold.load_players_gold();
--
-- CATATAN: dim_team harus sudah terisi sebelum menjalankan script ini.
-- ===========================================================================


-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-- BAGIAN 1 — Statement langsung (bisa dijalankan satu per satu di DBeaver)
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-- 1) Truncate (fact dulu karena FK)
TRUNCATE TABLE gold.fact_player_statistics;
TRUNCATE TABLE gold.fact_goalkeeper_statistics;
TRUNCATE TABLE gold.dim_player CASCADE;

-- 2) GOLD.DIM_PLAYER — dari semua pemain (outfield + GK)
INSERT INTO gold.dim_player (player_name, team_id)
SELECT DISTINCT
    all_players.name,
    d.team_id
FROM (
    SELECT name, club FROM silver.players_attacking
    UNION
    SELECT name, club FROM silver.players_defending
    UNION
    SELECT name, club FROM silver.players_passing
    UNION
    SELECT name, club FROM silver.players_carrying
    UNION
    SELECT name, club FROM silver.players_goalkeeping
) all_players
JOIN gold.dim_team d ON d.club = all_players.club
ORDER BY d.team_id, all_players.name;

-- 3) GOLD.FACT_PLAYER_STATISTICS (outfield — 4 tabel di-LEFT JOIN)
INSERT INTO gold.fact_player_statistics (
    player_id, team_id, apps, mins,
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
    dp.player_id,
    dp.team_id,
    COALESCE(a.apps, df.apps, p.apps, c.apps),
    COALESCE(a.mins, df.mins, p.mins, c.mins),
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
FROM gold.dim_player dp
JOIN gold.dim_team dt ON dt.team_id = dp.team_id
LEFT JOIN silver.players_attacking a  ON a.name  = dp.player_name AND a.club  = dt.club
LEFT JOIN silver.players_defending df ON df.name = dp.player_name AND df.club = dt.club
LEFT JOIN silver.players_passing   p  ON p.name  = dp.player_name AND p.club  = dt.club
LEFT JOIN silver.players_carrying  c  ON c.name  = dp.player_name AND c.club  = dt.club
WHERE COALESCE(a.name, df.name, p.name, c.name) IS NOT NULL;

-- 4) GOLD.FACT_GOALKEEPER_STATISTICS
INSERT INTO gold.fact_goalkeeper_statistics (
    player_id, team_id, apps, mins,
    gk_goals_conceded, gk_saves_made, gk_save_percentage,
    gk_xgot_conceded, gk_goals_prevented, gk_gp_rate
)
SELECT
    dp.player_id,
    dp.team_id,
    gk.apps,
    gk.mins,
    gk.goals_conceded,
    gk.saves_made,
    gk.save_percentage,
    gk.xgot_conceded,
    gk.goals_prevented,
    gk.gp_rate
FROM gold.dim_player dp
JOIN gold.dim_team dt ON dt.team_id = dp.team_id
JOIN silver.players_goalkeeping gk ON gk.name = dp.player_name AND gk.club = dt.club;


-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-- BAGIAN 2 — Procedure (membungkus semua statement di atas)
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CREATE OR REPLACE PROCEDURE gold.load_players_gold()
LANGUAGE plpgsql
AS $$
BEGIN
    -- 1) Truncate
    TRUNCATE TABLE gold.fact_player_statistics;
    TRUNCATE TABLE gold.fact_goalkeeper_statistics;
    TRUNCATE TABLE gold.dim_player CASCADE;

    -- 2) Load dim_player
    INSERT INTO gold.dim_player (player_name, team_id)
    SELECT DISTINCT
        all_players.name,
        d.team_id
    FROM (
        SELECT name, club FROM silver.players_attacking
        UNION
        SELECT name, club FROM silver.players_defending
        UNION
        SELECT name, club FROM silver.players_passing
        UNION
        SELECT name, club FROM silver.players_carrying
        UNION
        SELECT name, club FROM silver.players_goalkeeping
    ) all_players
    JOIN gold.dim_team d ON d.club = all_players.club
    ORDER BY d.team_id, all_players.name;

    RAISE NOTICE 'gold.dim_player loaded';

    -- 3) Load fact_player_statistics (outfield)
    INSERT INTO gold.fact_player_statistics (
        player_id, team_id, apps, mins,
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
        dp.player_id,
        dp.team_id,
        COALESCE(a.apps, df.apps, p.apps, c.apps),
        COALESCE(a.mins, df.mins, p.mins, c.mins),
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
    FROM gold.dim_player dp
    JOIN gold.dim_team dt ON dt.team_id = dp.team_id
    LEFT JOIN silver.players_attacking a  ON a.name  = dp.player_name AND a.club  = dt.club
    LEFT JOIN silver.players_defending df ON df.name = dp.player_name AND df.club = dt.club
    LEFT JOIN silver.players_passing   p  ON p.name  = dp.player_name AND p.club  = dt.club
    LEFT JOIN silver.players_carrying  c  ON c.name  = dp.player_name AND c.club  = dt.club
    WHERE COALESCE(a.name, df.name, p.name, c.name) IS NOT NULL;

    RAISE NOTICE 'gold.fact_player_statistics loaded';

    -- 4) Load fact_goalkeeper_statistics
    INSERT INTO gold.fact_goalkeeper_statistics (
        player_id, team_id, apps, mins,
        gk_goals_conceded, gk_saves_made, gk_save_percentage,
        gk_xgot_conceded, gk_goals_prevented, gk_gp_rate
    )
    SELECT
        dp.player_id,
        dp.team_id,
        gk.apps, gk.mins,
        gk.goals_conceded, gk.saves_made, gk.save_percentage,
        gk.xgot_conceded, gk.goals_prevented, gk.gp_rate
    FROM gold.dim_player dp
    JOIN gold.dim_team dt ON dt.team_id = dp.team_id
    JOIN silver.players_goalkeeping gk ON gk.name = dp.player_name AND gk.club = dt.club;

    RAISE NOTICE 'gold.fact_goalkeeper_statistics loaded';
    RAISE NOTICE 'Gold players load complete';
END;
$$;
