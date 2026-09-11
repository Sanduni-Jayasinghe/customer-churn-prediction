import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import warnings
warnings.filterwarnings('ignore')

# ===============================================
# PAGE CONFIGURATION
# ===============================================
st.set_page_config(
    page_title="Customer Churn Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# SMALL REUSABLE SVG CHART ICON
# ============================================
CHART_ICON_SVG = """
<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="3" y="12" width="4" height="9" rx="1" fill="#ffd200"/>
  <rect x="10" y="7" width="4" height="14" rx="1" fill="#f7971e"/>
  <rect x="17" y="3" width="4" height="18" rx="1" fill="#4f46e5"/>
</svg>
"""

# ============================================
# CUSTOM CSS - PROFESSIONAL DASHBOARD
# ============================================
st.markdown("""
<style>
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29 0%, #1a1a3e 50%, #24243e 100%);
        padding: 0;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    section[data-testid="stSidebar"] .css-1d391kg { padding: 0.5rem 0.8rem; }

    .sidebar-brand {
        text-align: center;
        padding: 1.5rem 0 1.2rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 1.5rem;
    }
    .sidebar-brand .logo { display: flex; justify-content: center; margin-bottom: 0.3rem; }
    .sidebar-brand h2 { color: #ffffff; margin: 0.3rem 0 0 0; font-weight: 700; font-size: 1.2rem; letter-spacing: 0.5px; }
    .sidebar-brand h2 span {
        background: linear-gradient(90deg, #f7971e, #ffd200);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }
    .sidebar-brand p { color: #6b7280; font-size: 0.7rem; margin: 0.1rem 0 0 0; letter-spacing: 1px; }

    .stRadio > div { gap: 0.3rem; }
    .stRadio label {
        display: flex !important; align-items: center !important; gap: 0.9rem !important;
        padding: 0.9rem 1.2rem !important; margin: 0.15rem 0 !important; border-radius: 10px !important;
        background: transparent !important; transition: all 0.25s ease !important; cursor: pointer !important;
        border: none !important; color: #9ca3af !important; font-weight: 600 !important; font-size: 1.5rem !important; letter-spacing: 0.5px !important;
    }
    .stRadio label:hover { background: rgba(255,255,255,0.06) !important; color: #ffffff !important; }
    .stRadio label[data-checked="true"] {
        background: rgba(79, 70, 229, 0.2) !important; color: #ffffff !important;
        border-left: 3px solid #4f46e5 !important; border-radius: 0 10px 10px 0 !important;
    }
    .stRadio label[data-checked="true"] .nav-icon { color: #4f46e5 !important; }
    .stRadio label > div:first-child { display: none !important; }
    .stRadio label > div:last-child { flex: 1; display: flex !important; align-items: center !important; gap: 0.9rem !important; }

    .sidebar-stats {
        background: rgba(255,255,255,0.04); padding: 0.8rem 1rem; border-radius: 10px;
        margin: 1.5rem 0.5rem; border: 1px solid rgba(255,255,255,0.04);
    }
    .sidebar-stats p { color: #9ca3af; font-size: 0.6rem; margin: 0 0 0.4rem 0; text-transform: uppercase; letter-spacing: 1px; }
    .sidebar-stats .stat-value { color: #e5e7eb; font-size: 0.85rem; margin: 0.1rem 0; font-weight: 400; }
    .sidebar-stats .stat-value strong { color: #ffffff; font-weight: 600; }
    .sidebar-stats .stat-highlight { color: #f59e0b; font-weight: 600; }

    .sidebar-footer {
        text-align: center; color: #6b7280; font-size: 0.6rem; margin-top: 1.5rem;
        padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.04); line-height: 1.8;
    }
    .sidebar-footer .emoji { font-size: 0.8rem; }

    .header-container {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        padding: 1.8rem 2.5rem; border-radius: 16px; margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.06); box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    .header-title {
        color: #ffffff; font-size: 2rem; font-weight: 700; margin: 0; letter-spacing: -0.5px;
        display: flex; align-items: center; gap: 0.7rem;
    }
    .header-title .highlight {
        background: linear-gradient(90deg, #f7971e, #ffd200);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }
    .header-subtitle { color: #a8b2d1; font-size: 0.95rem; margin: 0.3rem 0 0 0; opacity: 0.8; }
    .header-badge {
        display: inline-block; background: rgba(255, 215, 0, 0.1); color: #ffd700;
        padding: 0.2rem 1rem; border-radius: 20px; font-size: 0.7rem;
        border: 1px solid rgba(255, 215, 0, 0.15); margin-top: 0.5rem;
    }

    .metric-card {
        background: #ffffff; padding: 1rem 1.2rem; border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05); border: 1px solid #f1f3f5;
        transition: all 0.25s ease; height: 100%;
    }
    .metric-card:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(0,0,0,0.08); border-color: #4f46e5; }
    .metric-value { font-size: 1.8rem; font-weight: 700; color: #111827; line-height: 1.2; }
    .metric-label { font-size: 0.75rem; color: #6b7280; margin-top: 0.2rem; font-weight: 500; }
    .metric-change { font-size: 0.65rem; padding: 0.1rem 0.5rem; border-radius: 12px; font-weight: 600; display: inline-block; margin-top: 0.2rem; }
    .metric-change.up { background: #d1fae5; color: #065f46; }
    .metric-change.down { background: #fee2e2; color: #991b1b; }

    .section-header {
        font-size: 1.2rem; font-weight: 600; color: #111827; margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem; border-bottom: 2px solid #e5e7eb; display: flex; align-items: center; gap: 0.5rem;
    }
    .section-header .highlight { color: #4f46e5; }

    .chart-card {
        background: #ffffff; padding: 1rem 1.2rem 1.2rem 1.2rem; border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04); border: 1px solid #f1f3f5; margin: 0.5rem 0; height: 100%;
    }
    .chart-card h4 {
        font-size: 1.1rem; font-weight: 700; color: #111827; margin: 0 0 0.5rem 0;
        padding-bottom: 0.3rem; border-bottom: 2px solid #f3f4f6;
    }

    .info-box {
        background: #dbeafe !important; padding: 1rem 1.5rem !important; border-radius: 10px !important;
        border-left: 5px solid #2563eb !important; margin: 0.5rem 0 !important; color: #1e293b !important;
    }
    .info-box strong { color: #1e40af !important; }

    .risk-card {
        padding: 0.7rem 1.2rem; border-radius: 10px; margin: 0.4rem 0; border-left: 4px solid;
        display: flex; justify-content: space-between; align-items: center; background: #fafafa;
    }
    .risk-card .risk-level { font-weight: 700; font-size: 0.8rem; min-width: 70px; color: #111827 !important; }
    .risk-card .risk-segment { font-size: 0.85rem; color: #374151 !important; flex: 1; margin: 0 1rem; }
    .risk-card .risk-action {
        font-size: 0.75rem; background: #4f46e5; color: #ffffff !important;
        padding: 0.15rem 0.8rem; border-radius: 20px; font-weight: 500; white-space: nowrap;
    }
    .risk-critical { border-color: #dc2626; background: #fef2f2; }
    .risk-high { border-color: #f59e0b; background: #fffbeb; }
    .risk-medium { border-color: #3b82f6; background: #eff6ff; }
    .risk-low { border-color: #22c55e; background: #f0fdf4; }
    .risk-critical .risk-level { color: #dc2626 !important; }
    .risk-high .risk-level { color: #b45309 !important; }
    .risk-medium .risk-level { color: #1d4ed8 !important; }
    .risk-low .risk-level { color: #15803d !important; }

    .strategy-card {
        background: white; padding: 0.7rem 1.2rem; border-radius: 10px; margin: 0.4rem 0;
        border: 1px solid #e5e7eb; display: flex; align-items: center; gap: 1rem; transition: all 0.2s;
    }
    .strategy-card:hover { border-color: #4f46e5; box-shadow: 0 4px 15px rgba(79, 70, 229, 0.08); }
    .strategy-number {
        background: linear-gradient(135deg, #4f46e5, #7c3aed); color: white; width: 26px; height: 26px;
        border-radius: 50%; display: flex; align-items: center; justify-content: center;
        font-weight: 700; font-size: 0.75rem; flex-shrink: 0;
    }
    .strategy-text { font-size: 0.85rem; color: #1f2937 !important; }

    .predictor-section { background: #f8fafc; padding: 1.2rem 1.5rem; border-radius: 12px; border: 1px solid #e5e7eb; margin: 0.5rem 0; }
    .predictor-section h4 { font-size: 0.9rem; font-weight: 600; color: #111827; margin: 0 0 0.5rem 0; }

    .model-card {
        background: white; padding: 1rem; border-radius: 12px; border: 1px solid #e5e7eb;
        text-align: center; transition: all 0.3s; height: 100%;
    }
    .model-card:hover { border-color: #4f46e5; box-shadow: 0 4px 20px rgba(0,0,0,0.06); }
    .model-card .model-name { font-size: 0.8rem; font-weight: 600; color: #374151 !important; margin: 0; }
    .model-card .model-score { font-size: 1.6rem; font-weight: 700; color: #111827 !important; margin: 0.2rem 0; }
    .model-card .model-label { font-size: 0.65rem; color: #6b7280 !important; margin: 0; }
    .model-card .best-badge {
        display: inline-block; background: #d1fae5; color: #065f46 !important; font-size: 0.55rem;
        padding: 0.1rem 0.6rem; border-radius: 12px; font-weight: 600; margin-top: 0.2rem;
    }

    /* ===== KPI TABLE (real HTML table, not a pandas Styler passed to
       st.dataframe — Streamlit's dataframe component ignores most of that
       CSS, which is why the header kept looking unstyled no matter what
       colors were set on it). Full borders on every cell + header, as
       requested. ===== */
    .kpi-table-wrap { overflow-x: auto; border-radius: 12px; border: 2px solid #4f46e5; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
    .kpi-table { width: 100%; border-collapse: collapse; background: #ffffff; }
    .kpi-table th {
        background: #1a1a2e; color: #ffffff !important; padding: 14px 18px; text-align: left;
        font-weight: 700; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;
        border: 1px solid #4f46e5;
    }
    .kpi-table td { padding: 12px 16px; font-size: 0.85rem; color: #1f2937 !important; border: 1px solid #d1d5db; }
    .kpi-table tbody tr:nth-child(even) { background: #f8fafc; }
    .kpi-table tbody tr:nth-child(odd) { background: #ffffff; }
    .kpi-table tbody tr:hover td { background: #eef2ff; }
    .kpi-table .metric-cell { font-weight: 600; color: #1a1a2e !important; }
    .kpi-table .target-cell { color: #4b5563 !important; font-weight: 500; }
    .kpi-status-pill {
        display: inline-block; padding: 0.2rem 0.7rem; border-radius: 20px; font-weight: 700; font-size: 0.78rem;
    }
    .kpi-status-ontrack { background: #d1fae5; color: #065f46 !important; }
    .kpi-status-monitor { background: #fef3c7; color: #92400e !important; }

    .footer {
        text-align: center; padding: 1.2rem 0 0.5rem 0; color: #9ca3af; font-size: 0.7rem;
        border-top: 1px solid #e5e7eb; margin-top: 2rem;
    }
    .footer strong { color: #4b5563; }
</style>
""", unsafe_allow_html=True)

# ============================================
# CHART TEXT/COLOR HELPER
# ============================================
CHART_FONT = dict(color='#e5e7eb', size=12)

def style_fig(fig, height=None):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=CHART_FONT,
        template='plotly_dark',
    )
    if height:
        fig.update_layout(height=height)
    return fig

