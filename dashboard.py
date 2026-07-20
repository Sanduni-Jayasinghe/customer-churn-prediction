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
# CUSTOM CSS - FULLY PROFESSIONAL OVERHAUL
# ============================================
st.markdown("""
<style>
    /* ===== SIDEBAR STYLING ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29 0%, #1a1a3e 50%, #24243e 100%);
        padding: 0;
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    section[data-testid="stSidebar"] .css-1d391kg {
        padding: 1rem 0.5rem;
    }

    /* Sidebar Brand */
    .sidebar-brand {
        text-align: center;
        padding: 1.5rem 0 1.2rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 1.5rem;
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

    /* ===== NAVIGATION OVERHAUL ===== */
    /* Hide the default radio button completely */
    .stRadio > div {
        gap: 0.2rem;
    }

    .stRadio label {
        display: flex !important;
        align-items: center !important;
        gap: 0.8rem !important;
        padding: 0.65rem 1rem !important;
        margin: 0.15rem 0 !important;
        border-radius: 10px !important;
        background: transparent !important;
        transition: all 0.25s ease !important;
        cursor: pointer !important;
        border: none !important;
        color: #9ca3af !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        position: relative !important;
    }

    .stRadio label:hover {
        background: rgba(255,255,255,0.06) !important;
        color: #ffffff !important;
    }

    /* Active state - professional highlight */
    .stRadio label[data-checked="true"] {
        background: rgba(79, 70, 229, 0.2) !important;
        color: #ffffff !important;
        border-left: 3px solid #4f46e5 !important;
        border-radius: 0 10px 10px 0 !important;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.1) !important;
    }

    .stRadio label[data-checked="true"] .nav-icon {
        color: #4f46e5 !important;
    }

    /* Hide the original radio circle */
    .stRadio label > div:first-child {
        display: none !important;
    }

    /* Style the text container */
    .stRadio label > div:last-child {
        flex: 1;
        display: flex !important;
        align-items: center !important;
        gap: 0.8rem !important;
    }

    /* ===== SIDEBAR STATS ===== */
    .sidebar-stats {
        background: rgba(255,255,255,0.04);
        padding: 0.8rem 1rem;
        border-radius: 10px;
        margin: 1.5rem 0.5rem;
        border: 1px solid rgba(255,255,255,0.04);
    }

    .sidebar-stats p {
        color: #9ca3af;
        font-size: 0.6rem;
        margin: 0 0 0.4rem 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .sidebar-stats .stat-value {
        color: #e5e7eb;
        font-size: 0.85rem;
        margin: 0.1rem 0;
        font-weight: 400;
    }

    .sidebar-stats .stat-value strong {
        color: #ffffff;
        font-weight: 600;
    }

    .sidebar-stats .stat-highlight {
        color: #f59e0b;
        font-weight: 600;
    }

    .sidebar-footer {
        text-align: center;
        color: #6b7280;
        font-size: 0.6rem;
        margin-top: 1.5rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255,255,255,0.04);
        line-height: 1.8;
    }
    .sidebar-footer .emoji { font-size: 0.8rem; }

    /* ===== MAIN CONTENT STYLING ===== */
    /* Header */
    .header-container {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        padding: 1.8rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.06);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    .header-title { color: #ffffff; font-size: 2rem; font-weight: 700; margin: 0; letter-spacing: -0.5px; }
    .header-title .highlight { background: linear-gradient(90deg, #f7971e, #ffd200); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
    .header-subtitle { color: #a8b2d1; font-size: 0.95rem; margin: 0.3rem 0 0 0; opacity: 0.8; }
    .header-badge { display: inline-block; background: rgba(255, 215, 0, 0.1); color: #ffd700; padding: 0.2rem 1rem; border-radius: 20px; font-size: 0.7rem; border: 1px solid rgba(255, 215, 0, 0.15); margin-top: 0.5rem; }

    /* Metric Cards */
    .metric-card {
        background: #ffffff;
        padding: 1rem 1.2rem;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05);
        border: 1px solid #f1f3f5;
        transition: all 0.25s ease;
        height: 100%;
    }
    .metric-card:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(0,0,0,0.08); border-color: #4f46e5; }
    .metric-value { font-size: 1.8rem; font-weight: 700; color: #111827; line-height: 1.2; }
    .metric-label { font-size: 0.75rem; color: #6b7280; margin-top: 0.2rem; font-weight: 500; }
    .metric-change { font-size: 0.65rem; padding: 0.1rem 0.5rem; border-radius: 12px; font-weight: 600; display: inline-block; margin-top: 0.2rem; }
    .metric-change.up { background: #d1fae5; color: #065f46; }
    .metric-change.down { background: #fee2e2; color: #991b1b; }

    /* Section Headers */
    .section-header { font-size: 1.1rem; font-weight: 600; color: #111827; margin: 1.5rem 0 1rem 0; padding-bottom: 0.5rem; border-bottom: 2px solid #e5e7eb; display: flex; align-items: center; gap: 0.5rem; }
    .section-header .highlight { color: #4f46e5; }

    /* Chart Cards */
    .chart-card { background: #ffffff; padding: 1rem 1.2rem 1.2rem 1.2rem; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.04); border: 1px solid #f1f3f5; margin: 0.5rem 0; height: 100%; }
    .chart-card h4 { font-size: 0.9rem; font-weight: 600; color: #111827; margin: 0 0 0.5rem 0; }

    /* Risk Cards */
    .risk-card { padding: 0.7rem 1.2rem; border-radius: 10px; margin: 0.4rem 0; border-left: 4px solid; display: flex; justify-content: space-between; align-items: center; background: #fafafa; }
    .risk-card .risk-level { font-weight: 600; font-size: 0.8rem; min-width: 70px; }
    .risk-card .risk-segment { font-size: 0.85rem; color: #374151; flex: 1; margin: 0 1rem; }
    .risk-card .risk-action { font-size: 0.75rem; background: #4f46e5; color: white; padding: 0.15rem 0.8rem; border-radius: 20px; font-weight: 500; white-space: nowrap; }
    .risk-critical { border-color: #dc2626; background: #fef2f2; }
    .risk-high { border-color: #f59e0b; background: #fffbeb; }
    .risk-medium { border-color: #3b82f6; background: #eff6ff; }
    .risk-low { border-color: #22c55e; background: #f0fdf4; }

    /* Strategy Cards */
    .strategy-card { background: white; padding: 0.7rem 1.2rem; border-radius: 10px; margin: 0.4rem 0; border: 1px solid #e5e7eb; display: flex; align-items: center; gap: 1rem; transition: all 0.2s; }
    .strategy-card:hover { border-color: #4f46e5; box-shadow: 0 4px 15px rgba(79, 70, 229, 0.08); }
    .strategy-number { background: linear-gradient(135deg, #4f46e5, #7c3aed); color: white; width: 26px; height: 26px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.75rem; flex-shrink: 0; }
    .strategy-text { font-size: 0.85rem; color: #1f2937; }

    /* Predictor */
    .predictor-section { background: #f8fafc; padding: 1.2rem 1.5rem; border-radius: 12px; border: 1px solid #e5e7eb; margin: 0.5rem 0; }
    .predictor-section h4 { font-size: 0.9rem; font-weight: 600; color: #111827; margin: 0 0 0.5rem 0; }

    /* Model Cards */
    .model-card { background: white; padding: 1rem; border-radius: 12px; border: 1px solid #e5e7eb; text-align: center; transition: all 0.3s; height: 100%; }
    .model-card:hover { border-color: #4f46e5; box-shadow: 0 4px 20px rgba(0,0,0,0.06); }
    .model-card .model-name { font-size: 0.8rem; font-weight: 600; color: #374151; margin: 0; }
    .model-card .model-score { font-size: 1.6rem; font-weight: 700; color: #111827; margin: 0.2rem 0; }
    .model-card .model-label { font-size: 0.65rem; color: #6b7280; margin: 0; }
    .model-card .best-badge { display: inline-block; background: #d1fae5; color: #065f46; font-size: 0.55rem; padding: 0.1rem 0.6rem; border-radius: 12px; font-weight: 600; margin-top: 0.2rem; }

    /* Footer */
    .footer { text-align: center; padding: 1.2rem 0 0.5rem 0; color: #9ca3af; font-size: 0.7rem; border-top: 1px solid #e5e7eb; margin-top: 2rem; }
    .footer strong { color: #4b5563; }
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
# SIDEBAR - PROFESSIONAL NAVIGATION
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
    
    # Navigation - Clean radio with custom labels
    # Using format_func to add icons and style
    nav_options = ["Overview", "Analysis", "Predictor", "Models", "Insights"]
    nav_icons = ["🏠", "📈", "🔮", "📊", "💡"]
    
    # Create the radio with formatted labels
    # The key is using format_func to add icons, and CSS to hide the radio circle
    page_index = st.radio(
        label="",
        options=range(len(nav_options)),
        format_func=lambda i: f"{nav_icons[i]} {nav_options[i]}",
        index=0,
        key="nav_radio"
    )
    page = nav_options[page_index]

    # Dataset Stats
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
# PAGE LOGIC (SAME AS BEFORE, KEPT CONCISE FOR BREVITY)
# ============================================
if page == "Overview":
    # ... (Your existing Overview code) ...
    st.info("Overview page content goes here. Place your existing code for this section.")

elif page == "Analysis":
    # ... (Your existing Analysis code) ...
    st.info("Analysis page content goes here. Place your existing code for this section.")

elif page == "Predictor":
    # ... (Your existing Predictor code) ...
    st.info("Predictor page content goes here. Place your existing code for this section.")

elif page == "Models":
    # ... (Your existing Models code) ...
    st.info("Models page content goes here. Place your existing code for this section.")

elif page == "Insights":
    # ... (Your existing Insights code) ...
    st.info("Insights page content goes here. Place your existing code for this section.")

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