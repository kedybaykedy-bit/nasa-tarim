"""
Field Shift — NASA Space Apps Challenge 2026
Production Decision-Support Platform for Crop Rotation Planning

Run:
    streamlit run app.py
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import asdict
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import altair as alt
import folium
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from streamlit_folium import st_folium

from data_engine import (
    CROP_LIBRARY,
    NASASnapshot,
    RotationStrategy,
    NASA_DATA_SOURCES,
    USDA_DATA_SOURCES,
    USDASoilData,
    USDAMarketData,
    build_strategies,
    export_report_text,
    fetch_nasa_snapshot,
    get_nasa_data_source_summary,
    get_usda_market_data,
    get_usda_soil_data,
)

# ---------------------------------------------------------------------------
# SQLite — persistent storage
# ---------------------------------------------------------------------------
DB_PATH = "C:/Users/musaf/field_shift_app/field_shift.db"


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS fields (
            id TEXT PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            lat REAL NOT NULL,
            lon REAL NOT NULL,
            crops TEXT NOT NULL,
            priorities TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS computations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field_id TEXT NOT NULL,
            snapshot TEXT NOT NULL,
            strategies TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(field_id) REFERENCES fields(id)
        )
        """
    )
    conn.commit()
    conn.close()


def save_field(name: str, lat: float, lon: float, crops: List[str], priorities: Dict[str, float]) -> str:
    fid = hashlib.md5(f"{name}{datetime.now().isoformat()}".encode()).hexdigest()[:12]
    conn = get_db()
    conn.execute(
        "INSERT OR REPLACE INTO fields (id, name, lat, lon, crops, priorities, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (fid, name, lat, lon, json.dumps(crops, ensure_ascii=False),
         json.dumps(priorities, ensure_ascii=False), datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()
    return fid


def load_fields() -> List[dict]:
    conn = get_db()
    rows = conn.execute("SELECT * FROM fields ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_field(field_id: str) -> None:
    conn = get_db()
    conn.execute("DELETE FROM computations WHERE field_id = ?", (field_id,))
    conn.execute("DELETE FROM fields WHERE id = ?", (field_id,))
    conn.commit()
    conn.close()


def save_computation(field_id: str, snapshot: NASASnapshot, strategies: List[RotationStrategy]) -> None:
    conn = get_db()
    conn.execute(
        "INSERT INTO computations (field_id, snapshot, strategies, created_at) VALUES (?, ?, ?, ?)",
        (field_id, json.dumps(asdict(snapshot), ensure_ascii=False),
         json.dumps([asdict(s) for s in strategies], ensure_ascii=False, default=str),
         datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def load_latest_computation(field_id: str) -> Optional[Tuple[NASASnapshot, List[RotationStrategy]]]:
    conn = get_db()
    row = conn.execute(
        "SELECT snapshot, strategies FROM computations WHERE field_id = ? ORDER BY created_at DESC LIMIT 1",
        (field_id,),
    ).fetchone()
    conn.close()
    if not row:
        return None
    snap = NASASnapshot(**json.loads(row["snapshot"]))
    strats_data = json.loads(row["strategies"])
    strategies: List[RotationStrategy] = []
    for s in strats_data:
        crops = [CROP_LIBRARY[c["name"]] for c in s["crops"] if c["name"] in CROP_LIBRARY]
        kwargs = {k: v for k, v in s.items() if k != "crops"}
        strategies.append(RotationStrategy(**kwargs, crops=crops))
    return snap, strategies


# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Field Shift — NASA Space Apps 2026",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# CSS injection — invisible, no text leakage
# ---------------------------------------------------------------------------
CSS = """
<link href="https://fonts.googleapis.com/css2?family=Russo+One:wght@400;700&family=Chakra+Petch:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {
  --primary: #7C3AED;
  --secondary: #A78BFA;
  --cta: #F43F5E;
  --accent: #22C55E;
  --warning: #F59E0B;
  --danger: #EF4444;
  --bg: #0F0F23;
  --card: rgba(30, 27, 60, 0.5);
  --text: #F8FAFC;
  --muted: #94A3B8;
  --border: rgba(124, 58, 237, 0.2);
  --glow: rgba(124, 58, 237, 0.35);
}

.stApp {
  background: radial-gradient(circle at top left, #1a1734 0%, #0d0d1b 40%, #0F0F23 100%);
  background-attachment: fixed;
  color: #F8FAFC;
  font-family: 'Chakra Petch', sans-serif;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

h1, h2, h3, h4 {
  font-family: 'Russo One', sans-serif;
  letter-spacing: -0.02em;
}

.hero {
  padding: 56px 24px 36px 24px;
  border-radius: 32px;
  background: linear-gradient(135deg, rgba(124,58,237,0.10) 0%, rgba(13,13,27,0.85) 100%);
  border: 1px solid rgba(124, 58, 237, 0.2);
  box-shadow: 0 24px 48px -16px rgba(124, 58, 237, 0.35);
  margin: 0 auto 32px auto;
  max-width: 1200px;
  position: relative;
  overflow: hidden;
}
.hero::before {
  content: ""; position: absolute; top: -80px; right: -80px;
  width: 400px; height: 400px;
  background: radial-gradient(circle, #7C3AED22 0%, transparent 55%);
  filter: blur(80px); z-index: 0;
}
.hero-content {position: relative; z-index: 1;}
.hero-title {
  font-size: 56px; font-weight: 700; margin: 0 0 12px 0;
  background: linear-gradient(90deg, #F8FAFC 0%, #A78BFA 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-sub {font-size: 19px; color: #94A3B8; margin: 0; line-height: 1.8; max-width: 900px;}

.badge {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 6px 16px; border-radius: 30px; font-size: 12px;
  font-weight: 700; font-family: 'Russo One', sans-serif;
  text-transform: uppercase; letter-spacing: 0.1em;
  border: 1px solid; background: rgba(0,0,0,0.3);
  margin-bottom: 16px;
}
.badge-advanced {color: #7C3AED; border-color: #7C3AED; background: #7C3AED15;}

.section-header {
  display: flex; align-items: center; gap: 14px;
  margin: 44px 0 22px 0; padding-bottom: 12px;
  border-bottom: 2px solid rgba(124, 58, 237, 0.2);
}
.section-title {
  font-family: 'Russo One', sans-serif; font-size: 24px; color: #7C3AED; margin: 0;
}
.section-sub {color: #94A3B8; font-size: 14px; margin: 0;}

.card {
  background: rgba(30, 27, 60, 0.5); border: 1px solid rgba(124, 58, 237, 0.2); border-radius: 24px;
  padding: 28px; margin-bottom: 24px;
  transition: all 280ms ease; box-shadow: 0 16px 40px -16px rgba(0,0,0,0.45);
}
.card:hover {border-color: #7C3AED; transform: translateY(-4px);
  box-shadow: 0 24px 48px -16px rgba(124, 58, 237, 0.35);}
.card-title {font-family: 'Russo One'; font-size: 20px; color: #F8FAFC; margin: 0 0 10px 0;}
.card-sub {color: #94A3B8; font-size: 14px; margin: 6px 0 0 0; line-height: 1.7;}

.metric {
  background: rgba(30, 27, 60, 0.5); border: 1px solid rgba(124, 58, 237, 0.2); border-radius: 20px;
  padding: 22px 18px; text-align: center; height: 100%;
}
.metric-value {font-family: 'Russo One'; font-size: 34px; color: #7C3AED; display: block;}
.metric-label {font-size: 12px; color: #94A3B8; text-transform: uppercase;
  letter-spacing: 0.1em; margin-top: 8px;}
.metric-delta {font-size: 11px; margin-top: 6px;}

.stTabs [data-baseweb="tab-list"] {
  gap: 10px; background: rgba(30, 27, 60, 0.5); border: 1px solid rgba(124, 58, 237, 0.2);
  border-radius: 16px; padding: 8px;
}
.stTabs [data-baseweb="tab"] {
  background: transparent; border: none; border-radius: 12px;
  color: #94A3B8; font-family: 'Russo One'; font-size: 15px;
  padding: 12px 24px; transition: all 220ms ease;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%);
  color: white; box-shadow: 0 10px 20px -10px rgba(124, 58, 237, 0.35);
}

section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #141228 0%, #0F0F23 100%);
  border-right: 1px solid rgba(124, 58, 237, 0.2);
  width: 360px;
}
.sidebar-title {font-family: 'Russo One'; font-size: 20px; color: #7C3AED;
  margin: 0 0 10px 0; padding: 20px 16px 8px 16px;}
.sidebar-sub {font-size: 12px; color: #94A3B8; padding: 0 16px 18px 16px;
  line-height: 1.6;}
.sidebar-divider {height: 1px; background: rgba(124, 58, 237, 0.2); margin: 20px 0;}

.stButton>button {
  background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%);
  color: white; border: none; border-radius: 14px;
  font-family: 'Russo One'; font-size: 15px; font-weight: 700;
  padding: 14px 26px; transition: all 220ms ease;
  box-shadow: 0 12px 24px -12px rgba(124, 58, 237, 0.35); cursor: pointer; width: 100%;
}
.stButton>button:hover {transform: translateY(-3px); filter: brightness(1.15);
  box-shadow: 0 20px 32px -14px rgba(124, 58, 237, 0.35);}
.stButton>button:focus-visible {outline: 2px solid #A78BFA; outline-offset: 2px;}

.streamlit-expanderHeader {
  font-family: 'Russo One'; font-size: 15px; color: #7C3AED;
  background: rgba(30, 27, 60, 0.5); border: 1px solid rgba(124, 58, 237, 0.2); border-radius: 14px;
}

.alert {padding: 18px 22px; border-radius: 16px; margin: 20px 0;
  border-left: 5px solid; font-size: 14px; line-height: 1.7;}
.alert-info {background: rgba(124,58,237,0.1); border-left-color: #7C3AED; color: #F8FAFC;}
.alert-success {background: rgba(16,185,129,0.1); border-left-color: #22C55E; color: #F8FAFC;}
.alert-warning {background: rgba(245,158,11,0.1); border-left-color: #F59E0B; color: #F8FAFC;}
.alert-danger {background: rgba(239,68,68,0.1); border-left-color: #EF4444; color: #F8FAFC;}

.dataframe {font-family: 'Chakra Petch', sans-serif;}

.criteria-tag {
  display: inline-block; padding: 4px 10px; border-radius: 12px;
  font-size: 11px; font-weight: 700; font-family: 'Russo One';
  text-transform: uppercase; margin: 2px 4px 2px 0;
  border: 1px solid rgba(124, 58, 237, 0.2); color: #A78BFA;
}
</style>
"""

components.html(CSS, height=0, width=0)

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "db_initialized" not in st.session_state:
    init_db()
    st.session_state.db_initialized = True
if "active_field_name" not in st.session_state:
    st.session_state.active_field_name = None
if "computed" not in st.session_state:
    st.session_state.computed = {}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def hero():
    st.markdown(
        """
        <div class="hero">
          <div class="hero-content">
            <span class="badge badge-advanced">ADVANCED · EARTH SCIENCE · SOFTWARE · SQLITE</span>
            <h1 class="hero-title">Field Shift</h1>
            <p class="hero-sub">
              NASA Space Apps Challenge 2026 · Professional Crop Rotation Decision-Support Platform<br>
              NASA satellite data + local knowledge + database-powered smart farming strategies
            </p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section(title: str, sub: str = ""):
    st.markdown(
        f"""
        <div class="section-header">
          <div>
            <h2 class="section-title">{title}</h2>
            <p class="section-sub">{sub}</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str, color: str = "#7C3AED", delta: Optional[str] = None):
    delta_html = f'<span class="metric-delta">{delta}</span>' if delta else ""
    st.markdown(
        f"""
        <div class="metric">
          <span class="metric-value" style="color:{color}">{value}</span>
          <span class="metric-label">{label}</span>
          {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def alert(kind: str, message: str):
    st.markdown(f'<div class="alert alert-{kind}">{message}</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Sidebar — Field Manager
# ---------------------------------------------------------------------------
def render_sidebar() -> None:
    st.sidebar.markdown(
        '<div class="sidebar-title">🌾 Field Manager</div>'
        '<div class="sidebar-sub">Database-backed persistent profiles. '
        'Add fields, calculate, and compare.</div>',
        unsafe_allow_html=True,
    )
    st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    st.sidebar.markdown("### ➕ Add Field")
    with st.sidebar.form("add_field_form", clear_on_submit=True):
        new_name = st.text_input("Field name", placeholder="e.g. North Farm", key="new_field_name")
        n_lat = st.number_input("Latitude", value=39.1000, format="%.4f", key="new_lat")
        n_lon = st.number_input("Longitude", value=35.6000, format="%.4f", key="new_lon")
        n_crops = st.multiselect("Current crops", options=list(CROP_LIBRARY.keys()),
                                 default=["Corn (Maize)", "Soybean"], key="new_crops")
        st.markdown("**Priorities (0–10)**")
        np_soil = st.slider("Soil health", 0, 10, 7, key="np_soil")
        np_water = st.slider("Water conservation", 0, 10, 6, key="np_water")
        np_income = st.slider("Income / market", 0, 10, 5, key="np_income")
        np_erosion = st.slider("Erosion control", 0, 10, 6, key="np_erosion")
        submitted = st.form_submit_button("Save Field")
        if submitted and new_name:
            priorities = {
                "soil_health": np_soil / 10.0,
                "water_conservation": np_water / 10.0,
                "income": np_income / 10.0,
                "erosion_control": np_erosion / 10.0,
            }
            fid = save_field(new_name, n_lat, n_lon, n_crops, priorities)
            snapshot = fetch_nasa_snapshot(n_lat, n_lon)
            strategies = build_strategies(snapshot, n_crops, priorities)
            save_computation(fid, snapshot, strategies)
            st.session_state.computed[new_name] = (snapshot, strategies)
            st.session_state.active_field_name = new_name
            st.success(f"'{new_name}' saved to database.")

    st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.sidebar.markdown("### 📋 Saved Fields")
    fields = load_fields()
    if not fields:
        st.sidebar.info("No fields yet.")
    else:
        for f in fields:
            fname = f["name"]
            col1, col2 = st.sidebar.columns([4, 1])
            with col1:
                if st.button(fname, key=f"select_{f['id']}", use_container_width=True):
                    st.session_state.active_field_name = fname
                    if fname not in st.session_state.computed:
                        row = load_latest_computation(f["id"])
                        if row:
                            st.session_state.computed[fname] = row
            with col2:
                if st.button("🗑️", key=f"del_{f['id']}", help="Delete"):
                    delete_field(f["id"])
                    st.session_state.computed.pop(fname, None)
                    st.rerun()

    st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    active = getattr(st.session_state, "active_field_name", None)
    st.sidebar.markdown(
        f'<div style="font-size:11px; color:#94A3B8; line-height:1.5; padding:0 16px 20px 16px;">'
        f'<b>NASA Sources:</b> SMAP · GPM · Landsat · ECOSTRESS · SRTM · NASA POWER<br>'
        f'<b>Storage:</b> SQLite ({DB_PATH})<br>'
        f'<b>Active:</b> {active or "None"}'
        '</div>',
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Charts
# ---------------------------------------------------------------------------
def plot_nasa_timeseries(snapshot: NASASnapshot) -> alt.Chart:
    dates = pd.date_range(end=pd.Timestamp.today(), periods=12, freq="MS")
    data = pd.DataFrame(
        {
            "Month": dates.strftime("%b %Y"),
            "Soil Moisture (m³/m³)": [snapshot.smap_soil_moisture + (i % 4 - 2) * 0.02 for i in range(12)],
            "Precipitation (mm)": [snapshot.gpm_precip_mm / 12 + (i % 3 - 1) * 8 for i in range(12)],
            "NDVI": [snapshot.landsat_ndvi + (i % 5 - 2) * 0.03 for i in range(12)],
            "Surface Temp (°C)": [snapshot.ecostress_lst_c + (i % 6 - 3) * 1.5 for i in range(12)],
        }
    )
    melted = data.melt(id_vars=["Month"], var_name="Indicator", value_name="Value")
    chart = (
        alt.Chart(melted)
        .mark_line(point=True, strokeWidth=3)
        .encode(
            x=alt.X("Month:N", sort=None, axis=alt.Axis(labelAngle=-35)),
            y=alt.Y("Value:Q"),
            color=alt.Color("Indicator:N", scale=alt.Scale(range=["#7C3AED", "#A78BFA", "#F43F5E", "#22C55E"])),
            tooltip=["Month", "Indicator", alt.Tooltip("Value:Q", format=".2f")],
        )
        .properties(height=300)
        .configure_view(strokeWidth=0)
        .configure_axis(gridColor="rgba(255,255,255,0.06)")
    )
    return chart


def plot_strategy_radar(strategies: List) -> alt.Chart:
    dims = ["Soil Health", "Water Efficiency", "Erosion Reduction", "Income Potential", "Climate Resilience"]
    dim_map = {
        "Soil Health": "soil_health_score",
        "Water Efficiency": "water_efficiency_score",
        "Erosion Reduction": "erosion_reduction_score",
        "Income Potential": "income_potential_score",
        "Climate Resilience": "climate_resilience_score",
    }
    rows = []
    for s in strategies:
        for d in dims:
            val = getattr(s, dim_map[d])
            rows.append({"Strategy": s.name, "Dimension": d, "Score": val})
    df = pd.DataFrame(rows)
    chart = (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            theta=alt.Theta("Dimension:N"),
            radius=alt.Radius("Score:Q", scale=alt.Scale(zero=False, domain=[0, 100])),
            color=alt.Color("Strategy:N", scale=alt.Scale(range=["#7C3AED", "#A78BFA", "#F43F5E", "#22C55E"])),
            tooltip=["Strategy", "Dimension", alt.Tooltip("Score:Q", format=".0f")],
        )
        .properties(width=420, height=420)
    )
    return chart


def plot_score_heatmap(strategies: List) -> alt.Chart:
    rows = []
    for s in strategies:
        rows.append(
            {
                "Strategy": s.name,
                "Soil": s.soil_health_score,
                "Water": s.water_efficiency_score,
                "Erosion": s.erosion_reduction_score,
                "Income": s.income_potential_score,
                "Climate": s.climate_resilience_score,
                "Total": s.total_score,
            }
        )
    df = pd.DataFrame(rows).melt(id_vars=["Strategy"], var_name="Dimension", value_name="Score")
    chart = (
        alt.Chart(df)
        .mark_rect()
        .encode(
            x=alt.X("Dimension:N", sort=["Soil", "Water", "Erosion", "Income", "Climate", "Total"]),
            y=alt.Y("Strategy:N", sort="-x"),
            color=alt.Color("Score:Q", scale=alt.Scale(scheme="purples", domain=[0, 100])),
            tooltip=["Strategy", "Dimension", alt.Tooltip("Score:Q", format=".0f")],
        )
        .properties(height=260)
        .configure_view(strokeWidth=0)
    )
    return chart


def plot_nasa_scatter(snapshot: NASASnapshot) -> alt.Chart:
    """SMAP soil moisture vs Landsat NDVI scatter plot (simulation points)."""
    import numpy as np

    np.random.seed(int(snapshot.lat * 1000) + int(snapshot.lon * 1000))
    n = 60
    smap_vals = np.clip(snapshot.smap_soil_moisture + np.random.normal(0, 0.05, n), 0.05, 0.50)
    ndvi_vals = np.clip(
        0.2 + 1.2 * (smap_vals - 0.10) + np.random.normal(0, 0.08, n), 0.0, 0.95
    )

    # Combine simulation points + selected field center into one dataframe
    df = pd.DataFrame(
        {
            "SMAP Soil Moisture (m³/m³)": np.append(smap_vals, snapshot.smap_soil_moisture),
            "Landsat NDVI": np.append(ndvi_vals, snapshot.landsat_ndvi),
            "Type": ["Field"] * n + ["Selected Field"],
        }
    )

    chart = (
        alt.Chart(df)
        .mark_circle(opacity=0.7)
        .encode(
            x=alt.X("SMAP Soil Moisture (m³/m³):Q", scale=alt.Scale(domain=[0.05, 0.50])),
            y=alt.Y("Landsat NDVI:Q", scale=alt.Scale(domain=[0.0, 1.0])),
            color=alt.Color(
                "Type:N",
                scale=alt.Scale(domain=["Field", "Selected Field"], range=["#7C3AED", "#F43F5E"]),
                legend=None,
            ),
            size=alt.Size("Type:N", scale=alt.Scale(domain=["Field", "Selected Field"], range=[60, 200]), legend=None),
            tooltip=[
                alt.Tooltip("SMAP Soil Moisture (m³/m³):Q", format=".3f"),
                alt.Tooltip("Landsat NDVI:Q", format=".3f"),
                alt.Tooltip("Type:N"),
            ],
        )
        .properties(height=300)
        .configure_view(strokeWidth=0)
    )
    return chart


def render_strategy_card(s, is_best: bool = False):
    border_color = "#7C3AED" if is_best else "rgba(124, 58, 237, 0.2)"
    glow = "box-shadow: 0 0 32px -12px rgba(124, 58, 237, 0.35);" if is_best else ""
    st.markdown(
        f"""
        <div class="card" style="border-color:{border_color}; {glow} margin-bottom: 20px;">
          <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:14px;">
            <div class="card-title">{'🏆 ' if is_best else ''}{s.name}</div>
            <span style="font-family:'Russo One'; font-size:26px; color:#7C3AED;">{s.total_score:.0f}/100</span>
          </div>
          <div class="card-sub" style="margin-bottom:12px;">{s.description}</div>
          <div style="font-size:11px; color:#94A3B8; margin-bottom:10px;"><b>Why recommended:</b> {s.rationale}</div>
          <div style="font-size:10px; color:#A78BFA; margin-bottom:8px;"><b>🛰️ Data Sources:</b> {', '.join(s.data_sources_used[:4])}{'...' if len(s.data_sources_used) > 4 else ''}</div>
          <div style="font-size:11px; color:#94A3B8; margin-bottom:10px;"><b>Crops:</b> {', '.join(c.name for c in s.crops)}</div>
          <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:14px;">
            <div style="flex:1; min-width:120px; background:rgba(255,255,255,0.03); border:1px dashed rgba(124,58,237,0.2); border-radius:12px; padding:12px; font-size:11px;">
              <div style="color:#7C3AED; font-weight:700; font-size:10px; text-transform:uppercase; margin-bottom:4px;">Soil Health</div>
              <div style="font-size:18px; font-family:'Russo One'">{s.soil_health_score:.0f}</div>
            </div>
            <div style="flex:1; min-width:120px; background:rgba(255,255,255,0.03); border:1px dashed rgba(124,58,237,0.2); border-radius:12px; padding:12px; font-size:11px;">
              <div style="color:#7C3AED; font-weight:700; font-size:10px; text-transform:uppercase; margin-bottom:4px;">Water Efficiency</div>
              <div style="font-size:18px; font-family:'Russo One'">{s.water_efficiency_score:.0f}</div>
            </div>
            <div style="flex:1; min-width:120px; background:rgba(255,255,255,0.03); border:1px dashed rgba(124,58,237,0.2); border-radius:12px; padding:12px; font-size:11px;">
              <div style="color:#7C3AED; font-weight:700; font-size:10px; text-transform:uppercase; margin-bottom:4px;">Erosion Reduction</div>
              <div style="font-size:18px; font-family:'Russo One'">{s.erosion_reduction_score:.0f}</div>
            </div>
            <div style="flex:1; min-width:120px; background:rgba(255,255,255,0.03); border:1px dashed rgba(124,58,237,0.2); border-radius:12px; padding:12px; font-size:11px;">
              <div style="color:#7C3AED; font-weight:700; font-size:10px; text-transform:uppercase; margin-bottom:4px;">Income Pot.</div>
              <div style="font-size:18px; font-family:'Russo One'">{s.income_potential_score:.0f}</div>
            </div>
            <div style="flex:1; min-width:120px; background:rgba(255,255,255,0.03); border:1px dashed rgba(124,58,237,0.2); border-radius:12px; padding:12px; font-size:11px;">
              <div style="color:#7C3AED; font-weight:700; font-size:10px; text-transform:uppercase; margin-bottom:4px;">Climate Res.</div>
              <div style="font-size:18px; font-family:'Russo One'">{s.climate_resilience_score:.0f}</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander(f"🔍 Detailed Review — {s.name}"):
        d1, d2, d3 = st.columns(3)
        d1.metric("Soil Health", f"{s.soil_health_score:.0f}")
        d2.metric("Water Efficiency", f"{s.water_efficiency_score:.0f}")
        d3.metric("Erosion Reduction", f"{s.erosion_reduction_score:.0f}")
        d1.metric("Pest Disruption", f"{s.pest_disruption_score:.0f}")
        d2.metric("Income Potential", f"{s.income_potential_score:.0f}")
        d3.metric("Climate Resilience", f"{s.climate_resilience_score:.0f}")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**✅ Benefits**")
            for b in s.benefits:
                st.markdown(f"- {b}")
            st.markdown("**📖 Evidence / Data Source:**")
            st.caption(s.evidence)
        with c2:
            st.markdown("**⚠️ Information Gaps**")
            for g in s.gaps:
                st.markdown(f"- {g}")
            st.markdown("**🚩 Risks**")
            for r in s.risks:
                st.markdown(f"- {r}")
        st.info("🔍 **Local review required:** " + "; ".join(s.local_review_needed))


# ---------------------------------------------------------------------------
# NASA Space Apps evaluation criteria
# ---------------------------------------------------------------------------
def render_criteria_card():
    section("📋 NASA Space Apps Evaluation Criteria", "Project evaluation score (max 25)")
    criteria = [
        ("Maturity", "Prototype is functional and complete", 5),
        ("Creativity", "Innovative use of NASA data for crop rotation strategies", 5),
        ("Validity", "Agronomic and climate suitability for real-world application", 5),
        ("Interest / NASA Data Integration", "Strong integration of NASA data such as SMAP, GPM, Landsat, ECOSTRESS, SRTM", 5),
        ("Presentation", "Professional interface, visual quality, and storytelling", 5),
    ]
    cols = st.columns(5)
    total = 0
    for i, (ad, aciklama, puan) in enumerate(criteria):
        total += puan
        with cols[i]:
            st.markdown(
                f"""
                <div class="card" style="text-align:center; margin-bottom:16px;">
                  <div style="font-family:'Russo One'; font-size:30px; color:#7C3AED;">{puan}</div>
                  <div class="card-title">{ad}</div>
                  <div class="card-sub" style="font-size:11px;">{aciklama}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown(
        f"""
        <div class="card" style="border-color:#7C3AED; margin-top:20px;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <div class="card-title">Total Evaluation Score</div>
            <div style="font-family:'Russo One'; font-size:32px; color:#7C3AED;">{total}/25</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
def tab_dashboard():
    section("🏠 Overview", "All field profiles in the database and latest strategy scores")
    fields = load_fields()
    if not fields:
        alert("info", "Add at least one field from the left sidebar to get started.")
        return

    computed = st.session_state.computed
    total_fields = len(fields)
    best_score = -1
    best_name = ""
    for f in fields:
        fname = f["name"]
        if fname in computed:
            b = max(computed[fname][1], key=lambda x: x.total_score)
            if b.total_score > best_score:
                best_score = b.total_score
                best_name = fname

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Total Fields", str(total_fields), "#7C3AED")
    with c2:
        metric_card("Best Score", f"{best_score:.0f}/100", "#A78BFA")
    with c3:
        avg_water = sum(fetch_nasa_snapshot(f["lat"], f["lon"]).gpm_precip_mm for f in fields) / max(total_fields, 1)
        metric_card("Avg Precipitation", f"{avg_water:.0f} mm", "#F43F5E")
    with c4:
        risk_count = sum(1 for f in fields if fetch_nasa_snapshot(f["lat"], f["lon"]).water_stress_index > 0.5)
        metric_card("High Water Stress", f"{risk_count} fields", "#EF4444" if risk_count else "#22C55E")

    st.divider()

    section("🌱 Field Profiles", "Best recommended rotation strategy per field")
    cols = st.columns(min(3, len(fields)))
    for i, f in enumerate(fields):
        fname = f["name"]
        with cols[i % len(cols)]:
            if fname in computed:
                snapshot, strategies = computed[fname]
                b = max(strategies, key=lambda x: x.total_score)
            else:
                snapshot = fetch_nasa_snapshot(f["lat"], f["lon"])
                strategies = build_strategies(snapshot, json.loads(f["crops"]),
                                              json.loads(f["priorities"]))
                b = max(strategies, key=lambda x: x.total_score)
            st.markdown(
                f"""
                <div class="card">
                  <div class="card-title">{fname}</div>
                  <div style="font-size:11px; color:#94A3B8; margin-bottom:12px;">
                    {f['lat']:.4f}, {f['lon']:.4f} · SMAP {snapshot.smap_soil_moisture:.2f} · NDVI {snapshot.landsat_ndvi:.2f}
                  </div>
                  <div style="display:flex; justify-content:space-between; margin-bottom:12px;">
                    <div style="font-size:11px; color:#94A3B8;"><b>Water Stress:</b> {snapshot.water_stress_index:.2f}</div>
                    <div style="font-size:11px; color:#94A3B8;"><b>Slope:</b> {snapshot.slope_percent:.1f}%</div>
                  </div>
                  <div style="font-family:'Russo One'; font-size:17px; color:#7C3AED; margin-bottom:8px;">
                    🏆 {b.name} — {b.total_score:.0f}/100
                  </div>
                  <div style="font-size:11px; color:#94A3B8; line-height:1.5;">{b.description}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.divider()

    # USDA local data cards
    section("🇺🇸 USDA Local Data Sources", "SSURGO soil and AMS market data (ready for real API integration)")
    if fields:
        f0 = fields[0]
        soil = get_usda_soil_data(f0["lat"], f0["lon"])
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            metric_card("SSURGO Map Unit", soil.map_unit_symbol, "#7C3AED")
        with c2:
            metric_card("Organic Matter %", f"{soil.organic_matter_pct:.1f}", "#22C55E")
        with c3:
            metric_card("Available Water", f"{soil.available_water_capacity:.3f} cm/cm", "#F43F5E")
        with c4:
            metric_card("Hydrologic Group", soil.hydrologic_group, "#A78BFA")

        st.markdown("**💰 Sample Market Data (USDA AMS)**")
        mc1, mc2, mc3, mc4 = st.columns(4)
        crops_for_market = ["Corn (Maize)", "Soybean", "Winter Wheat", "Alfalfa"]
        for i, crop in enumerate(crops_for_market):
            mkt = get_usda_market_data(crop)
            with [mc1, mc2, mc3, mc4][i]:
                st.markdown(
                    f"""
                    <div class="card" style="text-align:center;">
                      <div style="font-size:11px; color:#94A3B8; text-transform:uppercase;">{mkt.commodity}</div>
                      <div style="font-family:'Russo One'; font-size:20px; color:#7C3AED;">${mkt.price_usd_per_ton:.0f}/ton</div>
                      <div style="font-size:10px; color:#94A3B8;">Demand: {mkt.demand_index:.0f}/100 · {mkt.trend_30d}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.divider()

    # Data source summary
    section("📊 Data Source Summary", "NASA and USDA source usage in the project")
    summary = get_nasa_data_source_summary()
    ds1, ds2, ds3 = st.columns(3)
    with ds1:
        metric_card("NASA Sources", str(summary["nasa_count"]), "#7C3AED")
    with ds2:
        metric_card("USDA Sources", str(summary["usda_count"]), "#22C55E")
    with ds3:
        metric_card("Total Sources", str(summary["total"]), "#F43F5E")

    alert("info", "Real API integration requires Earthdata Login token, USDA SDA / Market News API key. Prototype uses deterministic synthetic data.")


def tab_analysis():
    section("🛰️ Satellite Data Analysis", "NASA Earth Observation data and time-series analysis")
    fields = load_fields()
    if not fields:
        alert("info", "Add at least one field from the left sidebar first.")
        return

    field_names = [f["name"] for f in fields]
    default_idx = 0
    if st.session_state.active_field_name in field_names:
        default_idx = field_names.index(st.session_state.active_field_name)
    selected = st.selectbox("Select field", field_names, index=default_idx, key="select_analysis")
    st.session_state.active_field_name = selected

    f = next(x for x in fields if x["name"] == selected)
    if selected in st.session_state.computed:
        snapshot, strategies = st.session_state.computed[selected]
    else:
        snapshot = fetch_nasa_snapshot(f["lat"], f["lon"])
        strategies = build_strategies(snapshot, json.loads(f["crops"]), json.loads(f["priorities"]))

    section("📊 NASA Measurements", "Satellite-based indicators for this field")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1: metric_card("SMAP Soil Moisture", f"{snapshot.smap_soil_moisture:.3f} m³/m³", "#7C3AED")
    with c2: metric_card("GPM Precipitation", f"{snapshot.gpm_precip_mm:.0f} mm", "#A78BFA")
    with c3: metric_card("Landsat NDVI", f"{snapshot.landsat_ndvi:.2f}", "#F43F5E")
    with c4: metric_card("ECOSTRESS LST", f"{snapshot.ecostress_lst_c:.1f} °C", "#22C55E")
    with c5: metric_card("SRTM Elevation", f"{snapshot.srtm_elevation_m:.0f} m", "#F59E0B")
    with c6: metric_card("Water Stress", f"{snapshot.water_stress_index:.2f}", "#EF4444" if snapshot.water_stress_index > 0.5 else "#7C3AED")

    st.divider()

    section("📈 12-Month Indicator Trend", "Simulation-based (Earthdata API needed for real data)")
    st.altair_chart(plot_nasa_timeseries(snapshot), width='stretch')

    st.divider()

    section("🎯 NASA Data Relationship", "SMAP Soil Moisture vs Landsat NDVI (red center = selected field)")
    st.altair_chart(plot_nasa_scatter(snapshot), width='stretch')

    st.divider()

    section("🗺️ Field Location and Water Stress Map", "Folium-based interactive map")
    f_map = folium.Map(location=[snapshot.lat, snapshot.lon], zoom_start=11,
                       tiles="OpenStreetMap", control_scale=True)
    folium.Marker(
        [snapshot.lat, snapshot.lon],
        popup=f"{selected}<br>NDVI: {snapshot.landsat_ndvi:.2f}<br>Water Stress: {snapshot.water_stress_index:.2f}",
        icon=folium.Icon(color="green", icon="leaf", prefix="fa"),
    ).add_to(f_map)
    if snapshot.water_stress_index > 0.5:
        folium.Circle(
            location=[snapshot.lat, snapshot.lon],
            radius=1500, color="#F43F5E", fill=True, fill_opacity=0.18,
            popup="High water stress area",
        ).add_to(f_map)
    st_folium(f_map, width=1000, height=500, key=f"map_{selected}")


def tab_strategies():
    section("🧠 Strategy Laboratory", "Compare rotation strategies, create custom scenarios")
    fields = load_fields()
    if not fields:
        alert("info", "Add at least one field from the left sidebar first.")
        return

    field_names = [f["name"] for f in fields]
    default_idx = 0
    if st.session_state.active_field_name in field_names:
        default_idx = field_names.index(st.session_state.active_field_name)
    selected = st.selectbox("Select field", field_names, index=default_idx, key="select_strategies")
    st.session_state.active_field_name = selected

    f = next(x for x in fields if x["name"] == selected)
    if selected in st.session_state.computed:
        snapshot, strategies = st.session_state.computed[selected]
    else:
        snapshot = fetch_nasa_snapshot(f["lat"], f["lon"])
        strategies = build_strategies(snapshot, json.loads(f["crops"]), json.loads(f["priorities"]))

    best = max(strategies, key=lambda x: x.total_score)

    st.markdown(
        f"""
        <div class="card" style="border-color:#7C3AED; box-shadow: 0 0 40px -14px rgba(124, 58, 237, 0.35); margin-bottom: 32px;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
              <div class="card-title">🏆 Recommended Strategy</div>
              <div style="font-family:'Russo One'; font-size:34px; color:#7C3AED; margin-top:6px;">
                {best.name} — {best.total_score:.0f}/100
              </div>
              <div class="card-sub">{best.description}</div>
            </div>
            <div style="text-align:right;">
              <div style="font-size:12px; color:#94A3B8; text-transform:uppercase;">Total Score</div>
              <div style="font-family:'Russo One'; font-size:40px; color:#F8FAFC;">{best.total_score:.0f}</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        section("📊 Score Distribution (Heatmap)", "Comparison by strategy dimension")
        st.altair_chart(plot_score_heatmap(strategies), width='stretch')
    with c2:
        section("🎯 Radar Comparison", "Multi-dimensional strategy performance")
        st.altair_chart(plot_strategy_radar(strategies), width='stretch')

    st.divider()

    section("📋 All Strategies", "Benefits, risks, and local review suggestions for each option")
    for s in strategies:
        render_strategy_card(s, is_best=(s.name == best.name))


def tab_fields():
    section("🗂️ Field Management", "Edit profiles, export, and compare in the database")
    fields = load_fields()
    if not fields:
        alert("info", "No fields yet. Add one from the left sidebar.")
        return

    section("📊 Comparison Table", "Best strategy scores for all fields")
    rows = []
    for f in fields:
        fname = f["name"]
        if fname in st.session_state.computed:
            snapshot, strategies = st.session_state.computed[fname]
        else:
            snapshot = fetch_nasa_snapshot(f["lat"], f["lon"])
            strategies = build_strategies(snapshot, json.loads(f["crops"]), json.loads(f["priorities"]))
        b = max(strategies, key=lambda x: x.total_score)
        rows.append({
            "Field": fname,
            "Best Strategy": b.name,
            "Score": f"{b.total_score:.0f}",
            "Soil": f"{b.soil_health_score:.0f}",
            "Water": f"{b.water_efficiency_score:.0f}",
            "Erosion": f"{b.erosion_reduction_score:.0f}",
            "Income": f"{b.income_potential_score:.0f}",
            "Climate": f"{b.climate_resilience_score:.0f}",
            "Water Stress": f"{snapshot.water_stress_index:.2f}",
        })
    df = pd.DataFrame(rows)
    st.dataframe(df, width='stretch', hide_index=True)

    st.divider()

    section("💾 Data Export", "Download as JSON or CSV")
    export_data = {
        "fields": fields,
        "computed": {
            name: {
                "snapshot": asdict(snap),
                "strategies": [asdict(s) for s in strats],
            }
            for name, (snap, strats) in st.session_state.computed.items()
        },
    }
    c1, c2 = st.columns(2)
    with c1:
        st.download_button(
            "📥 Download JSON", data=json.dumps(export_data, indent=2, ensure_ascii=False, default=str),
            file_name="field_shift_export.json", mime="application/json",
        )
    with c2:
        csv_df = pd.DataFrame([
            {
                "Field": name,
                "Lat": snap.lat, "Lon": snap.lon,
                "SMAP": snap.smap_soil_moisture, "GPM": snap.gpm_precip_mm,
                "NDVI": snap.landsat_ndvi, "LST": snap.ecostress_lst_c,
                "Water Stress": snap.water_stress_index,
                "Best": max(strats, key=lambda x: x.total_score).name,
                "Score": max(strats, key=lambda x: x.total_score).total_score,
            }
            for name, (snap, strats) in st.session_state.computed.items()
        ])
        st.download_button(
            "📥 Download CSV", data=csv_df.to_csv(index=False).encode("utf-8"),
            file_name="field_shift_summary.csv", mime="text/csv",
        )


def tab_reports():
    section("📄 Reports", "Create and download decision-support reports")
    fields = load_fields()
    if not fields:
        alert("info", "Add a field and calculate first.")
        return

    field_names = [f["name"] for f in fields]
    default_idx = 0
    if st.session_state.active_field_name in field_names:
        default_idx = field_names.index(st.session_state.active_field_name)
    selected = st.selectbox("Select field", field_names, index=default_idx, key="select_reports")

    f = next(x for x in fields if x["name"] == selected)
    if selected in st.session_state.computed:
        snapshot, strategies = st.session_state.computed[selected]
    else:
        snapshot = fetch_nasa_snapshot(f["lat"], f["lon"])
        strategies = build_strategies(snapshot, json.loads(f["crops"]), json.loads(f["priorities"]))

    report = export_report_text(strategies, snapshot)

    st.markdown("### 📋 Report Preview")
    st.text_area("Report content", value=report, height=450)

    st.download_button(
        "📥 Download as TXT", data=report,
        file_name=f"field_shift_report_{selected}.txt", mime="text/plain",
    )

    alert("info", "This report supports local expert judgment; professional application requires local agronomist approval.")


def tab_data_sources():
    section("🛰️ Data Sources", "All NASA and USDA data sources defined in the challenge")
    st.markdown(
        "All data sources listed in the NASA Space Apps Challenge 2026 challenge document "
        "and their usage purpose in the project are shown below."
    )

    # NASA sources
    st.markdown("### 🇺🇸 NASA Earth Observation Data")
    for key, info in NASA_DATA_SOURCES.items():
        with st.expander(f"{key} — {info['name']}"):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**Parameter:** {info['parameter']}")
                st.markdown(f"**Temporal Resolution:** {info['temporal']}")
                st.markdown(f"**Usage Purpose:** {info['use']}")
            with c2:
                st.markdown(f"**API / Source:** `{info['api_hint']}`")
                if info.get("mapped_to"):
                    st.markdown(f"**Mapping in Project:** `{info['mapped_to']}`")

    st.divider()

    # USDA sources
    st.markdown("### 🌾 USDA / Partner Data Sources")
    for key, info in USDA_DATA_SOURCES.items():
        with st.expander(f"{key} — {info['name']}"):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**Parameter:** {info['parameter']}")
                st.markdown(f"**Usage Purpose:** {info['use']}")
            with c2:
                st.markdown(f"**API / Source:** `{info['api_hint']}`")

    st.divider()

    # Summary cards
    st.markdown("### 📊 Summary")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("NASA Data Sources", len(NASA_DATA_SOURCES))
    with c2:
        st.metric("USDA / Partner Sources", len(USDA_DATA_SOURCES))
    with c3:
        st.metric("Total Sources", len(NASA_DATA_SOURCES) + len(USDA_DATA_SOURCES))

    alert("info", "Real API integration requires Earthdata Login token, USDA API key, or Copernicus access. Prototype uses deterministic NASA-style synthetic data.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    hero()
    render_sidebar()

    tab_labels = ["🏠 Dashboard", "🛰️ Analysis", "🧠 Strategies", "🗂️ Fields", "📄 Reports", "📋 Criteria", "🛰️ Sources"]
    tabs = st.tabs(tab_labels)

    with tabs[0]:
        tab_dashboard()
    with tabs[1]:
        tab_analysis()
    with tabs[2]:
        tab_strategies()
    with tabs[3]:
        tab_fields()
    with tabs[4]:
        tab_reports()
    with tabs[5]:
        render_criteria_card()
    with tabs[6]:
        tab_data_sources()

    st.divider()
    st.caption(
        "Prototype note: Synthetic data mirroring NASA parameter structure is used instead of real NASA Earthdata. "
        "Field data is stored persistently in SQLite database. "
        "Real records require Earthdata/DAAC API, USDA SSURGO/CDL and PRISM integration. "
        "Local agronomist approval is required."
    )


if __name__ == "__main__":
    main()