# ============================================
# LOAD DATA
# ============================================
@st.cache_data
def load_data():
    df = pd.read_csv("data/telco_churn.csv")
    df['Churn_Flag'] = (df['Churn'] == 'Yes').astype(int)
    return df

def check_required_files():
    """Checks for the three files the Predictor page needs and returns a
    list of (path, exists) tuples plus the working directory Streamlit is
    actually running from. Used to build a precise, actionable error
    message instead of a generic 'not found'."""
    required = [
        "outputs/best_xgb_model.pkl",
        "outputs/model_features.pkl",
        "outputs/model_feature_defaults.pkl",
    ]
    status = [(f, os.path.exists(f)) for f in required]
    return status, os.getcwd()

@st.cache_resource
def load_model():
    try:
        return joblib.load("outputs/best_xgb_model.pkl"), None
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"

@st.cache_resource
def load_feature_schema():
    """Loads the exact column list + median/mode defaults the model was
    trained on (saved by the notebook). Needed because the Predictor form
    only collects a handful of fields, but the model expects every
    engineered column in the same order they were trained on."""
    try:
        columns = joblib.load("outputs/model_features.pkl")
        defaults = joblib.load("outputs/model_feature_defaults.pkl")
        return columns, defaults, None
    except Exception as e:
        return None, None, f"{type(e).__name__}: {e}"

