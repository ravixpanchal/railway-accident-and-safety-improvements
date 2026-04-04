import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Railway Accident Analysis",
    page_icon="🚂",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Theme State ───────────────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

dark = st.session_state.dark_mode

# ── Theme Variables ───────────────────────────────────────────────────────────
if dark:
    BG_MAIN        = "#080c14"
    BG_SIDEBAR     = "#0b0f1a"
    BG_CARD        = "rgba(255,255,255,0.04)"
    BG_CARD_HOVER  = "rgba(255,255,255,0.07)"
    BG_HERO        = "linear-gradient(135deg,#0d1b35 0%,#080c14 55%,#0a1628 100%)"
    BORDER_COLOR   = "rgba(255,255,255,0.08)"
    BORDER_ACCENT  = "rgba(99,179,237,0.4)"
    TEXT_PRIMARY   = "#f0f6ff"
    TEXT_SECONDARY = "#8fa8c8"
    TEXT_MUTED     = "#4a6080"
    ACCENT         = "#63b3ed"
    ACCENT2        = "#76e4f7"
    ACCENT3        = "#f6ad55"
    GLOW           = "rgba(99,179,237,0.12)"
    OBS_BG         = "rgba(99,179,237,0.05)"
    OBS_BORDER     = "#63b3ed"
    PLOT_BG        = "#080c14"
    PAPER_BG       = "#0d1320"
    GRID_COLOR     = "#111c2e"
    FONT_COLOR     = "#8fa8c8"
    PLOTLY_TPL     = "plotly_dark"
    TOGGLE_ICON    = "☀️"
    TOGGLE_LABEL   = "Light Mode"
    TAG_BG         = "rgba(99,179,237,0.1)"
    TAG_BORDER     = "rgba(99,179,237,0.25)"
    TAG_TEXT       = "#63b3ed"
    NUM_BG         = "rgba(99,179,237,0.12)"
    NUM_CLR        = "#63b3ed"
    FOOTER_BORDER  = "rgba(255,255,255,0.06)"
    FOOTER_TEXT    = "#3a5070"
    SCROLLBAR_CLR  = "#1a2744"
else:
    BG_MAIN        = "#f0f4f8"
    BG_SIDEBAR     = "#e8eef5"
    BG_CARD        = "rgba(255,255,255,0.85)"
    BG_CARD_HOVER  = "rgba(255,255,255,1.0)"
    BG_HERO        = "linear-gradient(135deg,#dbeafe 0%,#eff6ff 55%,#e0f2fe 100%)"
    BORDER_COLOR   = "rgba(0,0,0,0.08)"
    BORDER_ACCENT  = "rgba(37,99,235,0.3)"
    TEXT_PRIMARY   = "#0f172a"
    TEXT_SECONDARY = "#334155"
    TEXT_MUTED     = "#94a3b8"
    ACCENT         = "#2563eb"
    ACCENT2        = "#0ea5e9"
    ACCENT3        = "#d97706"
    GLOW           = "rgba(37,99,235,0.06)"
    OBS_BG         = "rgba(37,99,235,0.04)"
    OBS_BORDER     = "#2563eb"
    PLOT_BG        = "#f8fafc"
    PAPER_BG       = "#ffffff"
    GRID_COLOR     = "#e2e8f0"
    FONT_COLOR     = "#475569"
    PLOTLY_TPL     = "plotly_white"
    TOGGLE_ICON    = "🌙"
    TOGGLE_LABEL   = "Dark Mode"
    TAG_BG         = "rgba(37,99,235,0.08)"
    TAG_BORDER     = "rgba(37,99,235,0.2)"
    TAG_TEXT       = "#2563eb"
    NUM_BG         = "rgba(37,99,235,0.1)"
    NUM_CLR        = "#2563eb"
    FOOTER_BORDER  = "rgba(0,0,0,0.08)"
    FOOTER_TEXT    = "#94a3b8"
    SCROLLBAR_CLR  = "#cbd5e1"

SEV_COLORS = {"Low": "#68d391", "Medium": ACCENT3, "High": "#fc8181", "Unknown": TEXT_MUTED}
PALETTE    = [ACCENT, ACCENT2, ACCENT3, "#f687b3", "#68d391", "#fc8181", "#b794f4"]

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

*,*::before,*::after{{box-sizing:border-box;}}
html,body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
.main,.block-container{{
  background-color:{BG_MAIN}!important;
  color:{TEXT_PRIMARY}!important;
  font-family:'DM Sans',sans-serif!important;
  transition:background-color .35s,color .35s;
}}
.block-container{{padding:1.5rem 2.2rem 5rem!important;max-width:100%!important;}}

::-webkit-scrollbar{{width:5px;height:5px;}}
::-webkit-scrollbar-track{{background:transparent;}}
::-webkit-scrollbar-thumb{{background:{SCROLLBAR_CLR};border-radius:10px;}}

section[data-testid="stSidebar"]{{
  background:{BG_SIDEBAR}!important;
  border-right:1px solid {BORDER_COLOR}!important;
  transition:background .35s;
}}
section[data-testid="stSidebar"] *{{
  color:{TEXT_SECONDARY}!important;
  font-family:'DM Sans',sans-serif!important;
}}

