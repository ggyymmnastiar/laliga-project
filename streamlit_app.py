"""
La Liga Dashboard — Playing Style Analysis & K-Means Clustering
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import joblib
from pathlib import Path
from sklearn.decomposition import PCA

# ────────────────────────────────────────────────────────────
# CONFIG
# ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="La Liga Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    #MainMenu, footer {visibility: hidden;}
    .block-container {padding-top: 1.5rem;}

    .kpi-card {
        background: linear-gradient(135deg, #EEF2F7 0%, #DFE6EE 100%);
        border: 1px solid rgba(0,0,0,0.06);
        border-radius: 14px;
        padding: 22px 20px;
        text-align: center;
    }
    .kpi-value {font-size: 30px; font-weight: 700; color: #1A1F2B;}
    .kpi-label {font-size: 12px; color: #6B7280; text-transform: uppercase;
                letter-spacing: 1px; margin-top: 4px;}

    .cluster-badge {
        display: inline-block;
        padding: 6px 18px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 15px;
        color: #FAFAFA;
    }

    .cluster-card {
        background: linear-gradient(135deg, #1A1F2B 0%, #252B3B 100%);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 8px;
    }
    .cluster-card-title {font-weight: 700; font-size: 15px; margin-bottom: 8px;}
    .cluster-card-clubs {font-size: 13px; color: #B0B5C3; line-height: 1.8;}
</style>
""", unsafe_allow_html=True)


# ────────────────────────────────────────────────────────────
# CONSTANTS
# ────────────────────────────────────────────────────────────
BASE = Path(__file__).parent

SCORE_COLS = [
    "possession_score", "attacking_efficiency_score", "direct_play_score",
    "pressing_score", "defensive_solidity_score", "chance_creation_score",
    "build_up_score", "set_piece_score", "counter_attack_score",
]

SCORE_LABELS = {
    "possession_score": "Possession",
    "attacking_efficiency_score": "Attacking Efficiency",
    "direct_play_score": "Direct Play",
    "pressing_score": "Pressing",
    "defensive_solidity_score": "Defensive Solidity",
    "chance_creation_score": "Chance Creation",
    "build_up_score": "Build-up",
    "set_piece_score": "Set Piece",
    "counter_attack_score": "Counter Attack",
}

CLUSTER_COLORS = ["#E24A33", "#4C72B0", "#55A868", "#8172B2", "#C44E52", "#CCB974"]

POLAR_LAYOUT = dict(
    template=None,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#262730", size=12),
)

CHART_LAYOUT = dict(
    template=None,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#262730", size=12),
)


# ────────────────────────────────────────────────────────────
# DATA LOADING
# ────────────────────────────────────────────────────────────
@st.cache_data
def load_scores():
    return pd.read_csv(BASE / "data" / "gold" / "teams" / "teams_style_scores.csv")

@st.cache_data
def load_stats():
    return pd.read_csv(BASE / "data" / "gold" / "teams" / "teams_statistics.csv")

@st.cache_data
def load_clustering(k):
    return pd.read_csv(BASE / "data" / "clustering_results" / f"clustering_k{k}.csv")

@st.cache_data
def load_scaler():
    return joblib.load(BASE / "data" / "models" / "scaler.pkl")


scores = load_scores()
stats = load_stats()
scaler = load_scaler()