def build_feature_row(tenure, monthly, total, contract, internet, payment,
                       gender, senior, columns, defaults, monthly_median):
    """Builds a single-row DataFrame matching the model's training schema.
    Fields the Predictor form collects are set explicitly; everything else
    (Partner, Dependents, OnlineSecurity, NumServices, etc.) falls back to
    the training-set median/mode default, since the form doesn't ask about
    them."""
    row = pd.Series(defaults, index=columns).fillna(0)

    row['tenure'] = tenure
    row['MonthlyCharges'] = monthly
    row['TotalCharges'] = total
    row['AvgMonthlyCharges'] = total / (tenure + 1)
    if 'gender' in row.index:
        row['gender'] = 1 if gender == "Male" else 0
    if 'SeniorCitizen' in row.index:
        row['SeniorCitizen'] = 1 if senior == "Yes" else 0

    for c in ['Contract_One year', 'Contract_Two year', 'Contract_Month-to-month']:
        if c in row.index:
            row[c] = 0
    if contract in ("One year", "Two year"):
        col = f'Contract_{contract}'
        if col in row.index:
            row[col] = 1
    elif contract == "Month-to-month" and 'Contract_Month-to-month' in row.index:
        row['Contract_Month-to-month'] = 1

    for c in ['InternetService_Fiber optic', 'InternetService_No']:
        if c in row.index:
            row[c] = 0
    if internet in ("Fiber optic", "No"):
        col = f'InternetService_{internet}'
        if col in row.index:
            row[col] = 1

    payment_map = {
        "Electronic check": "PaymentMethod_Electronic check",
        "Mailed check": "PaymentMethod_Mailed check",
        "Bank transfer": "PaymentMethod_Bank transfer (automatic)",
        "Credit card": "PaymentMethod_Credit card (automatic)",
    }
    for c in payment_map.values():
        if c in row.index:
            row[c] = 0
    target_col = payment_map.get(payment)
    if target_col in row.index:
        row[target_col] = 1

    tenure_group_cols = [c for c in row.index if c.startswith('TenureGroup_')]
    for c in tenure_group_cols:
        row[c] = 0
    bins = [0, 1, 6, 12, 24, 60, 100]
    labels = ['0-1 months', '2-6 months', '7-12 months', '1-2 years', '2-5 years', '5+ years']
    group = pd.cut([tenure], bins=bins, labels=labels, right=False)[0]
    group_col = f'TenureGroup_{group}'
    if group_col in row.index:
        row[group_col] = 1

    if 'HighCost_Monthly' in row.index:
        row['HighCost_Monthly'] = int(monthly > monthly_median and contract == "Month-to-month")

    return pd.DataFrame([row])[columns]