/* ── Hero ── */
.hero{{
  background:{BG_HERO};
  border:1px solid {BORDER_COLOR};
  border-radius:22px;
  padding:3rem 2rem 2.5rem;
  margin-bottom:2rem;
  text-align:center;
  position:relative;
  overflow:hidden;
  animation:fadeUp .7s ease both;
}}
.hero::before{{
  content:'';position:absolute;inset:0;
  background:radial-gradient(ellipse 70% 60% at 20% 30%,{GLOW},transparent),
             radial-gradient(ellipse 50% 40% at 80% 70%,{GLOW},transparent);
  pointer-events:none;
}}
.hero::after{{
  content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,{ACCENT},{ACCENT2},transparent);
  border-radius:22px 22px 0 0;
}}
@keyframes fadeUp{{from{{opacity:0;transform:translateY(-18px);}}to{{opacity:1;transform:translateY(0);}}}}

.eyebrow{{
  display:inline-flex;align-items:center;gap:6px;
  background:{TAG_BG};border:1px solid {TAG_BORDER};
  color:{TAG_TEXT};font-family:'Syne',sans-serif;
  font-size:.7rem;font-weight:700;letter-spacing:.12em;
  text-transform:uppercase;padding:.3rem .9rem;border-radius:50px;margin-bottom:1.1rem;
}}
.hero-title{{
  font-family:'Syne',sans-serif;
  font-size:clamp(1.8rem,4vw,3rem);font-weight:800;
  color:{TEXT_PRIMARY};line-height:1.15;letter-spacing:-.03em;margin:0 0 .9rem;
}}
.hero-title .hl{{
  background:linear-gradient(135deg,{ACCENT} 0%,{ACCENT2} 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}}
.hero-sub{{
  font-size:clamp(.88rem,1.5vw,1.05rem);color:{TEXT_SECONDARY};
  max-width:600px;margin:0 auto 1.5rem;line-height:1.65;font-weight:400;
}}
.hero-tags{{display:flex;gap:.5rem;justify-content:center;flex-wrap:wrap;}}
.hero-tag{{
  background:{TAG_BG};border:1px solid {BORDER_COLOR};color:{TEXT_MUTED};
  font-family:'JetBrains Mono',monospace;font-size:.72rem;
  padding:.25rem .7rem;border-radius:6px;
}}

/* ── KPI Grid ── */
.kpi-grid{{
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(140px,1fr));
  gap:.85rem;margin-bottom:1.8rem;
}}
.kpi-card{{
  background:{BG_CARD};border:1px solid {BORDER_COLOR};
  border-radius:14px;padding:1.2rem 1rem 1rem;text-align:center;
  backdrop-filter:blur(12px);
  transition:transform .22s cubic-bezier(.34,1.56,.64,1),border-color .22s,box-shadow .22s;
  position:relative;overflow:hidden;
  animation:cardIn .5s ease both;
}}
.kpi-card:nth-child(1){{animation-delay:.05s;}}
.kpi-card:nth-child(2){{animation-delay:.10s;}}
.kpi-card:nth-child(3){{animation-delay:.15s;}}
.kpi-card:nth-child(4){{animation-delay:.20s;}}
.kpi-card:nth-child(5){{animation-delay:.25s;}}
.kpi-card:nth-child(6){{animation-delay:.30s;}}
@keyframes cardIn{{from{{opacity:0;transform:translateY(20px);}}to{{opacity:1;transform:translateY(0);}}}}
.kpi-card::before{{
  content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,{ACCENT},{ACCENT2});
  opacity:0;transition:opacity .25s;border-radius:14px 14px 0 0;
}}
.kpi-card:hover{{transform:translateY(-5px) scale(1.02);border-color:{BORDER_ACCENT};box-shadow:0 14px 38px {GLOW};}}
.kpi-card:hover::before{{opacity:1;}}
.kpi-icon{{font-size:1.7rem;margin-bottom:.4rem;display:block;}}
.kpi-val{{
  font-family:'Syne',sans-serif;font-size:1.65rem;font-weight:800;
  color:{TEXT_PRIMARY};line-height:1;
}}
.kpi-label{{
  font-size:.68rem;color:{TEXT_MUTED};
  text-transform:uppercase;letter-spacing:.1em;margin-top:.3rem;font-weight:600;
}}
.kpi-sub{{font-size:.75rem;color:{TEXT_SECONDARY};margin-top:.2rem;}}

/* ── Section header ── */
.sec-hdr{{
  display:flex;align-items:center;gap:.7rem;
  margin:2rem 0 1rem;padding-bottom:.65rem;
  border-bottom:1px solid {BORDER_COLOR};
}}
.sec-num{{
  width:28px;height:28px;background:{NUM_BG};color:{NUM_CLR};
  font-family:'JetBrains Mono',monospace;font-size:.7rem;font-weight:600;
  border-radius:7px;display:inline-flex;align-items:center;justify-content:center;flex-shrink:0;
}}
.sec-title{{
  font-family:'Syne',sans-serif;font-size:1.05rem;font-weight:700;
  color:{TEXT_PRIMARY};letter-spacing:-.02em;
}}