# ────────────────────────────────────────────────────────────
# SIDEBAR
# ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## La Liga")
    st.markdown("## Dashboard Analysis")
    st.markdown("## Season 2025-2026")
    st.markdown("---")

    page = st.radio(
        "Menu",
        ["Cluster Analysis", "Team Playing Style", "Playing Style Comparison"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    selected_k = st.selectbox("Number of Cluster (K)", [2, 3, 4, 5], index=2)
    # st.caption(f"Menggunakan K-Means dengan K={selected_k}")

clustered = load_clustering(selected_k)


# ────────────────────────────────────────────────────────────
# HELPER
# ────────────────────────────────────────────────────────────
def kpi_card(value, label):
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
    </div>""", unsafe_allow_html=True)


# ================================================================
#  OVERVIEW
# ================================================================
# if page == "Overview":
#     st.title("Overview")
#     st.caption(f"K-Means Clustering dengan K={selected_k}")

#     # KPI
#     cluster_counts = clustered["cluster"].value_counts().sort_index()

#     cols = st.columns(3)
#     with cols[0]:
#         kpi_card(len(clustered), "Jumlah Klub")
#     with cols[1]:
#         kpi_card(selected_k, "K (Cluster)")
#     with cols[2]:
#         kpi_card(selected_k, "Jumlah Cluster")

#     st.markdown("---")

#     # ── Anggota Cluster + Distribusi side by side ──
#     col_member, col_dist = st.columns([3, 2])

#     with col_member:
#         st.subheader("Anggota Cluster")

#         member_subcols = st.columns(selected_k)
#         for i, subcol in enumerate(member_subcols):
#             with subcol:
#                 color = CLUSTER_COLORS[i % len(CLUSTER_COLORS)]
#                 clubs_in = clustered[clustered["cluster"] == i]["club"].sort_values().tolist()
#                 st.markdown(
#                     f'<span class="cluster-badge" style="background:{color};">'
#                     f'Cluster {i}</span>',
#                     unsafe_allow_html=True,
#                 )
#                 st.caption(f"{len(clubs_in)} klub")
#                 for c in clubs_in:
#                     st.write(c)

#     with col_dist:
#         st.subheader("Distribusi Cluster")

#         fig_dist = go.Figure(go.Bar(
#             x=[f"Cluster {i}" for i in cluster_counts.index],
#             y=cluster_counts.values,
#             marker=dict(
#                 color=[CLUSTER_COLORS[i % len(CLUSTER_COLORS)] for i in cluster_counts.index],
#             ),
#             text=[f"{v} klub" for v in cluster_counts.values],
#             textposition="outside",
#             textfont=dict(size=13, color="#262730"),
#             hovertemplate="<b>%{x}</b><br>%{text}<extra></extra>",
#         ))

#         fig_dist.update_layout(
#             **CHART_LAYOUT,
#             margin=dict(l=50, r=20, t=20, b=20),
#             height=400,
#             yaxis=dict(
#                 title="Jumlah Klub",
#                 gridcolor="rgba(0,0,0,0.08)",
#                 range=[0, cluster_counts.max() + 3],
#                 dtick=1,
#             ),
#             xaxis=dict(tickfont=dict(size=12)),
#         )
#         st.plotly_chart(fig_dist, use_container_width=True)

#     st.markdown("---")

# ================================================================
#  TEAM PLAYING PROFILE
# ================================================================
if page == "Team Playing Style":
    st.title("Team Playing Style")

    club = st.selectbox("Select Club : ", sorted(scores["club"].unique()))

    sc = scores[scores["club"] == club].iloc[0]
    cl = clustered[clustered["club"] == club].iloc[0]
    cluster_id = int(cl["cluster"])
    color = CLUSTER_COLORS[cluster_id % len(CLUSTER_COLORS)]

    st.markdown(
        f'### {club} &nbsp; '
        f'<span class="cluster-badge" style="background:{color};">'
        f'Cluster {cluster_id}</span>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # Radar chart + Score ranking
    col_radar, col_score = st.columns([3, 2])

    with col_radar:
        st.subheader("Playing Style Chart")

        labels = [SCORE_LABELS[c] for c in SCORE_COLS]
        vals = [sc[c] for c in SCORE_COLS]

        labels_c = labels + [labels[0]]
        vals_c = vals + [vals[0]]

        fig_radar = go.Figure()

        fig_radar.add_trace(go.Scatterpolar(
            r=vals_c, theta=labels_c,
            fill="toself",
            fillcolor="rgba(226,74,51,0.18)",
            line=dict(color="#E24A33", width=2.5),
            marker=dict(size=7, color="#E24A33",
                        line=dict(width=1, color="white")),
            hovertemplate="%{theta}: %{r:.1f}<extra></extra>",
        ))

        fig_radar.update_layout(
            **POLAR_LAYOUT,
            margin=dict(l=60, r=60, t=30, b=30),
            height=480,
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                gridshape="circular",
                radialaxis=dict(
                    range=[0, 100],
                    tickvals=[20, 40, 60, 80, 100],
                    ticktext=["20", "40", "60", "80", "100"],
                    showticklabels=True,
                    showgrid=True,
                    tickfont=dict(size=9, color="#9CA3AF"),
                    gridcolor="rgba(0,0,0,0.12)",
                    gridwidth=1,
                    showline=False,
                ),
                angularaxis=dict(
                    showgrid=True,
                    gridcolor="rgba(0,0,0,0.12)",
                    gridwidth=1,
                    tickfont=dict(size=11, color="#262730"),
                    linecolor="rgba(0,0,0,0.12)",
                ),
            ),
            showlegend=False,
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with col_score:
        st.subheader("Playing Style Score")

        style_ranked = sorted(
            [(SCORE_LABELS[c], sc[c]) for c in SCORE_COLS],
            key=lambda x: x[1], reverse=True,
        )

        for i, (name, val) in enumerate(style_ranked, 1):
            st.markdown(f"**{i}. {name}** -- {val:.1f}")
            st.progress(val / 100)

    st.subheader("Overall Statistics")
    st.caption("Details for each statistics category")

    club_stats = stats[stats["club"] == club].iloc[0]

    # Categorize columns based on prefix
    categories = {
        "Attacking": [c for c in stats.columns if c.startswith("att_")],
        "Defending": [c for c in stats.columns if c.startswith("def_")],
        "Passing": [c for c in stats.columns if c.startswith("pas_")],
        "Pressing": [c for c in stats.columns if c.startswith("prs_")],
        "Sequences": [c for c in stats.columns if c.startswith("seq_")],
        "Misc": [c for c in stats.columns if c.startswith("msc_")]
    }

    for cat_name, cols in categories.items():
        with st.expander(cat_name):
            cat_df = pd.DataFrame({
                "Metric": cols,
                "Value": [club_stats[c] for c in cols]
            })
            st.dataframe(cat_df, use_container_width=True, hide_index=True)


# ================================================================
#  CLUSTER ANALYSIS
# ================================================================
elif page == "Cluster Analysis":
    st.title("Cluster Analysis")
    # st.caption(f"K-Means Clustering dengan K={selected_k}")

    # Merge scores + cluster labels
    merged = scores.merge(clustered, on="club")
    cluster_means = merged.groupby("cluster")[SCORE_COLS].mean()
    cluster_counts = clustered["cluster"].value_counts().sort_index()

    # ── KPI: jumlah klub per cluster ──
    kpi_cols = st.columns(selected_k)
    for i, col in enumerate(kpi_cols):
        with col:
            color = CLUSTER_COLORS[i % len(CLUSTER_COLORS)]
            count = cluster_counts.get(i, 0)
            st.markdown(
                f'<div class="kpi-card">'
                f'<div class="kpi-value" style="color:{color};">{count}</div>'
                f'<div class="kpi-label">Cluster {i}</div>'
                f'</div>', unsafe_allow_html=True,
            )

    st.markdown("---")

    # ── Anggota Cluster + Distribusi side by side ──
    col_member, col_dist = st.columns([3, 2])

    with col_member:
        st.subheader("Cluster Member")

        member_subcols = st.columns(selected_k)
        for i, subcol in enumerate(member_subcols):
            with subcol:
                color = CLUSTER_COLORS[i % len(CLUSTER_COLORS)]
                clubs_in = clustered[clustered["cluster"] == i]["club"].sort_values().tolist()
                st.markdown(
                    f'<span class="cluster-badge" style="background:{color};">'
                    f'Cluster {i}</span>',
                    unsafe_allow_html=True,
                )
                st.caption(f"{len(clubs_in)} club")
                for c in clubs_in:
                    st.write(c)

    with col_dist:
        st.subheader("Cluster Distribution")

        fig_dist = go.Figure(go.Bar(
            x=[f"Cluster {i}" for i in cluster_counts.index],
            y=cluster_counts.values,
            marker=dict(
                color=[CLUSTER_COLORS[i % len(CLUSTER_COLORS)] for i in cluster_counts.index],
            ),
            text=[f"{v} club" for v in cluster_counts.values],
            textposition="outside",
            textfont=dict(size=13, color="#262730"),
            hovertemplate="<b>%{x}</b><br>%{text}<extra></extra>",
        ))

        fig_dist.update_layout(
            **CHART_LAYOUT,
            margin=dict(l=50, r=20, t=20, b=20),
            height=400,
            yaxis=dict(
                title="Number of Club",
                gridcolor="rgba(0,0,0,0.08)",
                range=[0, cluster_counts.max() + 3],
                dtick=1,
            ),
            xaxis=dict(tickfont=dict(size=12)),
        )
        st.plotly_chart(fig_dist, use_container_width=True)

    st.markdown("---")

    # ── PCA Scatter Plot (full width) ──
    st.subheader("Cluster Visualization (PCA)")

    X = scores[SCORE_COLS]
    X_scaled = scaler.transform(X)

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    pca_df = pd.DataFrame({
        "PC1": X_pca[:, 0],
        "PC2": X_pca[:, 1],
        "club": scores["club"],
        "cluster": clustered["cluster"],
    })

    fig_pca = go.Figure()

    for cid in sorted(pca_df["cluster"].unique()):
        mask = pca_df["cluster"] == cid
        subset = pca_df[mask]
        color = CLUSTER_COLORS[cid % len(CLUSTER_COLORS)]

        fig_pca.add_trace(go.Scatter(
            x=subset["PC1"], y=subset["PC2"],
            mode="markers+text",
            marker=dict(size=11, color=color,
                        line=dict(width=1, color="white")),
            text=subset["club"],
            textposition="top center",
            textfont=dict(size=10, color="#6B7280"),
            name=f"Cluster {cid}",
            hovertemplate="<b>%{text}</b><br>PC1: %{x:.2f}<br>PC2: %{y:.2f}<extra></extra>",
        ))

    var_explained = pca.explained_variance_ratio_
    fig_pca.update_layout(
        **CHART_LAYOUT,
        margin=dict(l=60, r=40, t=20, b=60),
        height=500,
        xaxis=dict(
            title=f"PC1 ({var_explained[0]:.1%} variance)",
            gridcolor="rgba(0,0,0,0.08)",
            zeroline=False,
        ),
        yaxis=dict(
            title=f"PC2 ({var_explained[1]:.1%} variance)",
            gridcolor="rgba(0,0,0,0.08)",
            zeroline=False,
        ),
        legend=dict(
            orientation="h", yanchor="top", y=-0.22,
            xanchor="center", x=0.5,
        ),
    )
    st.plotly_chart(fig_pca, use_container_width=True)

    st.markdown("---")

    # ── Heatmap: rata-rata style scores per cluster ──
    st.subheader("Cluster Playing Style")
    st.caption("Playing Style (Avg) per Cluster")

    heatmap_labels = [SCORE_LABELS[c] for c in SCORE_COLS]
    z_vals = cluster_means[SCORE_COLS].values
    y_labels = [f"Cluster {i}" for i in cluster_means.index]
    z_text = [[f"{v:.1f}" for v in row] for row in z_vals]

    fig_hm = go.Figure(go.Heatmap(
        z=z_vals,
        x=heatmap_labels,
        y=y_labels,
        text=z_text,
        texttemplate="%{text}",
        textfont=dict(size=13),
        colorscale="RdYlGn",
        hovertemplate="<b>%{y}</b><br>%{x}: %{z:.1f}<extra></extra>",
    ))

    fig_hm.update_layout(
        **CHART_LAYOUT,
        margin=dict(l=20, r=20, t=20, b=100),
        height=80 + selected_k * 80,
        xaxis=dict(tickangle=-45, tickfont=dict(size=11), side="bottom"),
        yaxis=dict(tickfont=dict(size=12), autorange="reversed"),
    )
    st.plotly_chart(fig_hm, use_container_width=True)

    st.markdown("---")

    # ── Detail per cluster ──
    st.subheader("Cluster Details")

    for cid in sorted(merged["cluster"].unique()):
        color = CLUSTER_COLORS[cid % len(CLUSTER_COLORS)]
        clubs_in = merged[merged["cluster"] == cid]["club"].sort_values().tolist()

        with st.expander(f"Cluster {cid} — {len(clubs_in)} club", expanded=(cid == 0)):
            col_list, col_radar = st.columns([1, 2])

            with col_list:
                st.markdown("**Member :**")
                for c in clubs_in:
                    st.write(c)

            with col_radar:
                st.markdown("**Playing Style Chart (Avg)**")
                means = cluster_means.loc[cid]
                labels = [SCORE_LABELS[c] for c in SCORE_COLS]
                vals = [means[c] for c in SCORE_COLS]
                labels_c = labels + [labels[0]]
                vals_c = vals + [vals[0]]

                fig_cr = go.Figure()
                fig_cr.add_trace(go.Scatterpolar(
                    r=vals_c, theta=labels_c,
                    fill="toself",
                    fillcolor=f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.12)",
                    line=dict(color=color, width=2.5),
                    marker=dict(size=6, color=color,
                                line=dict(width=1, color="white")),
                    hovertemplate="%{theta}: %{r:.1f}<extra></extra>",
                ))
                fig_cr.update_layout(
                    **POLAR_LAYOUT,
                    margin=dict(l=50, r=50, t=20, b=20),
                    height=380,
                    polar=dict(
                        bgcolor="rgba(0,0,0,0)",
                        gridshape="circular",
                        radialaxis=dict(
                            range=[0, 100],
                            tickvals=[20, 40, 60, 80, 100],
                            ticktext=["20", "40", "60", "80", "100"],
                            showticklabels=True, showgrid=True,
                            tickfont=dict(size=8, color="#9CA3AF"),
                            gridcolor="rgba(0,0,0,0.10)", gridwidth=1,
                            showline=False,
                        ),
                        angularaxis=dict(
                            showgrid=True, gridcolor="rgba(0,0,0,0.10)",
                            gridwidth=1, tickfont=dict(size=10, color="#262730"),
                            linecolor="rgba(0,0,0,0.10)",
                        ),
                    ),
                    showlegend=False,
                )
                st.plotly_chart(fig_cr, use_container_width=True)

# ================================================================
#  STYLE COMPARISON
# ================================================================
elif page == "Playing Style Comparison":
    st.title("Playing Style Comparison")

    comp_type = st.radio("Compare By : ", ["Clubs", "Clusters"], horizontal=True)

    if comp_type == "Clubs":
        items_list = sorted(scores["club"].unique())
        selected_items = st.multiselect(
            "Select Clubs : ",
            options=items_list,
            default=items_list[:2],
            max_selections=4
        )
    else:
        items_list = [f"Cluster {i}" for i in range(selected_k)]
        selected_items = st.multiselect(
            "Select Clusters (2-4)",
            options=items_list,
            default=items_list[:2] if len(items_list) >= 2 else items_list,
            max_selections=4
        )

    if len(selected_items) < 2:
        st.warning("Select at least 2 items for comparison")
    else:
        st.markdown("---")
        
        if comp_type == "Clubs":
            comp_scores = scores[scores["club"].isin(selected_items)].set_index("club")
        else:
            merged = scores.merge(clustered, on="club")
            cluster_means = merged.groupby("cluster")[SCORE_COLS].mean()
            cluster_means.index = [f"Cluster {i}" for i in cluster_means.index]
            comp_scores = cluster_means.loc[selected_items]

        col_radar, col_table = st.columns([3, 2])

        with col_radar:
            st.subheader("Comparison Chart")
            
            fig_comp = go.Figure()

            labels = [SCORE_LABELS[c] for c in SCORE_COLS]
            labels_c = labels + [labels[0]]

            for i, item in enumerate(selected_items):
                if comp_type == "Clubs":
                    color = CLUSTER_COLORS[i % len(CLUSTER_COLORS)]
                else:
                    cid = int(item.split()[-1])
                    color = CLUSTER_COLORS[cid % len(CLUSTER_COLORS)]
                    
                sc = comp_scores.loc[item]
                vals = [sc[c] for c in SCORE_COLS]
                vals_c = vals + [vals[0]]

                fig_comp.add_trace(go.Scatterpolar(
                    r=vals_c, theta=labels_c,
                    fill="toself",
                    fillcolor=f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.12)",
                    line=dict(color=color, width=2.5),
                    marker=dict(size=6, color=color,
                                line=dict(width=1, color="white")),
                    name=item,
                    hovertemplate="%{theta}: %{r:.1f}<extra></extra>",
                ))

            fig_comp.update_layout(
                **POLAR_LAYOUT,
                margin=dict(l=60, r=60, t=30, b=30),
                height=480,
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    gridshape="circular",
                    radialaxis=dict(
                        range=[0, 100],
                        tickvals=[20, 40, 60, 80, 100],
                        ticktext=["20", "40", "60", "80", "100"],
                        showticklabels=True,
                        showgrid=True,
                        tickfont=dict(size=9, color="#9CA3AF"),
                        gridcolor="rgba(0,0,0,0.12)",
                        gridwidth=1,
                        showline=False,
                    ),
                    angularaxis=dict(
                        showgrid=True,
                        gridcolor="rgba(0,0,0,0.12)",
                        gridwidth=1,
                        tickfont=dict(size=11, color="#262730"),
                        linecolor="rgba(0,0,0,0.12)",
                    ),
                ),
                showlegend=True,
                legend=dict(
                    orientation="h", yanchor="top", y=-0.1,
                    xanchor="center", x=0.5
                )
            )
            st.plotly_chart(fig_comp, use_container_width=True)

        with col_table:
            st.subheader("Comparison Table")

            comp_table = comp_scores[SCORE_COLS].T
            comp_table.index = [SCORE_LABELS[c] for c in SCORE_COLS]

            st.dataframe(comp_table.style.format("{:.1f}"), use_container_width=True)