df = load_data()
model, model_load_error = load_model()
feature_columns, feature_defaults, schema_load_error = load_feature_schema()

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-brand">
        <div class="logo">{CHART_ICON_SVG.format(size=40)}</div>
        <h2>Churn <span>Analytics</span></h2>
        <p>Customer Retention Platform</p>
    </div>
    """, unsafe_allow_html=True)

    nav_options = ["Overview", "Analysis", "Predictor", "Models", "Insights"]
    nav_icons = ["🏠", "📈", "🔮", "📊", "💡"]

    page_index = st.radio(
        label="Navigation",
        options=range(len(nav_options)),
        format_func=lambda i: f"{nav_icons[i]} {nav_options[i]}",
        index=0,
        key="nav_radio",
        label_visibility="collapsed"
    )
    page = nav_options[page_index]

    total = len(df)
    churned = df[df['Churn'] == 'Yes'].shape[0]
    churn_rate = (churned / total) * 100

    st.markdown(f"""
    <div class="sidebar-stats">
        <p>📊 Dataset Snapshot</p>
        <div class="stat-value">Total: <strong>{total:,}</strong></div>
        <div class="stat-value">Churned: <strong>{churned:,}</strong></div>
        <div class="stat-value">Rate: <strong class="stat-highlight">{churn_rate:.1f}%</strong></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-footer">
        <span class="emoji">⚡</span> Real-time Analytics<br>
        <span class="emoji">📊</span> Interactive Visualizations<br>
        <span class="emoji">🎯</span> Actionable Insights
    </div>
    """, unsafe_allow_html=True)

# ============================================
# MAIN HEADER
# ============================================
st.markdown(f"""
<div class="header-container">
    <h1 class="header-title">{CHART_ICON_SVG.format(size=34)} Customer Churn <span class="highlight">Analytics</span></h1>
    <p class="header-subtitle">AI-powered insights to reduce customer churn and improve retention</p>
    <span class="header-badge">✨ IBM Telco Dataset • 7,043 Customers</span>
