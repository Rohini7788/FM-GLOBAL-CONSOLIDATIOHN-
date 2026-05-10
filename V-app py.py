import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FM · Operations & NPS Insights",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

LOGO_URI = "data:image/png;base64,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"

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

/* ── Base ── */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #0b0d14 !important;
    color: #d4d7e8 !important;
}
[data-testid="stAppViewContainer"] > .main { background: #0b0d14 !important; }
[data-testid="stHeader"] { background: transparent !important; display: none; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0e1018 !important;
    border-right: 1px solid #1c1f30 !important;
    padding-top: 0 !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }

.sidebar-logo-wrap {
    padding: 20px 20px 24px;
    border-bottom: 1px solid #1c1f30;
    margin-bottom: 16px;
    background: #0e1018;
}
.sidebar-logo-wrap img { width: 100%; max-width: 160px; filter: brightness(1.1); }

[data-testid="stSidebar"] .stRadio label {
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 13px !important;
    color: #6b7194 !important;
    padding: 6px 0 !important;
}
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] input:checked + div {
    background: rgba(99,130,255,0.15) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-thumb { background: #252840; border-radius: 2px; }
::-webkit-scrollbar-track { background: transparent; }

/* ── Main content ── */
.block-container {
    padding: 0 32px 48px !important;
    max-width: 100% !important;
}

/* ── Topbar ── */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 0 18px;
    border-bottom: 1px solid #181b28;
    margin-bottom: 36px;
}
.topbar-logo img { height: 36px; filter: brightness(1.15); }
.topbar-pill {
    display: flex; align-items: center; gap: 8px;
    background: #131623; border: 1px solid #1e2238;
    border-radius: 20px; padding: 6px 16px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px; color: #4a5178;
    letter-spacing: 0.06em; text-transform: uppercase;
}
.topbar-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #6382ff; animation: blink 2s infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* ── Page header ── */
.page-hero { padding: 8px 0 32px; }
.page-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px; font-weight: 500;
    letter-spacing: 0.14em; text-transform: uppercase;
    color: #3d4470; margin-bottom: 12px;
}
.page-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 42px !important; font-weight: 800 !important;
    letter-spacing: -0.035em !important; line-height: 1.05 !important;
    color: #ffffff !important; margin: 0 0 14px !important; padding: 0 !important;
}
.page-title .hi { color: #6382ff; }
.page-desc {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 15px; color: #5a6080; line-height: 1.65;
    max-width: 580px; font-weight: 300;
}

/* ── KPI cards ── */
.kpi-row { display: grid; grid-template-columns: repeat(3,1fr); gap: 14px; margin-bottom: 32px; }
.kpi-card {
    background: #0e1018; border: 1px solid #1a1d2e;
    border-radius: 10px; padding: 24px 22px; position: relative; overflow: hidden;
    transition: border-color .2s, transform .2s;
}
.kpi-card:hover { border-color: #272a42; transform: translateY(-2px); }
.kpi-card::after {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
}
.kpi-card.c-blue::after  { background: linear-gradient(90deg,transparent,#6382ff,transparent); }
.kpi-card.c-red::after   { background: linear-gradient(90deg,transparent,#ff5f6d,transparent); }
.kpi-card.c-amber::after { background: linear-gradient(90deg,transparent,#ffb347,transparent); }

.kpi-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px; letter-spacing: 0.1em; text-transform: uppercase;
    color: #363a58; margin-bottom: 10px;
}
.kpi-num {
    font-family: 'Syne', sans-serif;
    font-size: 40px; font-weight: 800; letter-spacing: -0.04em;
    color: #ffffff; line-height: 1; margin-bottom: 10px;
}
.kpi-badge {
    display: inline-flex; align-items: center; gap: 4px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px; font-weight: 500; padding: 3px 8px; border-radius: 4px;
}
.kpi-badge.neg { background: rgba(255,95,109,0.1); color: #ff5f6d; }
.kpi-badge.neu { background: rgba(99,130,255,0.1); color: #6382ff; }

/* ── Section ── */
.section-wrap { margin-bottom: 40px; }
.section-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px; letter-spacing: 0.16em; text-transform: uppercase;
    color: #2e3150; margin-bottom: 8px;
}
.section-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 22px !important; font-weight: 700 !important;
    color: #c8cbdf !important; letter-spacing: -0.025em !important;
    margin: 0 0 6px !important; padding: 0 !important;
}
.section-sub {
    font-size: 13px; color: #424670; font-weight: 300;
    line-height: 1.6; max-width: 560px; margin-bottom: 20px;
}

/* ── Chart card ── */
.chart-wrap {
    background: #0e1018; border: 1px solid #181b28;
    border-radius: 10px; overflow: hidden;
}

/* ── Callout boxes ── */
.callout {
    display: flex; gap: 14px; align-items: flex-start;
    background: #0d1019; border: 1px solid #1c1f32;
    border-radius: 8px; padding: 16px 18px;
    margin: 16px 0; font-size: 13px; line-height: 1.6; color: #8a8fb0;
}
.callout.amber { border-left: 3px solid #ffb347; }
.callout.blue  { border-left: 3px solid #6382ff; }
.callout.green { border-left: 3px solid #4fd4a8; }
.callout .ci { font-size: 16px; margin-top: 1px; flex-shrink: 0; }

/* ── Roadmap cards ── */
.road-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 14px; margin-top: 20px; }
.road-card {
    background: #0e1018; border: 1px solid #181b28; border-radius: 10px; padding: 24px 22px;
}
.road-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase;
    padding: 4px 10px; border-radius: 4px; display: inline-block; margin-bottom: 14px;
}
.road-tag.q  { background: rgba(79,212,168,0.1); color: #4fd4a8; }
.road-tag.op { background: rgba(99,130,255,0.1); color: #6382ff; }
.road-tag.lt { background: rgba(167,139,250,0.1); color: #a78bfa; }
.road-h {
    font-family: 'Syne', sans-serif; font-size: 15px; font-weight: 700;
    color: #c8cbdf; margin-bottom: 14px; letter-spacing: -0.02em;
}
.road-item {
    display: flex; gap: 10px; font-size: 12px; color: #55597a;
    line-height: 1.55; margin-bottom: 9px; align-items: flex-start;
}
.road-dot { width: 4px; height: 4px; background: #2a2d46; border-radius: 50%; margin-top: 6px; flex-shrink: 0; }

/* ── Success stripe ── */
.success-stripe {
    background: linear-gradient(135deg, rgba(79,212,168,0.05) 0%, rgba(99,130,255,0.05) 100%);
    border: 1px solid rgba(79,212,168,0.15); border-radius: 10px;
    padding: 20px 24px; margin-top: 28px;
    font-family: 'IBM Plex Sans', sans-serif; font-size: 14px;
    color: #4fd4a8; display: flex; align-items: center; gap: 14px;
}
.success-stripe strong { color: #7ef0cc; }

/* ── Divider ── */
.slim-divider {
    height: 1px; margin: 36px 0;
    background: linear-gradient(90deg,transparent,#181b28 20%,#181b28 80%,transparent);
}

/* ── Sidebar nav override ── */
[data-testid="stSidebar"] h1 {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 10px !important; letter-spacing: 0.14em !important;
    text-transform: uppercase !important; color: #2e3150 !important;
    margin-bottom: 8px !important; font-weight: 500 !important;
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# ─── DATA LOADING ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    orders = pd.read_csv('orders.csv')
    nps = pd.read_csv('nps.csv').dropna(subset=['order_id'])
    hub_perf = pd.read_csv('hub_performance.csv').dropna(subset=['hub_id'])
    courier_perf = pd.read_csv('courier_performance.csv').dropna(subset=['courier_partner'])
    customers = pd.read_csv('customers.csv').dropna(subset=['customer_id'])
    complaints = pd.read_csv('complaints.csv').dropna(subset=['order_id'])

    orders['order_date'] = pd.to_datetime(orders['order_date'])
    orders['promised_date'] = pd.to_datetime(orders['promised_date'])
    orders['delivery_date'] = pd.to_datetime(orders['delivery_date'])
    orders['delivery_delay'] = (orders['delivery_date'] - orders['promised_date']).dt.days
    orders['is_late'] = orders['delivery_delay'] > 0

    nps_orders = nps.merge(orders, on='order_id', how='left', suffixes=('_nps', '_ord'))

    def categorize_nps(score):
        if score >= 9: return 'Promoter'
        elif score >= 7: return 'Passive'
        else: return 'Detractor'
    nps_orders['nps_cat'] = nps_orders['score'].apply(categorize_nps)

    return orders, nps_orders, hub_perf, courier_perf, customers, complaints

orders, nps_orders, hub_perf, courier_perf, customers, complaints = load_data()

# ─── METRICS ──────────────────────────────────────────────────────────────────
total_responses = len(nps_orders)
promoters = (nps_orders['nps_cat'] == 'Promoter').sum()
detractors = (nps_orders['nps_cat'] == 'Detractor').sum()
nps_score = round(((promoters - detractors) / total_responses) * 100, 2)
otd_rate = round((orders[orders['order_status'] == 'Delivered']['is_late'] == False).mean() * 100, 2)
avg_res_time = round(complaints['resolution_time'].mean(), 2)

# ─── PLOTLY THEME ─────────────────────────────────────────────────────────────
BG = "#0e1018"
GRID = "#181b28"
TEXT = "#55597a"
FONT = "IBM Plex Sans"

def themed(fig, title=""):
    fig.update_layout(
        title=dict(text=title, font=dict(family="Syne", size=13, color="#8a8fb0"), x=0, xanchor='left', pad=dict(l=20, t=16)),
        paper_bgcolor=BG, plot_bgcolor=BG,
        font=dict(family=FONT, color=TEXT, size=11),
        margin=dict(l=16, r=16, t=48, b=16),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)", font=dict(color=TEXT)),
        xaxis=dict(gridcolor=GRID, linecolor=GRID, tickfont=dict(color=TEXT), zeroline=False),
        yaxis=dict(gridcolor=GRID, linecolor=GRID, tickfont=dict(color=TEXT), zeroline=False),
        hoverlabel=dict(bgcolor="#131623", bordercolor="#252840", font=dict(color="#ffffff", family=FONT)),
    )
    return fig

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f'''<div class="sidebar-logo-wrap"><img src="{LOGO_URI}" /></div>''', unsafe_allow_html=True)
    st.markdown("NAVIGATE")
    page = st.radio(
        "", 
        ["Executive Summary", "Logistics Performance", "Regional Deep-Dive", "Strategy & Roadmap"],
        label_visibility="collapsed"
    )

# ─── TOPBAR ───────────────────────────────────────────────────────────────────
st.markdown(f'''
<div class="topbar">
  <div class="topbar-logo"><img src="{LOGO_URI}" /></div>
  <div class="topbar-pill"><div class="topbar-dot"></div>Live · Q4 FY2024</div>
</div>
''', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — EXECUTIVE SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
if page == "Executive Summary":

    st.markdown('''
    <div class="page-hero">
      <div class="page-tag">Executive Summary · Customer Experience</div>
      <h1 class="page-title">The State of <span class="hi">Customer Trust</span></h1>
      <p class="page-desc">A critical disconnect between customer expectations and operational reality. Our current NPS indicates a brand under pressure, primarily driven by delivery failures and courier inconsistencies.</p>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown(f'''
    <div class="kpi-row">
      <div class="kpi-card c-blue">
        <div class="kpi-eyebrow">Net Promoter Score</div>
        <div class="kpi-num">{nps_score}</div>
        <div class="kpi-badge neg">↓ −15% vs Target</div>
      </div>
      <div class="kpi-card c-red">
        <div class="kpi-eyebrow">On-Time Delivery</div>
        <div class="kpi-num">{otd_rate}%</div>
        <div class="kpi-badge neg">↓ −30% vs Industry</div>
      </div>
      <div class="kpi-card c-amber">
        <div class="kpi-eyebrow">Avg. Resolution Time</div>
        <div class="kpi-num">{avg_res_time}<span style="font-size:18px;color:#55597a;font-family:'IBM Plex Sans'"> days</span></div>
        <div class="kpi-badge neu">→ Baseline</div>
      </div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('''
    <div class="section-wrap">
      <div class="section-eyebrow">Breakdown · NPS</div>
      <h2 class="section-title">Sentiment Distribution</h2>
      <p class="section-sub">Understanding the split between promoters, passives, and detractors reveals where recovery efforts should focus.</p>
    </div>
    ''', unsafe_allow_html=True)

    nps_dist = nps_orders['nps_cat'].value_counts(normalize=True).reset_index()
    nps_dist.columns = ['Category', 'Percentage']
    nps_dist['Percentage'] *= 100

    fig_nps = go.Figure(go.Bar(
        x=nps_dist['Category'],
        y=nps_dist['Percentage'],
        marker=dict(
            color=['#ff5f6d' if c == 'Detractor' else '#ffb347' if c == 'Passive' else '#4fd4a8' for c in nps_dist['Category']],
            line=dict(width=0),
        ),
        text=[f"{v:.1f}%" for v in nps_dist['Percentage']],
        textposition='outside',
        textfont=dict(color="#55597a", size=12),
        hovertemplate="<b>%{x}</b><br>%{y:.1f}%<extra></extra>",
    ))
    fig_nps = themed(fig_nps, "NPS Category Distribution")
    fig_nps.update_yaxes(ticksuffix="%")
    fig_nps.update_layout(height=340)

    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig_nps, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — LOGISTICS PERFORMANCE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Logistics Performance":

    st.markdown('''
    <div class="page-hero">
      <div class="page-tag">Analysis · Courier Performance</div>
      <h1 class="page-title">The <span class="hi">Logistics</span> Gap</h1>
      <p class="page-desc">Courier partners show significant variance in reliability. A single underperforming partner can cascade into NPS collapse across an entire region.</p>
    </div>
    ''', unsafe_allow_html=True)

    courier_summary = nps_orders.groupby('courier_partner').agg(
        avg_score=('score', 'mean'),
        late_rate=('is_late', 'mean')
    ).reset_index()

    fig_courier = px.scatter(
        courier_summary, x='late_rate', y='avg_score',
        text='courier_partner', size='late_rate',
        color='avg_score',
        color_continuous_scale=[[0,"#ff5f6d"],[0.5,"#ffb347"],[1,"#4fd4a8"]],
        labels={'late_rate': 'Late Delivery Rate', 'avg_score': 'Avg NPS Score'},
    )
    fig_courier.update_traces(
        textposition='top center',
        textfont=dict(color="#8a8fb0", size=11),
        marker=dict(line=dict(width=0)),
    )
    fig_courier = themed(fig_courier, "Courier Performance: NPS Score vs. Late Delivery Rate")
    fig_courier.update_coloraxes(showscale=False)
    fig_courier.update_layout(height=420)
    fig_courier.update_xaxes(tickformat=".0%")

    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig_courier, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('''
    <div class="callout amber">
      <div class="ci">⚡</div>
      <div><strong style="color:#ffb347">Key Finding:</strong> QuickShip is delivering 100% of orders late in sampled data, directly pulling down NPS scores across every region it serves. Immediate volume reallocation is warranted.</div>
    </div>
    ''', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — REGIONAL DEEP-DIVE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Regional Deep-Dive":

    st.markdown('''
    <div class="page-hero">
      <div class="page-tag">Regional Analysis · Hubs & Cities</div>
      <h1 class="page-title">Regional <span class="hi">Hotspots</span></h1>
      <p class="page-desc">Complaints and operational failures are geographically concentrated. Identifying these nodes unlocks targeted, high-leverage interventions.</p>
    </div>
    ''', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('''
        <div class="section-eyebrow">Distribution</div>
        <h2 class="section-title">Complaints by City</h2>
        ''', unsafe_allow_html=True)

        city_complaints = complaints.merge(orders, on='order_id')['city'].value_counts().reset_index()
        fig_city = go.Figure(go.Pie(
            labels=city_complaints['city'],
            values=city_complaints['count'],
            hole=0.55,
            marker=dict(
                colors=["#6382ff","#ff5f6d","#ffb347","#4fd4a8","#a78bfa","#f472b6"],
                line=dict(color=BG, width=3),
            ),
            textinfo='label+percent',
            textfont=dict(family=FONT, color="#c8cbdf", size=11),
            hovertemplate="<b>%{label}</b><br>%{value} complaints<br>%{percent}<extra></extra>",
        ))
        fig_city = themed(fig_city)
        fig_city.update_layout(height=360, showlegend=False)

        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.plotly_chart(fig_city, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('''
        <div class="section-eyebrow">Hub Ops</div>
        <h2 class="section-title">Hub Operational Integrity</h2>
        ''', unsafe_allow_html=True)

        fig_hub = go.Figure(data=[
            go.Bar(
                name='Failed Attempts', x=hub_perf['city'], y=hub_perf['failed_attempts'],
                marker=dict(color='#ff5f6d', line=dict(width=0)),
                hovertemplate="<b>%{x}</b><br>Failed: %{y}<extra></extra>",
            ),
            go.Bar(
                name='RTO Count', x=hub_perf['city'], y=hub_perf['rto_count'],
                marker=dict(color='#ffb347', line=dict(width=0)),
                hovertemplate="<b>%{x}</b><br>RTO: %{y}<extra></extra>",
            ),
        ])
        fig_hub = themed(fig_hub)
        fig_hub.update_layout(barmode='group', height=360,
            legend=dict(x=0, y=1.15, orientation='h'))

        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.plotly_chart(fig_hub, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('''
    <div class="callout blue">
      <div class="ci">🔍</div>
      <div><strong style="color:#6382ff">Pattern Detected:</strong> Nagpur and Indore show disproportionately high RTO counts and failed delivery attempts — the signature fingerprint of systematic "Fake Delivery Attempt" behaviour by field agents.</div>
    </div>
    ''', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — STRATEGY & ROADMAP
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Strategy & Roadmap":

    st.markdown('''
    <div class="page-hero">
      <div class="page-tag">Strategy · 90-Day Roadmap</div>
      <h1 class="page-title">The Road to <span class="hi">Recovery</span></h1>
      <p class="page-desc">Three horizons of action — from zero-cost volume shifts this week, to structural process reforms, to long-term contractual leverage with courier partners.</p>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('''
    <div class="road-grid">
      <div class="road-card">
        <div class="road-tag q">Immediate · No Cost</div>
        <div class="road-h">Volume & Expectation Fixes</div>
        <div class="road-item"><div class="road-dot"></div><div>Divert high-priority orders from <strong style="color:#c8cbdf">QuickShip</strong> to <strong style="color:#4fd4a8">ShipNow</strong> immediately.</div></div>
        <div class="road-item"><div class="road-dot"></div><div>Increase buffer in 'Promised Date' by 24–48h. Delivering to a longer window beats missing a short one for NPS.</div></div>
      </div>
      <div class="road-card">
        <div class="road-tag op">Operational · Low Cost</div>
        <div class="road-h">Process Integrity</div>
        <div class="road-item"><div class="road-dot"></div><div>Roll out OTP-based delivery in Indore and Nagpur to eliminate Fake Delivery Attempts at the field level.</div></div>
        <div class="road-item"><div class="road-dot"></div><div>Create a VIP complaint queue routing <strong style="color:#c8cbdf">High-Value</strong> customers to senior agents for same-day resolution.</div></div>
      </div>
      <div class="road-card">
        <div class="road-tag lt">Long-Term · Structural</div>
        <div class="road-h">Performance Contracts</div>
        <div class="road-item"><div class="road-dot"></div><div>Shift to pay-per-performance courier contracts with explicit SLA breach penalties written into agreements.</div></div>
        <div class="road-item"><div class="road-dot"></div><div>Quarterly courier scorecards published internally to create competitive accountability between partners.</div></div>
      </div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('''
    <div class="success-stripe">
      <span style="font-size:20px">🎯</span>
      <div>Implementing these three horizons targets an <strong>NPS lift of +20 points within 90 days</strong> — without significant incremental shipping cost. The primary lever is reallocation, not spend.</div>
    </div>
    ''', unsafe_allow_html=True)
