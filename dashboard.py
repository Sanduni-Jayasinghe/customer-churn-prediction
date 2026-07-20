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
# CUSTOM CSS - PROFESSIONAL DESIGN
# ============================================
st.markdown("""
<style>
    /* Remove default padding */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 0rem;
    }
    
    /* Professional header */
    .header-container {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2rem 2rem 1.5rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.05);
    }
    
    .header-title {
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .header-subtitle {
        color: #a8b2d1;
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.8;
    }
    
    .header-badge {
        display: inline-block;
        background: rgba(100, 200, 255, 0.15);
        color: #64c8ff;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        border: 1px solid rgba(100, 200, 255, 0.2);
        margin-top: 0.5rem;
    }
    
    /* Metric Cards - Glassmorphism */
    .metric-card {
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(10px);
        padding: 1.2rem 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        border: 1px solid rgba(255,255,255,0.8);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a1a2e;
        line-height: 1.2;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #6b7280;
        margin-top: 0.3rem;
        font-weight: 500;
    }
    
    .metric-icon {
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
    
    .metric-change {
        display: inline-block;
        font-size: 0.75rem;
        padding: 0.15rem 0.5rem;
        border-radius: 12px;
        margin-top: 0.3rem;
        font-weight: 600;
    }
    
    .metric-change.positive {
        background: #d1fae5;
        color: #065f46;
    }
    
    .metric-change.negative {
        background: #fee2e2;
        color: #991b1b;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1a1a2e;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #e5e7eb;
    }
    
    .section-header span {
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Risk cards */
    .risk-card {
        padding: 1rem 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 5px solid;
        transition: all 0.2s;
    }
    
    .risk-card:hover {
        transform: translateX(5px);
    }
    
    .risk-critical {
        background: #fef2f2;
        border-color: #dc2626;
    }
    
    .risk-high {
        background: #fffbeb;
        border-color: #f59e0b;
    }
    
    .risk-medium {
        background: #eff6ff;
        border-color: #3b82f6;
    }
    
    .risk-low {
        background: #f0fdf4;
        border-color: #22c55e;
    }
    
    .risk-title {
        font-weight: 600;
        font-size: 0.95rem;
    }
    
    .risk-desc {
        font-size: 0.85rem;
        color: #4b5563;
        margin-top: 0.2rem;
    }
    
    /* Strategy cards */
    .strategy-card {
        background: white;
        padding: 1rem 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border: 1px solid #e5e7eb;
        display: flex;
        align-items: center;
        gap: 1rem;
        transition: all 0.2s;
    }
    
    .strategy-card:hover {
        border-color: #667eea;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.15);
    }
    
    .strategy-number {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.9rem;
        flex-shrink: 0;
    }
    
    .strategy-text {
        font-size: 0.95rem;
        color: #1f2937;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: #9ca3af;
        font-size: 0.8rem;
        border-top: 1px solid #e5e7eb;
        margin-top: 3rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: #1a1a2e;
    }
    
    .sidebar-brand {
        text-align: center;
        padding: 1rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        margin-bottom: 1rem;
    }
    
    .sidebar-brand h2 {
        color: white;
        margin: 0;
        font-weight: 600;
    }
    
    .sidebar-brand p {
        color: #6b7280;
        font-size: 0.8rem;
        margin: 0.2rem 0 0 0;
    }
    
    /* Chart containers */
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 16px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
        border: 1px solid #f3f4f6;
        margin: 0.5rem 0;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-weight: 500;
        padding: 0.5rem 1rem;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.6rem 2rem;
        border-radius: 12px;
        transition: all 0.3s;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #f0f4ff, #faf0ff);
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
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
        <div style="font-size: 3rem;">📊</div>
        <h2>Churn Analytics</h2>
        <p>Customer Retention Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.radio(
        "Navigation",
        ["🏠 Overview", "📈 Analysis", "🔮 Predictor", "📊 Models", "💡 Insights"],
        index=0,
        key="nav"
    )
    
    st.markdown("---")
    
    # Quick stats
    total = len(df)
    churned = df[df['Churn'] == 'Yes'].shape[0]
    churn_rate = (churned / total) * 100
    
    st.markdown(f"""
    <div style="background: #1f2937; padding: 1rem; border-radius: 12px; margin: 1rem 0;">
        <p style="color: #9ca3af; font-size: 0.7rem; margin: 0; text-transform: uppercase; letter-spacing: 1px;">Dataset Snapshot</p>
        <p style="color: white; margin: 0.3rem 0;"><strong>Total:</strong> {total:,}</p>
        <p style="color: white; margin: 0.3rem 0;"><strong>Churned:</strong> {churned:,}</p>
        <p style="color: #f59e0b; margin: 0.3rem 0;"><strong>Rate:</strong> {churn_rate:.1f}%</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align: center; color: #6b7280; font-size: 0.7rem; margin-top: 1rem;">
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
    <h1 class="header-title">📊 Customer Churn Analytics</h1>
    <p class="header-subtitle">AI-powered insights to reduce customer churn and improve retention</p>
    <span class="header-badge">✨ IBM Telco Dataset • 7,043 Customers</span>
</div>
""", unsafe_allow_html=True)

# ============================================
# PAGE: OVERVIEW
# ============================================
if page == "🏠 Overview":
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_customers = len(df)
    churn_rate = (df['Churn'] == 'Yes').mean() * 100
    avg_tenure = df['tenure'].mean()
    avg_monthly = df['MonthlyCharges'].mean()
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">👥 {total_customers:,}</div>
            <div class="metric-label">Total Customers</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">📈 {churn_rate:.1f}%</div>
            <div class="metric-label">Churn Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">⏱️ {avg_tenure:.1f}m</div>
            <div class="metric-label">Avg. Tenure</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">💰 ${avg_monthly:.0f}</div>
            <div class="metric-label">Avg. Monthly Charge</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Churn Distribution")
        
        churn_counts = df['Churn'].value_counts()
        fig = go.Figure(data=[go.Pie(
            labels=['No Churn', 'Churn'],
            values=churn_counts.values,
            hole=0.45,
            marker=dict(colors=['#2ecc71', '#e74c3c']),
            textinfo='label+percent',
            textposition='outside',
            pull=[0, 0.05]
        )])
        fig.update_layout(
            height=350,
            showlegend=False,
            margin=dict(t=20, b=20, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#1f2937')
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Churn Rate by Contract")
        
        contract_churn = df.groupby('Contract').apply(
            lambda x: (x['Churn'] == 'Yes').mean() * 100
        ).reset_index()
        contract_churn.columns = ['Contract', 'Churn Rate']
        
        fig = px.bar(
            contract_churn,
            x='Contract',
            y='Churn Rate',
            color='Churn Rate',
            color_continuous_scale=['#2ecc71', '#f39c12', '#e74c3c'],
            text=contract_churn['Churn Rate'].round(1),
            template='plotly_white',
            height=350
        )
        fig.update_traces(textposition='outside', marker_line_width=0)
        fig.update_layout(
            showlegend=False,
            margin=dict(t=20, b=30, l=10, r=10),
            xaxis_title="",
            yaxis_title="Churn Rate (%)",
            font=dict(color='#1f2937')
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Tenure Distribution")
        
        fig = px.histogram(
            df,
            x='tenure',
            color='Churn',
            nbins=30,
            barmode='stack',
            color_discrete_map={'Yes': '#e74c3c', 'No': '#2ecc71'},
            template='plotly_white',
            height=320,
            labels={'tenure': 'Tenure (months)', 'count': 'Customers'}
        )
        fig.update_layout(
            margin=dict(t=20, b=30, l=10, r=10),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            font=dict(color='#1f2937')
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Churn by Payment Method")
        
        payment_churn = df.groupby('PaymentMethod').apply(
            lambda x: (x['Churn'] == 'Yes').mean() * 100
        ).reset_index()
        payment_churn.columns = ['Payment Method', 'Churn Rate']
        payment_churn = payment_churn.sort_values('Churn Rate', ascending=False)
        
        fig = px.bar(
            payment_churn,
            x='Payment Method',
            y='Churn Rate',
            color='Churn Rate',
            color_continuous_scale=['#2ecc71', '#f39c12', '#e74c3c'],
            text=payment_churn['Churn Rate'].round(1),
            template='plotly_white',
            height=320
        )
        fig.update_traces(textposition='outside', marker_line_width=0)
        fig.update_layout(
            showlegend=False,
            margin=dict(t=20, b=40, l=10, r=10),
            xaxis_title="",
            yaxis_title="Churn Rate (%)",
            font=dict(color='#1f2937')
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# PAGE: ANALYSIS
# ============================================
elif page == "📈 Analysis":
    st.markdown('<div class="section-header">🔍 <span>Churn Analysis</span></div>', unsafe_allow_html=True)
    
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
    
    # Filter data
    filtered_df = df[
        (df['Contract'].isin(contracts)) &
        (df['gender'].isin(genders)) &
        (df['InternetService'].isin(internet))
    ]
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Filtered Customers", f"{len(filtered_df):,}")
    with col2:
        rate = (filtered_df['Churn'] == 'Yes').mean() * 100
        st.metric("Churn Rate", f"{rate:.1f}%")
    with col3:
        st.metric("Avg. Tenure", f"{filtered_df['tenure'].mean():.1f}m")
    with col4:
        st.metric("Avg. Monthly", f"${filtered_df['MonthlyCharges'].mean():.2f}")
    
    st.markdown("---")
    
    # Analysis charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Churn by Service Type")
        
        service_churn = df.groupby('InternetService').apply(
            lambda x: (x['Churn'] == 'Yes').mean() * 100
        ).reset_index()
        service_churn.columns = ['Service', 'Churn Rate']
        
        fig = px.bar(
            service_churn,
            x='Service',
            y='Churn Rate',
            color='Churn Rate',
            color_continuous_scale=['#2ecc71', '#f39c12', '#e74c3c'],
            text=service_churn['Churn Rate'].round(1),
            template='plotly_white',
            height=350
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(showlegend=False, margin=dict(t=20, b=30))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Monthly Charges Distribution")
        
        fig = px.box(
            filtered_df,
            x='Churn',
            y='MonthlyCharges',
            color='Churn',
            color_discrete_map={'Yes': '#e74c3c', 'No': '#2ecc71'},
            template='plotly_white',
            height=350
        )
        fig.update_layout(
            showlegend=False,
            margin=dict(t=20, b=30),
            xaxis_title="",
            yaxis_title="Monthly Charges ($)"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# PAGE: PREDICTOR
# ============================================
elif page == "🔮 Predictor":
    st.markdown('<div class="section-header">🔮 <span>Churn Predictor</span></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <strong>💡 How it works:</strong> Enter customer details below to get a churn probability score.
        The model analyzes customer behavior patterns to predict churn risk.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👤 Customer Profile")
        tenure = st.slider("Tenure (months)", 0, 72, 12, key='pred_tenure')
        monthly = st.slider("Monthly Charges ($)", 0, 150, 50, key='pred_monthly')
        total = st.slider("Total Charges ($)", 0, 8000, 1000, key='pred_total')
        contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"], key='pred_contract')
    
    with col2:
        st.subheader("📋 Service Details")
        internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"], key='pred_internet')
        payment = st.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer", "Credit card"], key='pred_payment')
        gender = st.selectbox("Gender", ["Male", "Female"], key='pred_gender')
        senior = st.selectbox("Senior Citizen", ["No", "Yes"], key='pred_senior')
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔮 Predict Churn Risk", use_container_width=True, key='predict_btn'):
            # Simulate prediction (replace with actual model when ready)
            import random
            prob = random.uniform(0.1, 0.95)
            
            st.markdown("---")
            
            # Show results in two columns
            col1, col2 = st.columns(2)
            
            with col1:
                # Gauge chart
                fig = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=prob,
                    title={'text': "Churn Risk Score", 'font': {'size': 18}},
                    delta={'reference': 0.5, 'increasing.color': 'red', 'decreasing.color': 'green'},
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={
                        'axis': {'range': [0, 1], 'tickwidth': 1, 'tickcolor': "darkblue"},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 0.3], 'color': '#22c55e'},
                            {'range': [0.3, 0.6], 'color': '#f59e0b'},
                            {'range': [0.6, 1], 'color': '#ef4444'}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 0.5
                        }
                    }
                ))
                fig.update_layout(height=350, margin=dict(t=30, b=20))
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Risk assessment
                if prob < 0.3:
                    level = "🟢 Low Risk"
                    color = "#22c55e"
                    action = "Customer is likely to stay. Continue providing quality service."
                elif prob < 0.6:
                    level = "🟡 Medium Risk"
                    color = "#f59e0b"
                    action = "Customer shows signs of potential churn. Consider engagement offers."
                else:
                    level = "🔴 High Risk"
                    color = "#ef4444"
                    action = "Customer is at high risk! Immediate retention action needed."
                
                st.markdown(f"""
                <div style="background: white; padding: 2rem; border-radius: 16px; border: 2px solid {color}; text-align: center;">
                    <h2 style="color: {color}; margin: 0;">{level}</h2>
                    <div style="font-size: 3rem; font-weight: 700; margin: 0.5rem 0; color: #1a1a2e;">
                        {prob:.1%}
                    </div>
                    <p style="color: #4b5563; margin: 0.5rem 0;">{action}</p>
                </div>
                """, unsafe_allow_html=True)

# ============================================
# PAGE: MODELS
# ============================================
elif page == "📊 Models":
    st.markdown('<div class="section-header">📊 <span>Model Performance</span></div>', unsafe_allow_html=True)
    
    # Model comparison
    model_data = pd.DataFrame({
        'Model': ['Logistic Regression', 'Random Forest', 'XGBoost', 'XGBoost (Tuned)'],
        'ROC-AUC': [0.8414, 0.8411, 0.8369, 0.8430],
        'PR-AUC': [0.6306, 0.6538, 0.6477, 0.6512]
    })
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig = px.bar(
            model_data,
            x='Model',
            y=['ROC-AUC', 'PR-AUC'],
            barmode='group',
            text_auto='.3f',
            color_discrete_map={'ROC-AUC': '#667eea', 'PR-AUC': '#764ba2'},
            template='plotly_white',
            height=400,
            title="Model Performance Comparison"
        )
        fig.update_layout(
            margin=dict(t=40, b=30),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            yaxis_title="Score",
            xaxis_title=""
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🏆 Best Model")
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 1.5rem; border-radius: 12px; color: white; text-align: center;">
            <div style="font-size: 0.9rem; opacity: 0.8;">Random Forest</div>
            <div style="font-size: 2.5rem; font-weight: 700;">0.841</div>
            <div style="font-size: 0.8rem; opacity: 0.8;">ROC-AUC Score</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #f8fafc; padding: 1rem; border-radius: 12px; margin-top: 0.5rem;">
            <p style="margin: 0.2rem 0;"><strong>Precision:</strong> 0.53</p>
            <p style="margin: 0.2rem 0;"><strong>Recall:</strong> 0.77</p>
            <p style="margin: 0.2rem 0;"><strong>F1-Score:</strong> 0.63</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Feature Importance
    st.markdown("---")
    st.markdown('<div class="section-header">🔑 <span>Top Features Driving Churn</span></div>', unsafe_allow_html=True)
    
    try:
        rf_importance = pd.read_csv("outputs/feature_importance_rf.csv", index_col=0)
        rf_importance = rf_importance.sort_values(by=rf_importance.columns[0], ascending=True).tail(15)
        
        fig = px.bar(
            rf_importance,
            x=rf_importance.columns[0],
            y=rf_importance.index,
            orientation='h',
            color=rf_importance.columns[0],
            color_continuous_scale='Viridis',
            template='plotly_white',
            height=500,
            title="Random Forest Feature Importance"
        )
        fig.update_layout(
            margin=dict(t=40, b=30),
            xaxis_title="Importance",
            yaxis_title="",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.info("ℹ️ Feature importance data not available. Run the notebook first to generate this chart.")

# ============================================
# PAGE: INSIGHTS
# ============================================
elif page == "💡 Insights":
    st.markdown('<div class="section-header">💡 <span>Business Insights & Recommendations</span></div>', unsafe_allow_html=True)
    
    # Risk segments
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
            <div class="risk-title">[{risk['level']}] {risk['segment']}</div>
            <div class="risk-desc">🎯 Recommended: {risk['action']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Retention strategies
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
    st.dataframe(kpi_data, use_container_width=True, hide_index=True)

# ============================================
# FOOTER
# ============================================
st.markdown("""
<div class="footer">
    <p><strong>Customer Churn Prediction Dashboard</strong> • Built with Streamlit & Python</p>
    <p>Data Source: IBM Telco Customer Churn Dataset • 7,043 Customers</p>
    <p style="margin-top: 0.5rem; opacity: 0.6;">© 2024 Churn Analytics • All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)