</div>
""", unsafe_allow_html=True)

# ============================================
# PAGE: OVERVIEW
# ============================================
if page == "Overview":
    col1, col2, col3, col4 = st.columns(4)

    total_customers = len(df)
    churn_rate = (df['Churn'] == 'Yes').mean() * 100
    avg_tenure = df['tenure'].mean()
    avg_monthly = df['MonthlyCharges'].mean()

    with col1:
        st.markdown(f"""<div class="metric-card"><div class="metric-value">{total_customers:,}</div><div class="metric-label">👥 Total Customers</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card"><div class="metric-value" style="color: {'#dc2626' if churn_rate > 20 else '#22c55e'};">{churn_rate:.1f}%</div><div class="metric-label">📈 Churn Rate</div><span class="metric-change {'down' if churn_rate > 20 else 'up'}">{'+' if churn_rate > 20 else '-'}2.1%</span></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-card"><div class="metric-value">{avg_tenure:.1f}</div><div class="metric-label">⏱️ Avg. Tenure (months)</div></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="metric-card"><div class="metric-value">${avg_monthly:.0f}</div><div class="metric-label">💰 Avg. Monthly Charge</div></div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="chart-card"><h4>📊 Churn Distribution</h4>', unsafe_allow_html=True)
        churn_counts = df['Churn'].value_counts()
        fig = go.Figure(data=[go.Pie(
            labels=['✅ No Churn', '⚠️ Churn'],
            values=churn_counts.values,
            hole=0.5,
            marker=dict(colors=['#22c55e', '#dc2626'], line=dict(color='#1a1a2e', width=2)),
            textinfo='label+percent',
            textposition='outside',
            textfont=dict(size=14, color='#f9fafb'),
            pull=[0, 0.05],
            showlegend=False
        )])
        fig.update_layout(
            height=340, margin=dict(t=20, b=20, l=20, r=20),
            annotations=[dict(text=f'Total: {len(df):,} Customers', x=0.5, y=-0.08, font=dict(size=13, color='#cbd5e1'), showarrow=False)]
        )
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-card"><h4>📈 Churn Rate by Contract</h4>', unsafe_allow_html=True)
        contract_churn = df.groupby('Contract').apply(lambda x: (x['Churn'] == 'Yes').mean() * 100).reset_index()
        contract_churn.columns = ['Contract', 'Churn Rate']
        fig = px.bar(contract_churn, x='Contract', y='Churn Rate', color='Churn Rate',
                     color_continuous_scale=['#22c55e', '#f59e0b', '#dc2626'],
                     text=contract_churn['Churn Rate'].round(1), template='plotly_dark', height=340)
        fig.update_traces(textposition='outside', marker_line_width=0, textfont=dict(size=13, color='#f9fafb'))
        fig.update_layout(showlegend=False, margin=dict(t=10, b=30, l=10, r=10), xaxis_title="", yaxis_title="Churn Rate (%)",
                           yaxis=dict(range=[0, max(contract_churn['Churn Rate']) * 1.15]))
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="chart-card"><h4>📉 Tenure Distribution by Churn Status</h4>', unsafe_allow_html=True)
        fig = px.histogram(df, x='tenure', color='Churn', nbins=30, barmode='stack',
                            color_discrete_map={'Yes': '#dc2626', 'No': '#22c55e'}, template='plotly_dark', height=320,
                            labels={'tenure': 'Tenure (months)', 'count': 'Customers'}, category_orders={'Churn': ['No', 'Yes']})
        fig.update_layout(margin=dict(t=10, b=30, l=10, r=10), legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-card"><h4>💳 Churn Rate by Payment Method</h4>', unsafe_allow_html=True)
        payment_churn = df.groupby('PaymentMethod').apply(lambda x: (x['Churn'] == 'Yes').mean() * 100).reset_index()
        payment_churn.columns = ['Payment Method', 'Churn Rate']
        payment_churn = payment_churn.sort_values('Churn Rate', ascending=False)
        fig = px.bar(payment_churn, x='Payment Method', y='Churn Rate', color='Churn Rate',
                     color_continuous_scale=['#22c55e', '#f59e0b', '#dc2626'],
                     text=payment_churn['Churn Rate'].round(1), template='plotly_dark', height=320)
        fig.update_traces(textposition='outside', marker_line_width=0, textfont=dict(size=12, color='#f9fafb'))
        fig.update_layout(showlegend=False, margin=dict(t=10, b=40, l=10, r=10), xaxis_title="", yaxis_title="Churn Rate (%)",
                           yaxis=dict(range=[0, max(payment_churn['Churn Rate']) * 1.15]))
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# PAGE: ANALYSIS
# ============================================
elif page == "Analysis":
    st.markdown('<div class="section-header">🔍 <span class="highlight">Churn Analysis</span></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        contracts = st.multiselect("Contract Type", options=df['Contract'].unique(), default=df['Contract'].unique(), key='contract_filter')
    with col2:
        genders = st.multiselect("Gender", options=df['gender'].unique(), default=df['gender'].unique(), key='gender_filter')
    with col3:
        internet = st.multiselect("Internet Service", options=df['InternetService'].unique(), default=df['InternetService'].unique(), key='internet_filter')

    filtered_df = df[(df['Contract'].isin(contracts)) & (df['gender'].isin(genders)) & (df['InternetService'].isin(internet))]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="metric-card"><div class="metric-value">{len(filtered_df):,}</div><div class="metric-label">📊 Filtered Customers</div></div>""", unsafe_allow_html=True)
    with col2:
        rate = (filtered_df['Churn'] == 'Yes').mean() * 100
        st.markdown(f"""<div class="metric-card"><div class="metric-value" style="color: {'#dc2626' if rate > 20 else '#22c55e'};">{rate:.1f}%</div><div class="metric-label">📈 Churn Rate</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-card"><div class="metric-value">{filtered_df['tenure'].mean():.1f}</div><div class="metric-label">⏱️ Avg. Tenure</div></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="metric-card"><div class="metric-value">${filtered_df['MonthlyCharges'].mean():.2f}</div><div class="metric-label">💰 Avg. Monthly</div></div>""", unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="chart-card"><h4>🌐 Churn Rate by Internet Service</h4>', unsafe_allow_html=True)
        service_churn = filtered_df.groupby('InternetService').apply(lambda x: (x['Churn'] == 'Yes').mean() * 100).reset_index()
        service_churn.columns = ['Service', 'Churn Rate']
        fig = px.bar(service_churn, x='Service', y='Churn Rate', color='Churn Rate',
                     color_continuous_scale=['#22c55e', '#f59e0b', '#dc2626'],
                     text=service_churn['Churn Rate'].round(1), template='plotly_dark', height=320)
        fig.update_traces(textposition='outside', textfont=dict(size=13, color='#f9fafb'))
        fig.update_layout(showlegend=False, margin=dict(t=10, b=30))
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-card"><h4>💳 Churn Rate by Payment Method</h4>', unsafe_allow_html=True)
        payment_churn = filtered_df.groupby('PaymentMethod').apply(lambda x: (x['Churn'] == 'Yes').mean() * 100).reset_index()
        payment_churn.columns = ['Payment Method', 'Churn Rate']
        payment_churn = payment_churn.sort_values('Churn Rate', ascending=False)
        fig = px.bar(payment_churn, x='Payment Method', y='Churn Rate', color='Churn Rate',
                     color_continuous_scale=['#22c55e', '#f59e0b', '#dc2626'],
                     text=payment_churn['Churn Rate'].round(1), template='plotly_dark', height=320)
        fig.update_traces(textposition='outside', textfont=dict(size=12, color='#f9fafb'))
        fig.update_layout(showlegend=False, margin=dict(t=10, b=40))
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# PAGE: PREDICTOR
# ============================================
elif page == "Predictor":
    st.markdown('<div class="section-header">🔮 <span class="highlight">Churn Predictor</span></div>', unsafe_allow_html=True)
    st.markdown("""<div class="info-box"><strong>💡 How it works:</strong> Enter customer details below to get a churn probability score. The model analyzes customer behavior patterns to predict churn risk.</div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="predictor-section"><h4>👤 Customer Profile</h4>', unsafe_allow_html=True)
        tenure = st.slider("Tenure (months)", 0, 72, 12, key='pred_tenure')
        monthly = st.slider("Monthly Charges ($)", 0, 150, 50, key='pred_monthly')
        total = st.slider("Total Charges ($)", 0, 8000, 1000, key='pred_total')
        contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"], key='pred_contract')
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="predictor-section"><h4>📋 Service Details</h4>', unsafe_allow_html=True)
        internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"], key='pred_internet')
        payment = st.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer", "Credit card"], key='pred_payment')
        # Note: displayed as "Bank transfer" / "Credit card" for brevity, but
        # mapped to the training data's exact "... (automatic)" labels below.
        gender = st.selectbox("Gender", ["Male", "Female"], key='pred_gender')
        senior = st.selectbox("Senior Citizen", ["No", "Yes"], key='pred_senior')
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔮 Predict Churn Risk", use_container_width=True, key='predict_btn'):
            if model is None or feature_columns is None:
                status, cwd = check_required_files()
                missing = [f for f, exists in status if not exists]
                st.error("⚠️ Model or feature schema not found.")
                st.markdown(f"**Streamlit is running from:** `{cwd}`")
                for f, exists in status:
                    st.markdown(f"- {'✅' if exists else '❌'} `{f}`")
                if missing:
                    st.info(
                        "The files marked ❌ above don't exist at that path. "
                        "Either run the notebook's save cells (the XGBoost "
                        "GridSearchCV cell and the 'SAVE FEATURE SCHEMA' "
                        "cell) from top to bottom so they get created, or, "
                        "if the ✅/❌ files above look wrong, launch "
                        "Streamlit from the same folder that contains your "
                        "`outputs/` directory."
                    )
                else:
                    st.info(
                        "All three files exist but failed to load. "
                        "Actual error(s) below:"
                    )
                    if model_load_error:
                        st.code(f"best_xgb_model.pkl:\n{model_load_error}")
                    if schema_load_error:
                        st.code(f"model_features.pkl / model_feature_defaults.pkl:\n{schema_load_error}")
                st.stop()

            X_input = build_feature_row(
                tenure, monthly, total, contract, internet, payment,
                gender, senior, feature_columns, feature_defaults,
                monthly_median=df['MonthlyCharges'].median(),
            )
            prob = model.predict_proba(X_input)[:, 1][0]
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                fig = go.Figure(go.Indicator(
                    mode="gauge+number", value=prob, title={'text': "Churn Risk Score", 'font': {'size': 16}},
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={'axis': {'range': [0, 1], 'tickwidth': 1}, 'bar': {'color': "#4f46e5"},
                           'steps': [{'range': [0, 0.3], 'color': '#22c55e'}, {'range': [0.3, 0.6], 'color': '#f59e0b'}, {'range': [0.6, 1], 'color': '#dc2626'}],
                           'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': 0.5}}
                ))
                fig.update_layout(height=300, margin=dict(t=20, b=20))
                style_fig(fig)
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                if prob < 0.3:
                    level, color, bg, border = "🟢 Low Risk", "#22c55e", "#f0fdf4", "#22c55e"
                    action = "Customer is likely to stay. Continue providing quality service."
                elif prob < 0.6:
                    level, color, bg, border = "🟡 Medium Risk", "#f59e0b", "#fffbeb", "#f59e0b"
                    action = "Customer shows signs of potential churn. Consider engagement offers."
                else:
                    level, color, bg, border = "🔴 High Risk", "#dc2626", "#fef2f2", "#dc2626"
                    action = "Customer is at high risk! Immediate retention action needed."
                st.markdown(f"""
                <div style="background: {bg}; padding: 1.5rem; border-radius: 12px; border: 2px solid {border}; text-align: center;">
                    <h2 style="color: {color}; margin: 0; font-size: 1.5rem;">{level}</h2>
                    <div style="font-size: 2.5rem; font-weight: 700; margin: 0.5rem 0; color: #111827;">{prob:.1%}</div>
                    <p style="color: #4b5563; margin: 0; font-size: 0.85rem;">{action}</p>
                </div>
                """, unsafe_allow_html=True)

# ============================================
# PAGE: MODELS
# ============================================
elif page == "Models":
    st.markdown('<div class="section-header">📊 <span class="highlight">Model Performance</span></div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    # Corrected, leak-free metrics from the train/validation/test split
    # (threshold selected on validation, evaluated once on the held-out test set)
    #
    # NOTE ON "BEST": Logistic Regression scores marginally higher on
    # ROC-AUC/PR-AUC in the comparison table, but it is never saved to disk
    # anywhere in the notebook (no joblib.dump for it) and cannot be loaded
    # by load_model() below. The "Predict Churn Risk" page actually runs
    # outputs/best_xgb_model.pkl, i.e. XGBoost (Tuned). To avoid the
    # dashboard claiming one model is best while a different one produces
    # every live prediction, the badge here is tied to the model that is
    # actually deployed, not just the model with the top offline metric.
    # (If you'd rather deploy Logistic Regression, retrain it in the
    # notebook, joblib.dump it, and point load_model() at that file instead.)
    models = [
        {"name": "Logistic Regression", "roc": 0.8389, "pr": 0.6552},
        {"name": "Random Forest", "roc": 0.8289, "pr": 0.6318},
        {"name": "XGBoost", "roc": 0.8175, "pr": 0.6143},
        {"name": "XGBoost (Tuned)", "roc": 0.8339, "pr": 0.6357, "deployed": True},
    ]
    cols = [col1, col2, col3, col4]
    for i, model_info in enumerate(models):
        with cols[i]:
            best_badge = '<div class="best-badge">🏆 Deployed</div>' if model_info.get('deployed') else ''
            st.markdown(f"""<div class="model-card"><p class="model-name">{model_info['name']}</p><p class="model-score">{model_info['roc']:.4f}</p><p class="model-label">ROC-AUC</p><p style="font-size: 0.7rem; color: #6b7280; margin: 0.2rem 0;">PR-AUC: {model_info['pr']:.4f}</p>{best_badge}</div>""", unsafe_allow_html=True)
    st.caption("Logistic Regression edges out the others on ROC-AUC/PR-AUC, but XGBoost (Tuned) is the model actually saved and served by this dashboard's predictions below.")

    st.markdown("---")
    st.markdown('<div class="chart-card"><h4>📊 Model Performance Comparison</h4>', unsafe_allow_html=True)
    model_data = pd.DataFrame(models)
    fig = px.bar(model_data, x='name', y=['roc', 'pr'], barmode='group', text_auto='.3f',
                 color_discrete_map={'roc': '#4f46e5', 'pr': '#7c3aed'}, template='plotly_dark', height=350,
                 title="ROC-AUC vs PR-AUC Comparison")
    fig.update_layout(margin=dict(t=40, b=30), legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1), yaxis_title="Score", xaxis_title="")
    fig.update_traces(textfont=dict(color='#f9fafb', size=12))
    style_fig(fig)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-header">🔑 <span class="highlight">Top Features Driving Churn</span></div>', unsafe_allow_html=True)
    try:
        rf_importance = pd.read_csv("outputs/feature_importance_rf.csv", index_col=0)
        rf_importance = rf_importance.sort_values(by=rf_importance.columns[0], ascending=True).tail(15)
        fig = px.bar(rf_importance, x=rf_importance.columns[0], y=rf_importance.index, orientation='h',
                     color=rf_importance.columns[0], color_continuous_scale='Blues', template='plotly_dark', height=450,
                     title="Random Forest Feature Importance")
        fig.update_layout(margin=dict(t=40, b=30, l=0, r=0), xaxis_title="Importance", yaxis_title="", showlegend=False)
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)
    except Exception:
        st.info("ℹ️ Feature importance data not available. Run the notebook first to generate this chart.")

# ============================================
# PAGE: INSIGHTS
# ============================================
elif page == "Insights":
    st.markdown('<div class="section-header">💡 <span class="highlight">Business Insights & Recommendations</span></div>', unsafe_allow_html=True)

    # High-Risk Customer Segments
    st.markdown("### 🔴 High-Risk Customer Segments")
    risks = [
        {"level": "Critical", "segment": "Month-to-month + Monthly charges > $70", "action": "Immediate retention offer", "class": "risk-critical"},
        {"level": "High", "segment": "New customers (tenure < 6 months)", "action": "Welcome program", "class": "risk-high"},
        {"level": "Medium", "segment": "Fiber optic internet customers", "action": "Bundle services", "class": "risk-medium"},
        {"level": "Low", "segment": "Electronic check payment method", "action": "Auto-pay incentive", "class": "risk-low"}
    ]
    for risk in risks:
        st.markdown(f"""<div class="risk-card {risk['class']}"><span class="risk-level">{risk['level']}</span><span class="risk-segment">{risk['segment']}</span><span class="risk-action">{risk['action']}</span></div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Recommended Retention Strategies
    st.markdown("### ✅ Recommended Retention Strategies")
    strategies = [
        "💎 Offer annual contract discounts to month-to-month customers",
        "🎯 Implement 'welcome' retention program for first 6 months",
        "📦 Bundle high-speed internet with streaming services",
        "💳 Incentivize electronic check customers to switch to auto-pay"
    ]
    for i, strategy in enumerate(strategies, 1):
        st.markdown(f"""<div class="strategy-card"><div class="strategy-number">{i}</div><div class="strategy-text">{strategy}</div></div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Key Metrics to Monitor — real HTML table now (fixes the header visibility
    # for good, since st.dataframe + pandas Styler never actually applied
    # custom CSS reliably). Status is shown as a colored pill, which also makes
    # a separate "Status Legend" section unnecessary — the color + label is
    # already self-explanatory right in the table.
    st.markdown("### 📊 Key Metrics to Monitor")

    kpi_rows = [
        {"metric": "📊 Monthly churn rate by contract type", "target": "< 15% for month-to-month", "status": "On Track", "pill": "kpi-status-ontrack"},
        {"metric": "🎯 Churn rate at tenure milestones", "target": "< 20% at 3 months", "status": "Monitor", "pill": "kpi-status-monitor"},
        {"metric": "⭐ Customer satisfaction scores (high-risk)", "target": "> 4.0 / 5.0", "status": "On Track", "pill": "kpi-status-ontrack"},
        {"metric": "📈 Retention campaign conversion rate", "target": "> 25%", "status": "Monitor", "pill": "kpi-status-monitor"},
    ]

    table_rows_html = "".join(
        f"""<tr>
            <td class="metric-cell">{r['metric']}</td>
            <td class="target-cell">{r['target']}</td>
            <td><span class="kpi-status-pill {r['pill']}">{r['status']}</span></td>
        </tr>"""
        for r in kpi_rows
    )

    st.markdown(f"""
    <div class="kpi-table-wrap">
        <table class="kpi-table">
            <thead>
                <tr><th>Metric</th><th>Target</th><th>Status</th></tr>
            </thead>
            <tbody>
                {table_rows_html}
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

    # Export KPI Data
    st.markdown("---")
    st.markdown("### 📥 Export KPI Data")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        kpi_csv = pd.DataFrame([{"Metric": r["metric"], "Target": r["target"], "Status": r["status"]} for r in kpi_rows]).to_csv(index=False)
        st.download_button(
            label="📊 Download KPI Data (CSV)",
            data=kpi_csv,
            file_name="kpi_metrics.csv",
            mime="text/csv",
            use_container_width=True
        )

    # Download Report
    st.markdown("---")
    st.markdown("### 📥 Download Full Report")

    report_text = """
BUSINESS RECOMMENDATIONS REPORT
================================

HIGHEST RISK CUSTOMER SEGMENTS:
1. Month-to-month contracts with high monthly charges (>$70)
2. New customers (tenure < 6 months)
3. Fiber optic internet customers
4. Electronic check payment method

RECOMMENDED RETENTION STRATEGIES:
1. Offer annual contract discounts to month-to-month customers
2. Implement 'welcome' retention program for first 6 months
3. Bundle high-speed internet with streaming services
4. Incentivize electronic check customers to switch to auto-pay

KEY METRICS TO MONITOR:
- Monthly churn rate by contract type
- Churn rate at tenure milestones
- Customer satisfaction scores for high-risk segments
- Retention campaign conversion rate

MODEL PERFORMANCE (train/validation/test split, no leakage):
- Logistic Regression:  ROC-AUC 0.839, PR-AUC 0.655 (top ROC-AUC/PR-AUC, not deployed)
- Random Forest:        ROC-AUC 0.829, PR-AUC 0.632
- XGBoost:               ROC-AUC 0.818, PR-AUC 0.614
- XGBoost (Tuned):      ROC-AUC 0.834, PR-AUC 0.636  <-- DEPLOYED MODEL

DEPLOYED MODEL (XGBoost, Tuned) — Churn class, optimal threshold from validation:
- Precision (Churn): 0.54
- Recall (Churn):    0.72
- F1-Score (Churn):  0.62
"""

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label="📥 Download Report (TXT)",
            data=report_text,
            file_name="business_recommendations.txt",
            mime="text/plain",
            use_container_width=True
        )

# ================================================
# FOOTER
# ================================================
st.markdown("""
<div class="footer">
    <p><strong>Customer Churn Prediction Dashboard</strong> • Built with Streamlit & Python</p>
    <p>Data Source: IBM Telco Customer Churn Dataset • 7,043 Customers</p>
    <p style="margin-top: 0.3rem; opacity: 0.6;">© 2024 Churn Analytics • All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)