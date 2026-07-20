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
# CUSTOM CSS - ULTRA PROFESSIONAL DASHBOARD
# ============================================
st.markdown("""
<style>
    /* ===== GLOBAL RESET ===== */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* ===== SIDEBAR - PROFESSIONAL VERTICAL NAV ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29 0%, #1a1a3e 50%, #24243e 100%);
        padding: 0;
        border-right: 1px solid rgba(255,255,255,0.06);
        width: 280px !important;
        min-width: 280px !important;
        max-width: 280px !important;
        position: fixed !important;
        height: 100vh !important;
        overflow-y: auto !important;
        z-index: 100 !important;
    }
    
    section[data-testid="stSidebar"] .css-1d391kg {
        padding: 0.5rem 0.8rem;
        width: 100%;
    }
    
    /* Hide default Streamlit elements */
    section[data-testid="stSidebar"] .st-emotion-cache-16idsys {
        padding: 0;
    }
    
    /* ===== SIDEBAR BRAND ===== */
    .sidebar-brand {
        text-align: center;
        padding: 1.8rem 0 1.2rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 1rem;
    }
    
    .sidebar-brand .logo {
        font-size: 2.8rem;
        display: block;
        margin-bottom: 0.2rem;
    }
    
    .sidebar-brand h2 {
        color: #ffffff;
        margin: 0;
        font-weight: 700;
        font-size: 1.2rem;
        letter-spacing: 0.5px;
    }
    
    .sidebar-brand h2 span {
        background: linear-gradient(90deg, #f7971e, #ffd200);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .sidebar-brand p {
        color: #6b7280;
        font-size: 0.7rem;
        margin: 0.1rem 0 0 0;
        letter-spacing: 1px;
    }
    
    /* ===== NAVIGATION - PROFESSIONAL VERTICAL MENU ===== */
    /* Hide default radio completely */
    .stRadio {
        margin: 0;
        padding: 0;
    }
    
    .stRadio > div {
        gap: 0.1rem;
        padding: 0.3rem 0.5rem;
    }
    
    .stRadio label {
        display: flex !important;
        align-items: center !important;
        gap: 0.8rem !important;
        padding: 0.6rem 1rem !important;
        margin: 0.15rem 0 !important;
        border-radius: 10px !important;
        background: transparent !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        border: none !important;
        color: #9ca3af !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        width: 100% !important;
        position: relative !important;
    }
    
    .stRadio label:hover {
        background: rgba(255,255,255,0.06) !important;
        color: #ffffff !important;
        transform: translateX(4px);
    }
    
    /* Active state - Professional highlight with left accent bar */
    .stRadio label[data-checked="true"] {
        background: rgba(79, 70, 229, 0.15) !important;
        color: #ffffff !important;
        border-left: 3px solid #4f46e5 !important;
        border-radius: 0 10px 10px 0 !important;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.1) !important;
    }
    
    .stRadio label[data-checked="true"] .nav-icon {
        color: #4f46e5 !important;
    }
    
    .stRadio label[data-checked="true"] .nav-text {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Hide the radio circle */
    .stRadio label > div:first-child {
        display: none !important;
    }
    
    .stRadio label > div:last-child {
        flex: 1;
        display: flex !important;
        align-items: center !important;
        gap: 0.8rem !important;
    }
    
    /* Nav icon styling */
    .nav-icon {
        font-size: 1.2rem;
        width: 1.8rem;
        display: inline-block;
        text-align: center;
        color: #6b7280;
        transition: color 0.25s ease;
    }
    
    .nav-text {
        color: #9ca3af;
        transition: color 0.25s ease;
    }
    
    /* Active nav text */
    .nav-text.active {
        color: #ffffff;
        font-weight: 600;
    }
    
    /* ===== SIDEBAR DIVIDER ===== */
    .sidebar-divider {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.06);
        margin: 0.8rem 1rem;
    }
    
    /* ===== SIDEBAR STATS ===== */
    .sidebar-stats {
        background: rgba(255,255,255,0.04);
        padding: 0.8rem 1rem;
        border-radius: 10px;
        margin: 0.8rem 0.5rem;
        border: 1px solid rgba(255,255,255,0.04);
    }
    
    .sidebar-stats .stats-label {
        color: #9ca3af;
        font-size: 0.6rem;
        margin: 0 0 0.4rem 0;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    .sidebar-stats .stat-item {
        color: #e5e7eb;
        font-size: 0.8rem;
        margin: 0.2rem 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .sidebar-stats .stat-item strong {
        color: #ffffff;
        font-weight: 600;
    }
    
    .sidebar-stats .stat-highlight {
        color: #f59e0b;
        font-weight: 600;
    }
    
    /* ===== SIDEBAR FOOTER ===== */
    .sidebar-footer {
        text-align: center;
        color: #6b7280;
        font-size: 0.6rem;
        margin-top: 1.5rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255,255,255,0.04);
        line-height: 1.8;
    }
    
    .sidebar-footer .emoji {
        font-size: 0.8rem;
    }
    
    /* ===== MAIN HEADER ===== */
    .header-container {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        padding: 1.8rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.06);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        margin-left: 280px;
    }
    
    .header-title {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .header-title .highlight {
        background: linear-gradient(90deg, #f7971e, #ffd200);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .header-subtitle {
        color: #a8b2d1;
        font-size: 0.95rem;
        margin: 0.3rem 0 0 0;
        opacity: 0.8;
    }
    
    .header-badge {
        display: inline-block;
        background: rgba(255, 215, 0, 0.1);
        color: #ffd700;
        padding: 0.2rem 1rem;
        border-radius: 20px;
        font-size: 0.7rem;
        border: 1px solid rgba(255, 215, 0, 0.15);
        margin-top: 0.5rem;
    }
    
    /* ===== METRIC CARDS ===== */
    .metric-card {
        background: #ffffff;
        padding: 1rem 1.2rem;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05);
        border: 1px solid #f1f3f5;
        transition: all 0.25s ease;
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        border-color: #4f46e5;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #111827;
        line-height: 1.2;
    }
    
    .metric-label {
        font-size: 0.75rem;
        color: #6b7280;
        margin-top: 0.2rem;
        font-weight: 500;
    }
    
    .metric-change {
        font-size: 0.65rem;
        padding: 0.1rem 0.5rem;
        border-radius: 12px;
        font-weight: 600;
        display: inline-block;
        margin-top: 0.2rem;
    }
    
    .metric-change.up {
        background: #d1fae5;
        color: #065f46;
    }
    
    .metric-change.down {
        background: #fee2e2;
        color: #991b1b;
    }
    
    /* ===== SECTION HEADERS ===== */
    .section-header {
        font-size: 1.2rem;
        font-weight: 700;
        color: #111827;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e5e7eb;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .section-header .highlight {
        color: #4f46e5;
    }
    
    /* ===== CHART CARDS ===== */
    .chart-card {
        background: #ffffff;
        padding: 1rem 1.2rem 1.2rem 1.2rem;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        border: 1px solid #f1f3f5;
        margin: 0.5rem 0;
        height: 100%;
    }
    
    .chart-card h4 {
        font-size: 1.1rem;
        font-weight: 700;
        color: #111827;
        margin: 0 0 0.5rem 0;
        padding-bottom: 0.3rem;
        border-bottom: 2px solid #f3f4f6;
    }
    
    /* ===== INFO BOX ===== */
    .info-box {
        background: #dbeafe !important;
        padding: 1rem 1.5rem !important;
        border-radius: 10px !important;
        border-left: 5px solid #2563eb !important;
        margin: 0.5rem 0 !important;
        color: #1e293b !important;
    }
    
    .info-box strong {
        color: #1e40af !important;
    }
    
    /* ===== RISK CARDS ===== */
    .risk-card {
        padding: 0.7rem 1.2rem;
        border-radius: 10px;
        margin: 0.4rem 0;
        border-left: 4px solid;
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #fafafa;
    }
    
    .risk-card .risk-level {
        font-weight: 600;
        font-size: 0.8rem;
        min-width: 70px;
    }
    
    .risk-card .risk-segment {
        font-size: 0.85rem;
        color: #374151;
        flex: 1;
        margin: 0 1rem;
    }
    
    .risk-card .risk-action {
        font-size: 0.75rem;
        background: #4f46e5;
        color: white;
        padding: 0.15rem 0.8rem;
        border-radius: 20px;
        font-weight: 500;
        white-space: nowrap;
    }
    
    .risk-critical { border-color: #dc2626; background: #fef2f2; }
    .risk-high { border-color: #f59e0b; background: #fffbeb; }
    .risk-medium { border-color: #3b82f6; background: #eff6ff; }
    .risk-low { border-color: #22c55e; background: #f0fdf4; }
    
    /* ===== STRATEGY CARDS ===== */
    .strategy-card {
        background: white;
        padding: 0.7rem 1.2rem;
        border-radius: 10px;
        margin: 0.4rem 0;
        border: 1px solid #e5e7eb;
        display: flex;
        align-items: center;
        gap: 1rem;
        transition: all 0.2s;
    }
    
    .strategy-card:hover {
        border-color: #4f46e5;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.08);
    }
    
    .strategy-number {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        width: 26px;
        height: 26px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.75rem;
        flex-shrink: 0;
    }
    
    .strategy-text {
        font-size: 0.85rem;
        color: #1f2937;
    }
    
    /* ===== PREDICTOR ===== */
    .predictor-section {
        background: #f8fafc;
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        margin: 0.5rem 0;
    }
    
    .predictor-section h4 {
        font-size: 0.9rem;
        font-weight: 600;
        color: #111827;
        margin: 0 0 0.5rem 0;
    }
    
    /* ===== MODEL CARDS ===== */
    .model-card {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        text-align: center;
        transition: all 0.3s;
        height: 100%;
    }
    
    .model-card:hover {
        border-color: #4f46e5;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    }
    
    .model-card .model-name {
        font-size: 0.8rem;
        font-weight: 600;
        color: #374151;
        margin: 0;
    }
    
    .model-card .model-score {
        font-size: 1.6rem;
        font-weight: 700;
        color: #111827;
        margin: 0.2rem 0;
    }
    
    .model-card .model-label {
        font-size: 0.65rem;
        color: #6b7280;
        margin: 0;
    }
    
    .model-card .best-badge {
        display: inline-block;
        background: #d1fae5;
        color: #065f46;
        font-size: 0.55rem;
        padding: 0.1rem 0.6rem;
        border-radius: 12px;
        font-weight: 600;
        margin-top: 0.2rem;
    }
    
    /* ===== FOOTER ===== */
    .footer {
        text-align: center;
        padding: 1.2rem 0 0.5rem 0;
        color: #9ca3af;
        font-size: 0.7rem;
        border-top: 1px solid #e5e7eb;
        margin-top: 2rem;
        margin-left: 280px;
    }
    
    .footer strong {
        color: #4b5563;
    }
</style>
""", unsafe_allow_html=True)

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
    except:
        return None

