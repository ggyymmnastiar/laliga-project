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
    st.caption("Playing Style Analysis")
    st.markdown("---")

    page = st.radio(
        "Menu",
        ["Overview", "Team Profile"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    selected_k = st.selectbox("Jumlah Cluster (K)", [2, 3, 4, 5], index=2)
    st.caption(f"Menggunakan K-Means dengan K={selected_k}")

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
if page == "Overview":
    st.title("Overview")
    st.caption(f"K-Means Clustering dengan K={selected_k}")

    # KPI
    cluster_counts = clustered["cluster"].value_counts().sort_index()

    cols = st.columns(3)
    with cols[0]:
        kpi_card(len(clustered), "Jumlah Klub")
    with cols[1]:
        kpi_card(selected_k, "K (Cluster)")
    with cols[2]:
        kpi_card(selected_k, "Jumlah Cluster")

    st.markdown("---")

    # ── Anggota Cluster + Distribusi side by side ──
    col_member, col_dist = st.columns([3, 2])

    with col_member:
        st.subheader("Anggota Cluster")

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
                st.caption(f"{len(clubs_in)} klub")
                for c in clubs_in:
                    st.write(c)

    with col_dist:
        st.subheader("Distribusi Cluster")

        fig_dist = go.Figure(go.Bar(
            x=[f"Cluster {i}" for i in cluster_counts.index],
            y=cluster_counts.values,
            marker=dict(
                color=[CLUSTER_COLORS[i % len(CLUSTER_COLORS)] for i in cluster_counts.index],
            ),
            text=[f"{v} klub" for v in cluster_counts.values],
            textposition="outside",
            textfont=dict(size=13, color="#262730"),
            hovertemplate="<b>%{x}</b><br>%{text}<extra></extra>",
        ))

        fig_dist.update_layout(
            **CHART_LAYOUT,
            margin=dict(l=50, r=20, t=20, b=20),
            height=400,
            yaxis=dict(
                title="Jumlah Klub",
                gridcolor="rgba(0,0,0,0.08)",
                range=[0, cluster_counts.max() + 3],
                dtick=1,
            ),
            xaxis=dict(tickfont=dict(size=12)),
        )
        st.plotly_chart(fig_dist, use_container_width=True)

    st.markdown("---")

    # ── PCA Scatter Plot (full width) ──
    st.subheader("Visualisasi Cluster (PCA)")

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


# ================================================================
#  TEAM PROFILE
# ================================================================
elif page == "Team Profile":
    st.title("Team Profile")

    club = st.selectbox("Pilih Klub", sorted(scores["club"].unique()))

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
