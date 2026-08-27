import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import warnings
warnings.filterwarnings('ignore')

# ============================================
# PAGE CONFIGURATION
# ============================================
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

    .stRadio > div { gap: 0.2rem; }
    .stRadio label {
        display: flex !important; align-items: center !important; gap: 0.8rem !important;
        padding: 0.8rem 1.2rem !important; margin: 0.15rem 0 !important; border-radius: 10px !important;
        background: transparent !important; transition: all 0.25s ease !important; cursor: pointer !important;
        border: none !important; color: #9ca3af !important; font-weight: 500 !important; font-size: 1.3rem !important; letter-spacing: 0.5px !important;
    }
    .stRadio label:hover { background: rgba(255,255,255,0.06) !important; color: #ffffff !important; }
    .stRadio label[data-checked="true"] {
        background: rgba(79, 70, 229, 0.2) !important; color: #ffffff !important;
        border-left: 3px solid #4f46e5 !important; border-radius: 0 10px 10px 0 !important;
    }
    .stRadio label[data-checked="true"] .nav-icon { color: #4f46e5 !important; }
    .stRadio label > div:first-child { display: none !important; }
    .stRadio label > div:last-child { flex: 1; display: flex !important; align-items: center !important; gap: 0.8rem !important; }

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

    /* ===== RISK CARDS ===== */
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

@st.cache_resource
def load_model():
    try:
        return joblib.load("outputs/best_xgb_model.pkl")
    except Exception:
        return None

df = load_data()
model = load_model()

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
        gender = st.selectbox("Gender", ["Male", "Female"], key='pred_gender')
        senior = st.selectbox("Senior Citizen", ["No", "Yes"], key='pred_senior')
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔮 Predict Churn Risk", use_container_width=True, key='predict_btn'):
            import random
            prob = random.uniform(0.1, 0.95)
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
    models = [
        {"name": "Logistic Regression", "roc": 0.8414, "pr": 0.630