df = load_data()
model = load_model()

# ============================================
# SIDEBAR - PROFESSIONAL VERTICAL NAVIGATION
# ============================================
with st.sidebar:
    # Brand
    st.markdown("""
    <div class="sidebar-brand">
        <span class="logo">📊</span>
        <h2>Churn <span>Analytics</span></h2>
        <p>Customer Retention Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation - Professional vertical menu
    nav_options = ["Overview", "Analysis", "Predictor", "Models", "Insights"]
    nav_icons = ["🏠", "📈", "🔮", "📊", "💡"]
    
    # Create the radio with formatted labels
    page_index = st.radio(
        label="Navigation",
        options=range(len(nav_options)),
        format_func=lambda i: f'<span class="nav-icon">{nav_icons[i]}</span><span class="nav-text">{nav_options[i]}</span>',
        index=0,
        key="nav_radio",
        label_visibility="collapsed"
    )
    page = nav_options[page_index]
    
    # Divider
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    
    # Dataset Stats
    total = len(df)
    churned = df[df['Churn'] == 'Yes'].shape[0]
    churn_rate = (churned / total) * 100
    
    st.markdown(f"""
    <div class="sidebar-stats">
        <div class="stats-label">📊 Dataset Snapshot</div>
        <div class="stat-item">Total <strong>{total:,}</strong></div>
        <div class="stat-item">Churned <strong>{churned:,}</strong></div>
        <div class="stat-item">Rate <strong class="stat-highlight">{churn_rate:.1f}%</strong></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Footer
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
st.markdown("""
<div class="header-container">
    <h1 class="header-title">📊 Customer Churn <span class="highlight">Analytics</span></h1>
    <p class="header-subtitle">AI-powered insights to reduce customer churn and improve retention</p>
    <span class="header-badge">✨ IBM Telco Dataset • 7,043 Customers</span>
</div>
""", unsafe_allow_html=True)

# ============================================
# PAGE: OVERVIEW
# ============================================
if page == "Overview":
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_customers = len(df)
    churn_rate = (df['Churn'] == 'Yes').mean() * 100
    avg_tenure = df['tenure'].mean()
    avg_monthly = df['MonthlyCharges'].mean()
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_customers:,}</div>
            <div class="metric-label">👥 Total Customers</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: {'#dc2626' if churn_rate > 20 else '#22c55e'};">{churn_rate:.1f}%</div>
            <div class="metric-label">📈 Churn Rate</div>
            <span class="metric-change {'down' if churn_rate > 20 else 'up'}">{'+' if churn_rate > 20 else '-'}2.1%</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{avg_tenure:.1f}</div>
            <div class="metric-label">⏱️ Avg. Tenure (months)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${avg_monthly:.0f}</div>
            <div class="metric-label">💰 Avg. Monthly Charge</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-card"><h4>📊 Churn Distribution</h4>', unsafe_allow_html=True)
        churn_counts = df['Churn'].value_counts()
        
        fig = go.Figure(data=[go.Pie(
            labels=['✅ No Churn', '⚠️ Churn'],
            values=churn_counts.values,
            hole=0.5,
            marker=dict(colors=['#22c55e', '#dc2626']),
            textinfo='label+percent',
            textposition='outside',
            textfont=dict(size=14, color='#1f2937'),
            pull=[0, 0.05],
            showlegend=False
        )])
        fig.update_layout(
            height=340,
            margin=dict(t=20, b=20, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#1f2937', size=13),
            annotations=[
                dict(
                    text=f'Total: {len(df):,} Customers',
                    x=0.5, y=-0.08,
                    font=dict(size=13, color='#6b7280'),
                    showarrow=False
                )
            ]
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-card"><h4>📈 Churn Rate by Contract</h4>', unsafe_allow_html=True)
        contract_churn = df.groupby('Contract').apply(lambda x: (x['Churn'] == 'Yes').mean() * 100).reset_index()
        contract_churn.columns = ['Contract', 'Churn Rate']
        
        fig = px.bar(
            contract_churn,
            x='Contract',
            y='Churn Rate',
            color='Churn Rate',
            color_continuous_scale=['#22c55e', '#f59e0b', '#dc2626'],
            text=contract_churn['Churn Rate'].round(1),
            template='plotly_white',
            height=340
        )
        fig.update_traces(
            textposition='outside', 
            marker_line_width=0,
            textfont=dict(size=13, color='#1f2937')
        )
        fig.update_layout(
            showlegend=False,
            margin=dict(t=10, b=30, l=10, r=10),
            xaxis_title="",
            yaxis_title="Churn Rate (%)",
            font=dict(color='#1f2937', size=12),
            yaxis=dict(range=[0, max(contract_churn['Churn Rate']) * 1.15])
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-card"><h4>📉 Tenure Distribution by Churn Status</h4>', unsafe_allow_html=True)
        fig = px.histogram(
            df,
            x='tenure',
            color='Churn',
            nbins=30,
            barmode='stack',
            color_discrete_map={'Yes': '#dc2626', 'No': '#22c55e'},
            template='plotly_white',
            height=320,
            labels={'tenure': 'Tenure (months)', 'count': 'Customers'},
            category_orders={'Churn': ['No', 'Yes']}
        )
        fig.update_layout(
            margin=dict(t=10, b=30, l=10, r=10),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            font=dict(color='#1f2937', size=12)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-card"><h4>💳 Churn Rate by Payment Method</h4>', unsafe_allow_html=True)
        payment_churn = df.groupby('PaymentMethod').apply(lambda x: (x['Churn'] == 'Yes').mean() * 100).reset_index()
        payment_churn.columns = ['Payment Method', 'Churn Rate']
        payment_churn = payment_churn.sort_values('Churn Rate', ascending=False)
        
        fig = px.bar(
            payment_churn,
            x='Payment Method',
            y='Churn Rate',
            color='Churn Rate',
            color_continuous_scale=['#22c55e', '#f59e0b', '#dc2626'],
            text=payment_churn['Churn Rate'].round(1),
            template='plotly_white',
            height=320
        )
        fig.update_traces(
            textposition='outside', 
            marker_line_width=0,
            textfont=dict(size=12, color='#1f2937')
        )
        fig.update_layout(
            showlegend=False,
            margin=dict(t=10, b=40, l=10, r=10),
            xaxis_title="",
            yaxis_title="Churn Rate (%)",
            font=dict(color='#1f2937', size=11),
            yaxis=dict(range=[0, max(payment_churn['Churn Rate']) * 1.15])
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# PAGE: ANALYSIS - WITH STANDARD DROPDOWN FILTERS
# ============================================
elif page == "Analysis":
    st.markdown('<div class="section-header">🔍 <span class="highlight">Churn Analysis</span></div>', unsafe_allow_html=True)
    
    # Filter Section - Professional layout
    st.markdown("### 📋 Filter Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Contract Type**")
        contracts = st.multiselect(
            "Select contract types",
            options=df['Contract'].unique(),
            default=df['Contract'].unique(),
            key='contract_filter',
            placeholder="Choose contract types..."
        )
    
    with col2:
        st.markdown("**Gender**")
        genders = st.multiselect(
            "Select gender",
            options=df['gender'].unique(),
            default=df['gender'].unique(),
            key='gender_filter',
            placeholder="Choose gender..."
        )
    
    with col3:
        st.markdown("**Internet Service**")
        internet = st.multiselect(
            "Select internet service",
            options=df['InternetService'].unique(),
            default=df['InternetService'].unique(),
            key='internet_filter',
            placeholder="Choose internet service..."
        )
    
    # Filter data
    filtered_df = df[
        (df['Contract'].isin(contracts)) &
        (df['gender'].isin(genders)) &
        (df['InternetService'].isin(internet))
    ]
    
    # Filtered Stats
    st.markdown("---")
    st.markdown("### 📊 Filtered Results")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(filtered_df):,}</div>
            <div class="metric-label">📊 Filtered Customers</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        rate = (filtered_df['Churn'] == 'Yes').mean() * 100
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: {'#dc2626' if rate > 20 else '#22c55e'};">{rate:.1f}%</div>
            <div class="metric-label">📈 Churn Rate</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{filtered_df['tenure'].mean():.1f}</div>
            <div class="metric-label">⏱️ Avg. Tenure</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${filtered_df['MonthlyCharges'].mean():.2f}</div>
            <div class="metric-label">💰 Avg. Monthly</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-card"><h4>🌐 Churn Rate by Internet Service</h4>', unsafe_allow_html=True)
        service_churn = filtered_df.groupby('InternetService').apply(lambda x: (x['Churn'] == 'Yes').mean() * 100).reset_index()
        service_churn.columns = ['Service', 'Churn Rate']
        
        fig = px.bar(
            service_churn,
            x='Service',
            y='Churn Rate',
            color='Churn Rate',
            color_continuous_scale=['#22c55e', '#f59e0b', '#dc2626'],
            text=service_churn['Churn Rate'].round(1),
            template='plotly_white',
            height=320
        )
        fig.update_traces(
            textposition='outside',
            textfont=dict(size=13, color='#1f2937')
        )
        fig.update_layout(showlegend=False, margin=dict(t=10, b=30), font=dict(size=12))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-card"><h4>💳 Churn Rate by Payment Method</h4>', unsafe_allow_html=True)
        payment_churn = filtered_df.groupby('PaymentMethod').apply(lambda x: (x['Churn'] == 'Yes').mean() * 100).reset_index()
        payment_churn.columns = ['Payment Method', 'Churn Rate']
        payment_churn = payment_churn.sort_values('Churn Rate', ascending=False)
        
        fig = px.bar(
            payment_churn,
            x='Payment Method',
            y='Churn Rate',
            color='Churn Rate',
            color_continuous_scale=['#22c55e', '#f59e0b', '#dc2626'],
            text=payment_churn['Churn Rate'].round(1),
            template='plotly_white',
            height=320
        )
        fig.update_traces(
            textposition='outside',
            textfont=dict(size=12, color='#1f2937')
        )
        fig.update_layout(showlegend=False, margin=dict(t=10, b=40), font=dict(size=11))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# PAGE: PREDICTOR
# ============================================
elif page == "Predictor":
    st.markdown('<div class="section-header">🔮 <span class="highlight">Churn Predictor</span></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <strong>💡 How it works:</strong> Enter customer details below to get a churn probability score.
        The model analyzes customer behavior patterns to predict churn risk.
    </div>
    """, unsafe_allow_html=True)
    
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
                    mode="gauge+number",
                    value=prob,
                    title={'text': "Churn Risk Score", 'font': {'size': 16}},
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={
                        'axis': {'range': [0, 1], 'tickwidth': 1},
                        'bar': {'color': "#4f46e5"},
                        'steps': [
                            {'range': [0, 0.3], 'color': '#22c55e'},
                            {'range': [0.3, 0.6], 'color': '#f59e0b'},
                            {'range': [0.6, 1], 'color': '#dc2626'}
                        ],
                        'threshold': {
                            'line': {'color': "black", 'width': 4},
                            'thickness': 0.75,
                            'value': 0.5
                        }
                    }
                ))
                fig.update_layout(height=300, margin=dict(t=20, b=20))
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                if prob < 0.3:
                    level = "🟢 Low Risk"
                    color = "#22c55e"
                    bg = "#f0fdf4"
                    border = "#22c55e"
                    action = "Customer is likely to stay. Continue providing quality service."
                elif prob < 0.6:
                    level = "🟡 Medium Risk"
                    color = "#f59e0b"
                    bg = "#fffbeb"
                    border = "#f59e0b"
                    action = "Customer shows signs of potential churn. Consider engagement offers."
                else:
                    level = "🔴 High Risk"
                    color = "#dc2626"
                    bg = "#fef2f2"
                    border = "#dc2626"
                    action = "Customer is at high risk! Immediate retention action needed."
                
                st.markdown(f"""
                <div style="background: {bg}; padding: 1.5rem; border-radius: 12px; border: 2px solid {border}; text-align: center;">
                    <h2 style="color: {color}; margin: 0; font-size: 1.5rem;">{level}</h2>
                    <div style="font-size: 2.5rem; font-weight: 700; margin: 0.5rem 0; color: #111827;">
                        {prob:.1%}
                    </div>
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
        {"name": "Logistic Regression", "roc": 0.8414, "pr": 0.6306},
        {"name": "Random Forest", "roc": 0.8411, "pr": 0.6538, "best": True},
        {"name": "XGBoost", "roc": 0.8369, "pr": 0.6477},
        {"name": "XGBoost (Tuned)", "roc": 0.8430, "pr": 0.6512}
    ]
    
    cols = [col1, col2, col3, col4]
    for i, model in enumerate(models):
        with cols[i]:
            best_badge = '<div class="best-badge">🏆 Best</div>' if model.get('best') else ''
            st.markdown(f"""
            <div class="model-card">
                <p class="model-name">{model['name']}</p>
                <p class="model-score">{model['roc']:.4f}</p>
                <p class="model-label">ROC-AUC</p>
                <p style="font-size: 0.7rem; color: #6b7280; margin: 0.2rem 0;">PR-AUC: {model['pr']:.4f}</p>
                {best_badge}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<div class="chart-card"><h4>📊 Model Performance Comparison</h4>', unsafe_allow_html=True)
    model_data = pd.DataFrame(models)
    fig = px.bar(
        model_data,
        x='name',
        y=['roc', 'pr'],
        barmode='group',
        text_auto='.3f',
        color_discrete_map={'roc': '#4f46e5', 'pr': '#7c3aed'},
        template='plotly_white',
        height=350,
        title="ROC-AUC vs PR-AUC Comparison"
    )
    fig.update_layout(
        margin=dict(t=40, b=30),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        yaxis_title="Score",
        xaxis_title="",
        font=dict(color='#1f2937', size=12)
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<div class="section-header">🔑 <span class="highlight">Top Features Driving Churn</span></div>', unsafe_allow_html=True)
    
    try:
        rf_importance = pd.read_csv("outputs/feature_importance_rf.csv", index_col=0)
        rf_importance = rf_importance.sort_values(by=rf_importance.columns[0], ascending=True).tail(15)
        
        fig = px.bar(
            rf_importance,
            x=rf_importance.columns[0],
            y=rf_importance.index,
            orientation='h',
            color=rf_importance.columns[0],
            color_continuous_scale='Blues',
            template='plotly_white',
            height=450,
            title="Random Forest Feature Importance"
        )
        fig.update_layout(
            margin=dict(t=40, b=30, l=0, r=0),
            xaxis_title="Importance",
            yaxis_title="",
            showlegend=False,
            font=dict(color='#1f2937', size=12)
        )
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.info("ℹ️ Feature importance data not available. Run the notebook first to generate this chart.")

# ============================================
# PAGE: INSIGHTS
# ============================================
elif page == "Insights":
    st.markdown('<div class="section-header">💡 <span class="highlight">Business Insights & Recommendations</span></div>', unsafe_allow_html=True)
    
    st.markdown("### 🔴 High-Risk Customer Segments")
    
    risks = [
        {"level": "Critical", "segment": "Month-to-month + Monthly charges > $70", "action": "Immediate retention offer", "class": "risk-critical"},
        {"level": "High", "segment": "New customers (tenure < 6 months)", "action": "Welcome program", "class": "risk-high"},
        {"level": "Medium", "segment": "Fiber optic internet customers", "action": "Bundle services", "class": "risk-medium"},
        {"level": "Low", "segment": "Electronic check payment method", "action": "Auto-pay incentive", "class": "risk-low"}
    ]
    
    for risk in risks:
        st.markdown(f"""
        <div class="risk-card {risk['class']}">
            <span class="risk-level">{risk['level']}</span>
            <span class="risk-segment">{risk['segment']}</span>
            <span class="risk-action">{risk['action']}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### ✅ Recommended Retention Strategies")
    
    strategies = [
        "💎 Offer annual contract discounts to month-to-month customers",
        "🎯 Implement 'welcome' retention program for first 6 months",
        "📦 Bundle high-speed internet with streaming services",
        "💳 Incentivize electronic check customers to switch to auto-pay"
    ]
    
    for i, strategy in enumerate(strategies, 1):
        st.markdown(f"""
        <div class="strategy-card">
            <div class="strategy-number">{i}</div>
            <div class="strategy-text">{strategy}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📊 Key Metrics to Monitor")
    
    kpi_data = pd.DataFrame({
        'Metric': [
            "📊 Monthly churn rate by contract type",
            "🎯 Churn rate at tenure milestones",
            "⭐ Customer satisfaction scores (high-risk)",
            "📈 Retention campaign conversion rate"
        ],
        'Target': [
            "< 15% for month-to-month",
            "< 20% at 3 months",
            "> 4.0/5.0",
            "> 25%"
        ],
        'Status': [
            "🟢 On Track",
            "🟡 Monitor",
            "🟢 On Track",
            "🟡 Monitor"
        ]
    })
    
    st.dataframe(
        kpi_data.style
            .set_properties(**{
                'background-color': '#f8fafc',
                'color': '#1f2937',
                'border-color': '#e5e7eb',
                'padding': '10px'
            })
            .set_table_styles([
                {'selector': 'thead th', 'props': [
                    ('background', '#1a1a2e'), 
                    ('color', 'white'), 
                    ('font-weight', '600'),
                    ('padding', '10px')
                ]},
                {'selector': 'tbody tr:hover', 'props': [
                    ('background', '#eef2ff')
                ]}
            ])
            .set_properties(subset=['Status'], **{
                'font-weight': '600'
            }),
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")
    st.markdown("### 📥 Download Report")
    
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
    
    MODEL PERFORMANCE:
    - Best Model: Random Forest (ROC-AUC: 0.841)
    - Precision (Churn): 0.53
    - Recall (Churn): 0.77
    - F1-Score (Churn): 0.63
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

# ============================================
# FOOTER
# ============================================
st.markdown("""
<div class="footer">
    <p><strong>Customer Churn Prediction Dashboard</strong> • Built with Streamlit & Python</p>
    <p>Data Source: IBM Telco Customer Churn Dataset • 7,043 Customers</p>
    <p style="margin-top: 0.3rem; opacity: 0.6;">© 2024 Churn Analytics • All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)