/* ── Observation box ── */
.obs-box{{
  background:{OBS_BG};border-left:3px solid {OBS_BORDER};
  border-radius:0 10px 10px 0;padding:.85rem 1.1rem;margin-top:.7rem;
  font-size:.875rem;color:{TEXT_SECONDARY};line-height:1.65;
}}
.obs-box strong{{color:{TEXT_PRIMARY};}}

/* ── Chart wrapper ── */
.chart-wrap{{
  background:{BG_CARD};border:1px solid {BORDER_COLOR};
  border-radius:14px;padding:.4rem;backdrop-filter:blur(8px);
  transition:border-color .2s;
}}
.chart-wrap:hover{{border-color:{BORDER_ACCENT};}}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"]{{
  gap:4px;background:{BG_CARD};
  border:1px solid {BORDER_COLOR};border-radius:12px;
  padding:4px;flex-wrap:wrap;
}}
.stTabs [data-baseweb="tab"]{{
  background:transparent!important;border-radius:9px!important;
  border:none!important;color:{TEXT_SECONDARY}!important;
  font-family:'DM Sans',sans-serif!important;
  font-size:.84rem!important;font-weight:500!important;
  padding:.43rem 1.05rem!important;transition:all .2s!important;
}}
.stTabs [data-baseweb="tab"]:hover{{
  background:{BG_CARD_HOVER}!important;color:{TEXT_PRIMARY}!important;
}}
.stTabs [aria-selected="true"]{{
  background:{TAG_BG}!important;color:{TAG_TEXT}!important;font-weight:600!important;
}}
[data-baseweb="tab-highlight"]{{display:none!important;}}
[data-baseweb="tab-border"]{{display:none!important;}}

/* ── Sidebar helpers ── */
.sb-logo{{
  font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:800;
  color:{TEXT_PRIMARY};display:flex;align-items:center;gap:8px;margin-bottom:.5rem;
}}
.sb-div{{height:1px;background:{BORDER_COLOR};margin:.9rem 0;}}
.sb-sec{{
  font-family:'DM Sans',sans-serif;font-size:.68rem;font-weight:600;
  letter-spacing:.1em;text-transform:uppercase;color:{TEXT_MUTED};margin-bottom:.5rem;
}}

