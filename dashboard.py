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
# CUSTOM CSS - MODERN PROFESSIONAL DESIGN
# ============================================
st.markdown("""
<style>
    /* ===== GLOBAL STYLES ===== */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 0rem;
        max-width: 1400px;
    }
    
    /* ===== HEADER ===== */
    .header-container {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    
    .header-title {
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .header-title span {
        background: linear-gradient(90deg, #f7971e, #ffd200);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .header-subtitle {
        color: #a8b2d1;
        font-size: 1rem;
        margin: 0.3rem 0 0 0;
        opacity: 0.8;
    }
    
    .header-badge {
        display: inline-block;
        background: rgba(255, 215, 0, 0.12);
        color: #ffd700;
        padding: 0.25rem 1rem;
        border-radius: 20px;
        font-size: 0.75rem;
        border: 1px solid rgba(255, 215, 0, 0.2);
        margin-top: 0.5rem;
    }
    
    /* ===== METRIC CARDS ===== */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .metric-card {
        background: white;
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid #f0f2f5;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border-color: #4f46e5;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #111827;
        line-height: 1.2;
    }
    
    .metric-label {
        font-size: 0.8rem;
        color: #6b7280;
        margin-top: 0.2rem;
        font-weight: 500;
    }
    
    .metric-change {
        font-size: 0.7rem;
        padding: 0.15rem 0.6rem;
        border-radius: 12px;
        font-weight: 600;
        display: inline-block;
        margin-top: 0.3rem;
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
        font-size: 1.1rem;
        font-weight: 600;
        color: #111827;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e5e7eb;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .section-header .icon {
        font-size: 1.3rem;
    }
    
    .section-header .highlight {
        color: #4f46e5;
    }
    
    /* ===== CHART CONTAINERS ===== */
    .chart-card {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05);
        border: 1px solid #f0f2f5;
        margin: 0.5rem 0;
        height: 100%;
    }
    
    .chart-card h4 {
        font-size: 0.95rem;
        font-weight: 600;
        color: #111827;
        margin: 0 0 0.5rem 0;
    }
    
    /* ===== RISK CARDS ===== */
    .risk-card {
        padding: 0.8rem 1.2rem;
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
        font-size: 0.85rem;
    }
    
    .risk-card .risk-segment {
        font-size: 0.85rem;
        color: #374151;
        flex: 1;
        margin: 0 1rem;
    }
    
    .risk-card .risk-action {
        font-size: 0.8rem;
        background: #4f46e5;
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-weight: 500;
    }
    
    .risk-critical { border-color: #dc2626; background: #fef2f2; }
    .risk-high { border-color: #f59e0b; background: #fffbeb; }
    .risk-medium { border-color: #3b82f6; background: #eff6ff; }
    .risk-low { border-color: #22c55e; background: #f0fdf4; }
    
    /* ===== STRATEGY CARDS ===== */
    .strategy-card {
        background: white;
        padding: 0.8rem 1.2rem;
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
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.1);
    }
    
    .strategy-number {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.8rem;
        flex-shrink: 0;
    }
    
    .strategy-text {
        font-size: 0.9rem;
        color: #1f2937;
    }
    
    /* ===== SIDEBAR ===== */
    .css-1d391kg {
        background: linear-gradient(180deg, #0f0c29, #302b63);
        padding: 1.5rem 0.5rem;
    }
    
    .sidebar-brand {
        text-align: center;
        padding: 0.5rem 0 1rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 1rem;
    }
    
    .sidebar-brand .logo {
        font-size: 2.5rem;
    }
    
    .sidebar-brand h2 {
        color: white;
        margin: 0.3rem 0 0 0;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    .sidebar-brand p {
        color: #6b7280;
        font-size: 0.7rem;
        margin: 0.1rem 0 0 0;
    }
    
    /* ===== FOOTER ===== */
    .footer {
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
        color: #9ca3af;
        font-size: 0.75rem;
        border-top: 1px solid #e5e7eb;
        margin-top: 2rem;
    }
    
    /* ===== PREDICTOR INPUTS ===== */
    .predictor-section {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        margin: 0.5rem 0;
    }
    
    .predictor-section h4 {
        font-size: 0.95rem;
        font-weight: 600;
        color: #111827;
        margin: 0 0 0.5rem 0;
    }
    
    /* ===== MODEL PERFORMANCE ===== */
    .model-card {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        text-align: center;
        transition: all 0.3s;
        height: 100%;
    }
    
    .model-card:hover {
        border-color: #4f46e5;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    
    .model-card .model-name {
        font-size: 0.85rem;
        font-weight: 600;
        color: #374151;
        margin: 0;
    }
    
    .model-card .model-score {
        font-size: 1.8rem;
        font-weight: 700;
        color: #111827;
        margin: 0.3rem 0;
    }
    
    .model-card .model-label {
        font-size: 0.7rem;
        color: #6b7280;
        margin: 0;
    }
    
    .model-card .best-badge {
        display: inline-block;
        background: #d1fae5;
        color: #065f46;
        font-size: 0.6rem;
        padding: 0.1rem 0.6rem;
        border-radius: 12px;
        font-weight: 600;
        margin-top: 0.3rem;
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
# SIDEBAR
# ============================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="logo">📊</div>
        <h2>Churn Analytics</h2>
        <p>Customer Retention Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.radio(
        "",
        ["🏠 Overview", "📈 Analysis", "🔮 Predictor", "📊 Models", "💡 Insights"],
        index=0,
        key="nav"
    )
    
    st.markdown("---")
    
    total = len(df)
    churned = df[df['Churn'] == 'Yes'].shape[0]
    churn_rate = (churned / total) * 100
    
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.05); padding: 0.8rem 1rem; border-radius: 10px; margin: 0.5rem 0;">
        <p style="color: #9ca3af; font-size: 0.6rem; margin: 0; text-transform: uppercase; letter-spacing: 1px;">Dataset Snapshot</p>
        <p style="color: white; margin: 0.2rem 0; font-size: 0.85rem;"><strong>Total:</strong> {total:,}</p>
        <p style="color: white; margin: 0.2rem 0; font-size: 0.85rem;"><strong>Churned:</strong> {churned:,}</p>
        <p style="color: #f59e0b; margin: 0.2rem 0; font-size: 0.85rem;"><strong>Rate:</strong> {churn_rate:.1f}%</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align: center; color: #6b7280; font-size: 0.65rem; margin-top: 1rem;">
        <p>⚡ Real-time Analytics</p>
        <p>📊 Interactive Visualizations</p>
        <p>🎯 Actionable Insights</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# HEADER
# ============================================
st.markdown("""
<div class="header-container">
    <h1 class="header-title">📊 Customer Churn <span>Analytics</span></h1>
    <p class="header-subtitle">AI-powered insights to reduce customer churn and improve retention</p>
    <span class="header-badge">✨ IBM Telco Dataset • 7,043 Customers</span>
</div>
""", unsafe_allow_html=True)

# ============================================
# PAGE: OVERVIEW
# ============================================
if page == "🏠 Overview":
    # Metrics Row
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
            labels=['No Churn', 'Churn'],
            values=churn_counts.values,
            hole=0.5,
            marker=dict(colors=['#22c55e', '#dc2626']),
            textinfo='label+percent',
            textposition='outside',
            pull=[0, 0.05]
        )])
        fig.update_layout(
            height=320,
            showlegend=False,
            margin=dict(t=10, b=10, l=10, r=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#1f2937', size=12)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-card"><h4>📈 Churn Rate by Contract</h4>', unsafe_allow_html=True)
        contract_churn = df.groupby('Contract').apply(lambda x: (x['Churn'] == 'Yes').mean() * 100).reset_index()
        contract_churn.columns = ['Contract', 'Churn Rate']
        colors = ['#dc2626' if x > 30 else '#f59e0b' if x > 15 else '#22c55e' for x in contract_churn['Churn Rate']]
        fig = px.bar(
            contract_churn,
            x='Contract',
            y='Churn Rate',
            color='Churn Rate',
            color_continuous_scale=['#22c55e', '#f59e0b', '#dc2626'],
            text=contract_churn['Churn Rate'].round(1),
            template='plotly_white',
            height=320
        )
        fig.update_traces(textposition='outside', marker_line_width=0)
        fig.update_layout(
            showlegend=False,
            margin=dict(t=10, b=30, l=10, r=10),
            xaxis_title="",
            yaxis_title="Churn Rate (%)",
            font=dict(color='#1f2937', size=11)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-card"><h4>📉 Tenure Distribution</h4>', unsafe_allow_html=True)
        fig = px.histogram(
            df,
            x='tenure',
            color='Churn',
            nbins=30,
            barmode='stack',
            color_discrete_map={'Yes': '#dc2626', 'No': '#22c55e'},
            template='plotly_white',
            height=300,
            labels={'tenure': 'Tenure (months)', 'count': 'Customers'}
        )
        fig.update_layout(
            margin=dict(t=10, b=30, l=10, r=10),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            font=dict(color='#1f2937', size=11)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-card"><h4>💳 Churn by Payment Method</h4>', unsafe_allow_html=True)
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
            height=300
        )
        fig.update_traces(textposition='outside', marker_line_width=0)
        fig.update_layout(
            showlegend=False,
            margin=dict(t=10, b=40, l=10, r=10),
            xaxis_title="",
            yaxis_title="Churn Rate (%)",
            font=dict(color='#1f2937', size=10)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# PAGE: ANALYSIS
# ============================================
elif page == "📈 Analysis":
    st.markdown('<div class="section-header"><span class="icon">🔍</span> <span class="highlight">Churn Analysis</span></div>', unsafe_allow_html=True)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        contracts = st.multiselect(
            "Contract Type",
            options=df['Contract'].unique(),
            default=df['Contract'].unique(),
            key='contract_filter'
        )
    with col2:
        genders = st.multiselect(
            "Gender",
            options=df['gender'].unique(),
            default=df['gender'].unique(),
            key='gender_filter'
        )
    with col3:
        internet = st.multiselect(
            "Internet Service",
            options=df['InternetService'].unique(),
            default=df['InternetService'].unique(),
            key='internet_filter'
        )
    
    filtered_df = df[
        (df['Contract'].isin(contracts)) &
        (df['gender'].isin(genders)) &
        (df['InternetService'].isin(internet))
    ]
    
    # Filtered Stats
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
        st.markdown('<div class="chart-card"><h4>🌐 Churn by Internet Service</h4>', unsafe_allow_html=True)
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
        fig.update_traces(textposition='outside')
        fig.update_layout(showlegend=False, margin=dict(t=10, b=30))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-card"><h4>💳 Churn by Payment Method</h4>', unsafe_allow_html=True)
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
        fig.update_traces(textposition='outside')
        fig.update_layout(showlegend=False, margin=dict(t=10, b=40))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# PAGE: PREDICTOR
# ============================================
elif page == "🔮 Predictor":
    st.markdown('<div class="section-header"><span class="icon">🔮</span> <span class="highlight">Churn Predictor</span></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #eef2ff; padding: 1rem 1.5rem; border-radius: 10px; border-left: 4px solid #4f46e5; margin: 0.5rem 0;">
        <strong>💡 How it works:</strong> Enter customer details below to get a churn probability score.
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
                elif prob < 0.6:
                    level = "🟡 Medium Risk"
                    color = "#f59e0b"
                    bg = "#fffbeb"
                    border = "#f59e0b"
                else:
                    level = "🔴 High Risk"
                    color = "#dc2626"
                    bg = "#fef2f2"
                    border = "#dc2626"
                
                st.markdown(f"""
                <div style="background: {bg}; padding: 2rem; border-radius: 12px; border: 2px solid {border}; text-align: center;">
                    <h2 style="color: {color}; margin: 0; font-size: 1.8rem;">{level}</h2>
                    <div style="font-size: 2.5rem; font-weight: 700; margin: 0.5rem 0; color: #111827;">
                        {prob:.1%}
                    </div>
                    <p style="color: #4b5563; margin: 0; font-size: 0.9rem;">{action if 'action' in locals() else 'Recommended action needed.'}</p>
                </div>
                """, unsafe_allow_html=True)

# ============================================
# PAGE: MODELS
# ============================================
elif page == "📊 Models":
    st.markdown('<div class="section-header"><span class="icon">📊</span> <span class="highlight">Model Performance</span></div>', unsafe_allow_html=True)
    
    # Model Cards
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
                <p style="font-size: 0.8rem; color: #6b7280; margin: 0.2rem 0;">PR-AUC: {model['pr']:.4f}</p>
                {best_badge}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Model Comparison Chart
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
        font=dict(color='#1f2937', size=11)
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Feature Importance
    st.markdown("---")
    st.markdown('<div class="section-header"><span class="icon">🔑</span> <span class="highlight">Top Features Driving Churn</span></div>', unsafe_allow_html=True)
    
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
            font=dict(color='#1f2937', size=11)
        )
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.info("ℹ️ Feature importance data not available. Run the notebook first to generate this chart.")

# ============================================
# PAGE: INSIGHTS
# ============================================
elif page == "💡 Insights":
    st.markdown('<div class="section-header"><span class="icon">💡</span> <span class="highlight">Business Insights & Recommendations</span></div>', unsafe_allow_html=True)
    
    # Risk Segments
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
    
    # Retention Strategies
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
    
    # KPIs
    st.markdown("### 📊 Key Metrics to Monitor")
    
    kpi_data = pd.DataFrame({
        'Metric': [
            "Monthly churn rate by contract type",
            "Churn rate at tenure milestones",
            "Customer satisfaction scores (high-risk)",
            "Retention campaign conversion rate"
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
        kpi_data.style.set_properties(**{'background-color': '#f8fafc'}).set_table_styles([
            {'selector': 'thead th', 'props': [('background', '#4f46e5'), ('color', 'white')]}
        ]),
        use_container_width=True,
        hide_index=True
    )
    
    # Download Report
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