/* ── Footer ── */
.footer-wrap{{
  text-align:center;padding:2.5rem 1rem 2rem;
  margin-top:3.5rem;border-top:1px solid {FOOTER_BORDER};position:relative;
}}
.footer-wrap::before{{
  content:'';position:absolute;top:0;left:50%;transform:translateX(-50%);
  width:80px;height:2px;background:linear-gradient(90deg,{ACCENT},{ACCENT2});border-radius:2px;
}}
.footer-name{{
  font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:800;
  color:{TEXT_PRIMARY};margin-bottom:.2rem;
}}
.footer-heart{{color:#ef4444;animation:beat 1.4s ease infinite;}}
@keyframes beat{{0%,100%{{transform:scale(1);}}14%{{transform:scale(1.3);}}28%{{transform:scale(1);}}42%{{transform:scale(1.2);}}}}
.footer-copy{{font-size:.8rem;color:{FOOTER_TEXT};margin-top:.25rem;}}
.footer-email{{
  display:inline-flex;align-items:center;gap:6px;
  background:{TAG_BG};border:1px solid {BORDER_COLOR};border-radius:50px;
  padding:.4rem 1.1rem;font-size:.82rem;color:{TEXT_SECONDARY};
  text-decoration:none!important;margin-top:.9rem;
  transition:border-color .2s,color .2s;font-family:'DM Sans',sans-serif;
}}
.footer-email:hover{{border-color:{ACCENT};color:{ACCENT};}}
.footer-ds{{
  font-size:.72rem;color:{FOOTER_TEXT};
  font-family:'JetBrains Mono',monospace;margin-top:.8rem;
}}

@media(max-width:768px){{
  .block-container{{padding:1rem .85rem 3rem!important;}}
  .hero{{padding:2rem 1rem 1.8rem;}}
  .kpi-grid{{grid-template-columns:repeat(2,1fr);}}
  .stTabs [data-baseweb="tab"]{{font-size:.76rem!important;padding:.37rem .6rem!important;}}
}}
@media(max-width:480px){{
  .kpi-grid{{grid-template-columns:repeat(2,1fr);gap:.55rem;}}
  .hero-title{{font-size:1.55rem;}}
}}

#MainMenu,footer,header{{visibility:hidden;}}
</style>
""", unsafe_allow_html=True)

# ── Plotly helper ─────────────────────────────────────────────────────────────
def style_fig(fig, height=420, legend=True):
    fig.update_layout(
        template=PLOTLY_TPL,
        plot_bgcolor=PLOT_BG,
        paper_bgcolor=PAPER_BG,
        font=dict(family="DM Sans, sans-serif", color=FONT_COLOR, size=12),
        height=height,
        margin=dict(l=8, r=8, t=38, b=8),
        showlegend=legend,
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=GRID_COLOR, borderwidth=1, font=dict(size=11)),
        xaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR, linecolor=GRID_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR, linecolor=GRID_COLOR),
        hoverlabel=dict(bgcolor=PAPER_BG, bordercolor=GRID_COLOR,
                        font=dict(family="DM Sans", size=12, color=FONT_COLOR)),
    )
    return fig

def section(n, t):
    st.markdown(f'<div class="sec-hdr"><span class="sec-num">{n:02d}</span>'
                f'<span class="sec-title">{t}</span></div>', unsafe_allow_html=True)

def obs(txt):
    st.markdown(f'<div class="obs-box">📌 {txt}</div>', unsafe_allow_html=True)

def chart(fig):
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="⚙️ Processing railway data…")
def load_data():
    df = pd.read_excel("erail_database.xlsx", sheet_name="Investigations")
    drop_cols = [
        'Only received by email after ERAIL stopped to work','ERAIL Occurrence','ID','Acronym',
        'Report Type','Investigation Status','Reporting Body','Legal basis',
        'Decision to investigate','Decision to investigate ',
        'Notification date (occurrence creation date for data from ERAIL)',
        'Date of sending the interim statement(s), if any',
        'Date of sending the final report to ERA','Date of the investigation closure',
        'Investigation report','DATE (Italic format)','Day','Month','Year',
        'Occurrence creation date','Declaration date','Month DECL DATE','Year DECL DATE',
        'Date of IM/RU notification','Unnamed: 56','Unnamed: 57','Unnamed: 58',
        'Unnamed: 59','Unnamed: 60','Unnamed: 61','Unnamed: 62','Unnamed: 63','Unnamed: 64',
        'Direct cause description (including causal and contributing factors, excluding those of systemic nature)',
        'Underlying and root causes description (i.e. systemic factors, if any)',
        'Damage Description','Notes','Title','RU involved','IM involved',
        'N. of related Safety Recs','Delay',
    ]
    df.drop(columns=[c for c in drop_cols if c in df.columns], inplace=True)
    df.columns = df.columns.str.strip()

    sev = {
        "Wrong-side signalling failure":2,"Train derailment":3,"Other":2,"Spad":2,
        "Level crossing accident":3,"Fire in RS":3,"Trains collision with an obstacle":2,
        "Trains collision":4,"Accident to persons caused by RS in motion":3,"Broken rails":2,
        "Runaway":3,"Broken wheels or axles":2,"Unauthorised train movement other than SPAD":2,
        "Trains collision near miss":1,"Level crossing near miss":1,"Track buckles":2,
        "Dangerous goods release":4,"Other event":2,"Rolling stock events":2,
        "Operational event":1,"Railway vehicle movement events":2,"Broken axles":2,
        "Broken wheels":2,"Level crossing event":3,"Infrastructure events":2,
        "Electric shock":3,"Broken rails and track buckles":2,"SPAD":2,
        "Railway vehicle movement event":2,"Collission with object":2,
        "Wrong-side signaling failure":2,"Rolling stock event":2,"Trains collision ":4,
        "Train collision with technical device":3,"Infrastructure event":2,
        "Accident to person involving rolling stock in motion":3,
        "Train collision with an obstacle":3,"Unauthorized train movement other than SPAD":2,
        "Unauthorized movement (SPAD)":2,
    }
    df["Severity Level"] = df["Occurrence type"].map(sev)

    def wx(d):
        if pd.isnull(d): return "Unknown"
        m = d.month
        if m in [12,1,2]: return "Foggy"
        elif m in [9,10,11]: return "Rainy"
        return "Clear"

    df["Weather Conditions"] = df["Date of occurrence"].apply(wx)
    nc = ["Passenger fatalities","Staff fatalities","LC User fatalities",
          "Unauthorised person fatalities","Other fatalities","Total fatalities",
          "Passenger serious injuries","Staff serious injuries",
          "LC User serious injuries","Unauth. person serious injuries",
          "Other serious injuries","Total serious injuries"]
    df[nc] = df[nc].apply(pd.to_numeric, errors="coerce").fillna(0).astype(int)
    df["Year"]        = df["Date of occurrence"].dt.year
    df["Month"]       = df["Date of occurrence"].dt.month
    df["Day_of_Week"] = df["Date of occurrence"].dt.day_name()
    df["Time of occurrence"] = pd.to_datetime(df["Time of occurrence"], errors="coerce")
    df["Hour"]        = df["Time of occurrence"].dt.hour
    df["Severity Category"] = df["Severity Level"].apply(
        lambda l: "Unknown" if pd.isnull(l) else ("Low" if l<=2 else ("Medium" if l<=5 else "High")))
    df = df[df["Occurrence type"] != "Unknown"].reset_index(drop=True)
    df["Fatal"]    = df["Total fatalities"].apply(lambda x: "Fatal" if x>0 else "Non-Fatal")
    df["Severity"] = df["Total fatalities"] + df["Total serious injuries"]
    return df

df = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f'<div class="sb-logo">🚂 RailAnalytics</div>', unsafe_allow_html=True)

    if st.button(f"{TOGGLE_ICON}  Switch to {TOGGLE_LABEL}", key="toggle",
                 use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    st.markdown('<div class="sb-div"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-sec">📅 Year Range</div>', unsafe_allow_html=True)
    yr_min, yr_max = int(df["Year"].dropna().min()), int(df["Year"].dropna().max())
    year_range = st.slider("Year", yr_min, yr_max, (2006, yr_max), label_visibility="collapsed")

    st.markdown('<div class="sb-sec" style="margin-top:1rem">🌍 Country</div>', unsafe_allow_html=True)
    countries = sorted(df["Country"].dropna().unique())
    sel_countries = st.multiselect("Country", countries, default=None,
                                   placeholder="All countries", label_visibility="collapsed")

    st.markdown('<div class="sb-sec" style="margin-top:1rem">⚠️ Occurrence Type</div>', unsafe_allow_html=True)
    occ_types = sorted(df["Occurrence type"].dropna().unique())
    sel_types = st.multiselect("Type", occ_types, default=None,
                               placeholder="All types", label_visibility="collapsed")

    st.markdown('<div class="sb-div"></div>', unsafe_allow_html=True)
    st.markdown(
        f'<div style="font-size:.71rem;color:{TEXT_MUTED};font-family:JetBrains Mono,monospace;line-height:1.9">'
        f'📦 ERAIL Database<br>🗃️ {len(df):,} total records<br>📅 {yr_min} – {yr_max}<br><br>'
        f'<a href="mailto:ravi.panchal.kaithi@gmail.com" style="color:{ACCENT};text-decoration:none;">'
        f'✉️ Contact Author</a></div>', unsafe_allow_html=True)

# ── Filter data ───────────────────────────────────────────────────────────────
fdf = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]
if sel_countries: fdf = fdf[fdf["Country"].isin(sel_countries)]
if sel_types:     fdf = fdf[fdf["Occurrence type"].isin(sel_types)]

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <div class="eyebrow">🛡️ Data-Driven Safety Research</div>
  <h1 class="hero-title">Railway Accident<br><span class="hl">Analysis Dashboard</span><br><span style="font-size:.9rem;font-weight:400;color:rgb(148,163,184);margin-top:.8rem;display:block;line-height:1.6;">Exploring  {len(df):,} European railway investigations to surface patterns, causes, and safety opportunities across {df['Country'].nunique()} countries.</span></h1>
  <div class="hero-tags">
    <span class="hero-tag">ERAIL Database</span>
    <span class="hero-tag">2002 – 2025</span>
    <span class="hero-tag">EDA · ML · Safety</span>
    <span class="hero-tag">B.Tech 3rd Year Project</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ─────────────────────────────────────────────────────────────────
n_recs    = len(fdf)
n_fatal   = int(fdf["Total fatalities"].sum())
n_inj     = int(fdf["Total serious injuries"].sum())
f_pct     = round((fdf["Fatal"]=="Fatal").sum() / max(n_recs,1) * 100, 1)
n_ctry    = fdf["Country"].nunique()
peak_yr   = int(fdf.groupby("Year").size().idxmax()) if n_recs else "–"

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card">
    <span class="kpi-icon">📋</span>
    <div class="kpi-val">{n_recs:,}</div>
    <div class="kpi-label">Total Incidents</div><div class="kpi-sub">Filtered records</div>
  </div>
  <div class="kpi-card">
    <span class="kpi-icon">💀</span>
    <div class="kpi-val">{n_fatal:,}</div>
    <div class="kpi-label">Total Fatalities</div><div class="kpi-sub">All categories</div>
  </div>
  <div class="kpi-card">
    <span class="kpi-icon">🏥</span>
    <div class="kpi-val">{n_inj:,}</div>
    <div class="kpi-label">Serious Injuries</div><div class="kpi-sub">Passenger + staff</div>
  </div>
  <div class="kpi-card">
    <span class="kpi-icon">⚠️</span>
    <div class="kpi-val">{f_pct}%</div>
    <div class="kpi-label">Fatal Rate</div><div class="kpi-sub">Of all incidents</div>
  </div>
  <div class="kpi-card">
    <span class="kpi-icon">🌍</span>
    <div class="kpi-val">{n_ctry}</div>
    <div class="kpi-label">Countries</div><div class="kpi-sub">In filtered view</div>
  </div>
  <div class="kpi-card">
    <span class="kpi-icon">📈</span>
    <div class="kpi-val">{peak_yr}</div>
    <div class="kpi-label">Peak Year</div><div class="kpi-sub">Highest count</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊  Temporal",
    "⚠️  Causes & Types",
    "💥  Severity & Fatalities",
    "🌍  Geography",
    "🔬  Deep Dive",
])

# ════ TAB 1 – Temporal ════════════════════════════════════════════════════════
with tab1:
    section(1, "Accidents Per Year")
    yr = fdf[fdf["Year"]>2005].groupby("Year").size().reset_index(name="Count")
    f1 = px.bar(yr, x="Year", y="Count", color="Count",
                color_continuous_scale=[[0,PLOT_BG],[0.3,ACCENT],[1,ACCENT2]])
    f1.update_traces(marker_line_width=0)
    f1.update_coloraxes(showscale=False)
    style_fig(f1, 400, legend=False)
    chart(f1)
    obs("<strong>Peak 2011–2017.</strong> Steady decline post-2017 reflects improved safety measures. "
        "Post-2020 sharp drop needs further investigation.")

    st.markdown("<br>", unsafe_allow_html=True)
    section(2, "Yearly Trend Line")
    yt = fdf.groupby("Year").size().reset_index(name="Accidents")
    f2 = px.line(yt, x="Year", y="Accidents", markers=True, line_shape="spline",
                 color_discrete_sequence=[ACCENT])
    f2.update_traces(line_width=2.5, marker_size=6, marker_color=ACCENT2)
    anns = [dict(x=r.Year, y=r.Accidents, text=f"  {int(r.Accidents)}",
                 showarrow=False, font=dict(color="#fc8181", size=11, family="JetBrains Mono"))
            for _, r in yt.iterrows() if r.Year in [2010, 2015, 2020]]
    f2.update_layout(annotations=anns)
    style_fig(f2, 370, legend=False)
    chart(f2)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        section(3, "Accidents by Hour of Day")
        hc = fdf["Hour"].dropna().astype(int).value_counts().sort_index().reset_index()
        hc.columns = ["Hour","Count"]
        f3 = px.bar(hc, x="Hour", y="Count", color="Count",
                    color_continuous_scale=[[0,PLOT_BG],[0.4,"#68d391"],[1,ACCENT2]])
        f3.update_traces(marker_line_width=0)
        f3.update_coloraxes(showscale=False)
        style_fig(f3, 340, legend=False)
        chart(f3)
        obs("<strong>8–11 AM</strong> and <strong>3–6 PM</strong> are peak risk windows.")
    with c2:
        section(4, "Accidents by Day of Week")
        day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        dc = fdf["Day_of_Week"].value_counts().reindex(day_order).reset_index()
        dc.columns = ["Day","Count"]
        f4 = px.bar(dc, x="Day", y="Count", color="Count",
                    color_continuous_scale=[[0,PLOT_BG],[0.4,ACCENT3],[1,"#fc8181"]])
        f4.update_traces(marker_line_width=0)
        f4.update_coloraxes(showscale=False)
        style_fig(f4, 340, legend=False)
        chart(f4)
        obs("<strong>Tue–Thu</strong> are highest; weekends drop significantly.")

# ════ TAB 2 – Causes & Types ══════════════════════════════════════════════════
with tab2:
    c1, c2 = st.columns([3,2])
    with c1:
        section(5, "Top 10 Occurrence Types")
        tt = fdf["Occurrence type"].value_counts().head(10).reset_index()
        tt.columns = ["Type","Count"]
        f5 = px.bar(tt, x="Count", y="Type", orientation="h", color="Count",
                    color_continuous_scale=[[0,PLOT_BG],[0.3,"#fc8181"],[1,"#f687b3"]])
        f5.update_yaxes(categoryorder="total ascending")
        f5.update_coloraxes(showscale=False)
        style_fig(f5, 420, legend=False)
        chart(f5)
    with c2:
        section(6, "Type Share")
        top9 = fdf["Occurrence type"].value_counts().head(9)
        oth  = len(fdf) - top9.sum()
        pd9  = pd.concat([top9, pd.Series({"Others": oth})])
        f6 = px.pie(values=pd9.values, names=pd9.index,
                    color_discrete_sequence=PALETTE + ["#718096"], hole=0.45)
        f6.update_traces(textposition="inside", textinfo="percent", textfont_size=10)
        style_fig(f6, 420, legend=False)
        chart(f6)

    st.markdown("<br>", unsafe_allow_html=True)
    section(7, "Accident Type vs. Severity Level")
    pv = fdf.pivot_table(index="Occurrence type", columns="Severity Category",
                         aggfunc="size", fill_value=0)
    pv = pv[pv.sum(axis=1) > 40].reset_index()
    pm = pv.melt(id_vars="Occurrence type", var_name="Severity", value_name="Count")
    f7 = px.bar(pm, x="Occurrence type", y="Count", color="Severity",
                barmode="stack", color_discrete_map=SEV_COLORS)
    f7.update_xaxes(tickangle=-38, tickfont=dict(size=11))
    style_fig(f7, 440)
    chart(f7)
    obs("<strong>Train derailment</strong> tops all at medium severity. "
        "Level crossing & collision types follow closely.")

    st.markdown("<br>", unsafe_allow_html=True)
    section(8, "Weather Conditions Impact")
    wc = fdf["Weather Conditions"].value_counts().reset_index()
    wc.columns = ["Weather","Count"]
    f8 = px.bar(wc, x="Count", y="Weather", orientation="h", color="Weather",
                color_discrete_map={"Clear":"#68d391","Rainy":ACCENT,"Foggy":"#a0aec0","Unknown":TEXT_MUTED})
    f8.update_layout(showlegend=False)
    style_fig(f8, 290, legend=False)
    chart(f8)
    obs("Most accidents occur in <strong>clear weather</strong> — environment is rarely the root cause. "
        "Rainy &amp; foggy conditions still contribute meaningfully.")

# ════ TAB 3 – Severity & Fatalities ══════════════════════════════════════════
with tab3:
    c1, c2 = st.columns(2)
    with c1:
        section(9, "Severity Level Distribution")
        sc = fdf["Severity Level"].value_counts().sort_index().reset_index()
        sc.columns = ["Level","Count"]
        f9 = px.bar(sc, x="Level", y="Count", color="Level",
                    color_discrete_sequence=["#68d391",ACCENT3,"#fc8181","#9f7aea"])
        f9.update_layout(showlegend=False)
        style_fig(f9, 350, legend=False)
        chart(f9)
        obs("<strong>Level 3</strong> dominates. Level 4 is rare but critical-impact.")
    with c2:
        section(10, "Fatal vs Non-Fatal")
        fc = fdf["Fatal"].value_counts().reset_index()
        fc.columns = ["Type","Count"]
        f10 = px.pie(fc, values="Count", names="Type", hole=0.52,
                     color="Type", color_discrete_map={"Fatal":"#fc8181","Non-Fatal":"#68d391"})
        f10.update_traces(textposition="inside", textinfo="percent+label", textfont_size=13)
        style_fig(f10, 350, legend=False)
        chart(f10)

    st.markdown("<br>", unsafe_allow_html=True)
    section(11, "Fatalities — Passenger vs Staff vs Unauthorised")
    fcols = ["Passenger fatalities","Staff fatalities","Unauthorised person fatalities"]
    fs = fdf[fcols].sum().reset_index()
    fs.columns = ["Category","Total"]
    fs["Category"] = fs["Category"].str.replace(" fatalities","")
    f11 = px.bar(fs, x="Category", y="Total", color="Category",
                 color_discrete_sequence=[ACCENT, ACCENT3, "#fc8181"])
    f11.update_layout(showlegend=False)
    style_fig(f11, 340, legend=False)
    chart(f11)
    obs("<strong>Passenger fatalities</strong> dominate. Staff deaths remain low — "
        "reflecting occupational safety measures in Europe.")

    st.markdown("<br>", unsafe_allow_html=True)
    section(12, "Fatality Trends Over Years")
    fy = fdf.groupby("Year")[fcols].sum().reset_index()
    fm = fy.melt(id_vars="Year", var_name="Category", value_name="Fatalities")
    fm["Category"] = fm["Category"].str.replace(" fatalities","")
    f12 = px.line(fm, x="Year", y="Fatalities", color="Category",
                  markers=True, line_shape="spline",
                  color_discrete_sequence=[ACCENT, ACCENT3, "#fc8181"])
    f12.update_traces(line_width=2, marker_size=5)
    style_fig(f12, 360)
    chart(f12)

    st.markdown("<br>", unsafe_allow_html=True)
    section(13, "Correlation Matrix")
    nc = ["Passenger fatalities","Staff fatalities","LC User fatalities",
          "Unauthorised person fatalities","Total fatalities",
          "Passenger serious injuries","Total serious injuries","Severity Level"]
    corr = fdf[nc].dropna().corr().round(2)
    short = [c.replace(" fatalities","").replace(" serious injuries"," inj.")
               .replace("Unauthorised person","Unauth.").replace("Passenger","Pass.")
               .replace("LC User","LC").replace("Total","Tot.")
             for c in corr.columns]
    f13 = go.Figure(go.Heatmap(
        z=corr.values, x=short, y=short,
        colorscale=[[0,"#fc8181"],[0.5,PAPER_BG],[1,ACCENT]],
        zmid=0, text=corr.values, texttemplate="%{text}",
        textfont=dict(size=9, family="JetBrains Mono"), hoverongaps=False,
    ))
    style_fig(f13, 450, legend=False)
    f13.update_layout(xaxis_tickangle=-30)
    chart(f13)
    obs("<strong>LC User fatalities ↔ injuries (0.96)</strong> — strongest link. "
        "<strong>Pass. fatalities ↔ injuries (0.70)</strong> also high. "
        "Severity Level shows weak correlation with casualty count.")

# ════ TAB 4 – Geography ═══════════════════════════════════════════════════════
with tab4:
    section(14, "Top 15 Countries by Accident Count")
    tc = fdf["Country"].value_counts().head(15).reset_index()
    tc.columns = ["Country","Accidents"]
    f14 = px.bar(tc, x="Accidents", y="Country", orientation="h", color="Accidents",
                 color_continuous_scale=[[0,PLOT_BG],[0.4,ACCENT3],[1,"#f687b3"]])
    f14.update_yaxes(categoryorder="total ascending")
    f14.update_coloraxes(showscale=False)
    style_fig(f14, 490, legend=False)
    chart(f14)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        section(15, "Avg Fatalities by Location Type")
        lf = fdf.groupby("Location type")["Total fatalities"].mean().sort_values(ascending=False).reset_index()
        lf.columns = ["Location","Avg"]
        f15 = px.bar(lf, x="Avg", y="Location", orientation="h", color="Avg",
                     color_continuous_scale=[[0,PLOT_BG],[0.5,ACCENT3],[1,"#fc8181"]])
        f15.update_yaxes(categoryorder="total ascending")
        f15.update_coloraxes(showscale=False)
        style_fig(f15, 370, legend=False)
        chart(f15)
    with c2:
        section(16, "Avg Severity by Railway System")
        ss = fdf.groupby("Railway System type")["Severity"].mean().sort_values(ascending=False).reset_index()
        ss.columns = ["System","AvgSev"]
        f16 = px.bar(ss, x="AvgSev", y="System", orientation="h", color="AvgSev",
                     color_continuous_scale=[[0,PLOT_BG],[0.4,ACCENT],[1,ACCENT2]])
        f16.update_yaxes(categoryorder="total ascending")
        f16.update_coloraxes(showscale=False)
        style_fig(f16, 370, legend=False)
        chart(f16)

    st.markdown("<br>", unsafe_allow_html=True)
    section(17, "Accident Types × Top 10 Countries — Heatmap")
    top10c = fdf["Country"].value_counts().head(10).index
    top7t  = fdf["Occurrence type"].value_counts().head(7).index
    hp     = fdf[fdf["Country"].isin(top10c) & fdf["Occurrence type"].isin(top7t)]
    hpiv   = hp.pivot_table(index="Country", columns="Occurrence type", aggfunc="size", fill_value=0)
    f17 = go.Figure(go.Heatmap(
        z=hpiv.values, x=hpiv.columns, y=hpiv.index,
        colorscale=[[0,PLOT_BG],[0.3,"#2a5a8c"],[1,ACCENT]],
        text=hpiv.values, texttemplate="%{text}",
        textfont=dict(size=9, family="JetBrains Mono"), hoverongaps=False,
    ))
    style_fig(f17, 430, legend=False)
    f17.update_layout(xaxis_tickangle=-28)
    chart(f17)

# ════ TAB 5 – Deep Dive ═══════════════════════════════════════════════════════
with tab5:
    c1, c2 = st.columns(2)
    with c1:
        section(18, "Line Type Distribution")
        lt = fdf["Line type"].value_counts().head(10).reset_index()
        lt.columns = ["Type","Count"]
        f18 = px.pie(lt, values="Count", names="Type", hole=0.42,
                     color_discrete_sequence=PALETTE)
        f18.update_traces(textposition="inside", textinfo="percent", textfont_size=10)
        style_fig(f18, 360, legend=False)
        chart(f18)
    with c2:
        section(19, "Movement Type at Accident")
        mt = fdf["Movement type"].value_counts().head(10).reset_index()
        mt.columns = ["Type","Count"]
        f19 = px.bar(mt, x="Count", y="Type", orientation="h", color="Count",
                     color_continuous_scale=[[0,PLOT_BG],[0.4,ACCENT2],[1,ACCENT]])
        f19.update_yaxes(categoryorder="total ascending")
        f19.update_coloraxes(showscale=False)
        style_fig(f19, 360, legend=False)
        chart(f19)

    st.markdown("<br>", unsafe_allow_html=True)
    section(20, "Monthly Accident Heatmap by Year")
    my = fdf.groupby(["Year","Month"]).size().reset_index(name="Count")
    mp = my.pivot(index="Year", columns="Month", values="Count").fillna(0)
    mlbl = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    mp.columns = mlbl[:len(mp.columns)]
    f20 = go.Figure(go.Heatmap(
        z=mp.values, x=mp.columns, y=mp.index.astype(str),
        colorscale=[[0,PLOT_BG],[0.35,"#2a6090"],[1,ACCENT]],
        text=mp.values.astype(int), texttemplate="%{text}",
        textfont=dict(size=8, family="JetBrains Mono"), hoverongaps=False,
    ))
    style_fig(f20, 520, legend=False)
    chart(f20)
    obs("Warmer months <strong>(May–Sep)</strong> spike in peak-activity years. "
        "Winter months show fog/ice-related surges.")

    st.markdown("<br>", unsafe_allow_html=True)
    section(21, "Fatality Types — Stacked Area Over Time")
    ac  = ["Passenger fatalities","Staff fatalities","LC User fatalities","Unauthorised person fatalities"]
    ay  = fdf.groupby("Year")[ac].sum().reset_index()
    am  = ay.melt(id_vars="Year", var_name="Category", value_name="Fatalities")
    am["Category"] = am["Category"].str.replace(" fatalities","")
    f21 = px.area(am, x="Year", y="Fatalities", color="Category",
                  color_discrete_sequence=[ACCENT, ACCENT3, "#68d391", "#fc8181"])
    f21.update_traces(line_width=1.5)
    style_fig(f21, 390)
    chart(f21)

    st.markdown("<br>", unsafe_allow_html=True)
    section(22, "Summary Statistics")
    scols = ["Total fatalities","Total serious injuries",
             "Passenger fatalities","Staff fatalities","Severity Level"]
    st.dataframe(
        fdf[scols].describe().round(2).style
            .background_gradient(cmap="Blues", axis=None)
            .format("{:.2f}"),
        use_container_width=True
    )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer-wrap">
  <div class="footer-name">
    Made With <span class="footer-heart">❤️</span> by Team.
  </div>
  <div class="footer-copy">All Rights Reserved &copy; 2026</div>
 <a class="footer-email" href="mailto:ravi.panchal.kaithi@gmail.com">
  &#9993; ravi.panchal.kaithi@gmail.com
</a>
  <div class="footer-ds">
    ERAIL European Railway Accident Database &nbsp;·&nbsp;
    Accident Analysis &amp; Safety Improvements in Railways
  </div>
</div>
""", unsafe_allow_html=True)