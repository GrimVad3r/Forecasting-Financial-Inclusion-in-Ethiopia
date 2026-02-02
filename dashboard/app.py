"""
Ethiopia Financial Inclusion Forecasting Dashboard
===================================================

A comprehensive interactive dashboard for exploring financial inclusion 
trends, event impacts, and forecasts for 2025-2027.

Author: Selam Analytics
Date: February 2026
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
from datetime import datetime
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Streamlit page
st.set_page_config(
    page_title="Ethiopia Financial Inclusion Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
    <style>
    :root {
        --primary-color: #1E3A8A;
        --secondary-color: #F97316;
        --accent-color: #06B6D4;
        --success-color: #10B981;
        --warning-color: #F59E0B;
        --danger-color: #EF4444;
        --light-bg: #F3F4F6;
        --dark-bg: #111827;
    }
    
    .main {
        max-width: 1400px;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .insight-box {
        background-color: #EFF6FF;
        border-left: 4px solid #3B82F6;
        padding: 12px;
        border-radius: 6px;
        margin: 8px 0;
    }
    
    .forecast-box {
        background-color: #ECFDF5;
        border-left: 4px solid #10B981;
        padding: 12px;
        border-radius: 6px;
        margin: 8px 0;
    }
    
    .warning-box {
        background-color: #FFFBEB;
        border-left: 4px solid #F59E0B;
        padding: 12px;
        border-radius: 6px;
        margin: 8px 0;
    }
    
    h1 {
        color: #1E3A8A;
        font-size: 2.5rem;
        margin-bottom: 10px;
    }
    
    h2 {
        color: #1E40AF;
        font-size: 1.8rem;
        margin-top: 30px;
        margin-bottom: 15px;
    }
    
    h3 {
        color: #1E40AF;
        font-size: 1.3rem;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# DATA LOADING
# =============================================================================

@st.cache_data
def load_forecast_data():
    """Load forecast data from CSV."""
    try:
        # Try to load from processed data
        df = pd.read_csv('data/processed/forecasts_2025_2027.csv')
        logger.info("Loaded forecasts from processed data")
        return df
    except FileNotFoundError:
        logger.warning("Forecast file not found, using sample data")
        # Return sample data if file doesn't exist
        return create_sample_forecast_data()

@st.cache_data
def load_scenarios():
    """Load scenario data from JSON."""
    try:
        with open('data/processed/forecast_scenarios.json') as f:
            scenarios = json.load(f)
        logger.info("Loaded scenarios from JSON")
        return scenarios
    except FileNotFoundError:
        logger.warning("Scenarios file not found, using defaults")
        return create_sample_scenarios()

@st.cache_data
def load_association_matrix():
    """Load event-indicator association matrix."""
    try:
        df = pd.read_csv('data/processed/event_indicator_association_matrix.csv', index_col=0)
        logger.info("Loaded association matrix")
        return df
    except FileNotFoundError:
        logger.warning("Association matrix not found, using sample")
        return create_sample_matrix()

# =============================================================================
# SAMPLE DATA GENERATORS
# =============================================================================

def create_sample_forecast_data():
    """Create sample forecast data if file not available."""
    return pd.DataFrame({
        'Year': [2025, 2026, 2027],
        'Account_Ownership_%': [52.0, 54.0, 57.0],
        'Ownership_CI_Lower': [50.0, 52.0, 54.0],
        'Ownership_CI_Upper': [54.0, 56.0, 60.0],
        'Digital_Payment_%': [40.0, 43.0, 46.0],
        'Payment_CI_Lower': [37.0, 40.0, 42.0],
        'Payment_CI_Upper': [43.0, 46.0, 50.0]
    })

def create_sample_scenarios():
    """Create sample scenario data."""
    return {
        'scenarios': {
            'Pessimistic': [50, 52, 54],
            'Base': [52, 54, 57],
            'Optimistic': [55, 59, 62]
        },
        'years': [2025, 2026, 2027]
    }

def create_sample_matrix():
    """Create sample association matrix."""
    return pd.DataFrame({
        'ACC_OWNERSHIP': ['+15%', '-', '-', '+10%', '-'],
        'ACC_MM_ACCOUNT': ['+25%', '-', '+5%', '-', '-'],
        'USG_DIGITAL_PAY': ['-', '-', '+8%', '-', '-'],
        'ACC_4G_COV': ['-', '+15%', '-', '-', '-']
    }, index=['Telebirr', 'Safaricom', 'M-Pesa', 'Fayda ID', 'FX Reform'])

# =============================================================================
# VISUALIZATION FUNCTIONS
# =============================================================================

def create_access_forecast_chart(forecast_df, scenarios):
    """Create interactive access forecast chart."""
    fig = go.Figure()
    
    # Historical data point
    fig.add_trace(go.Scatter(
        x=[2024],
        y=[49],
        mode='markers',
        name='2024 Actual',
        marker=dict(size=12, color='#EF4444', symbol='diamond'),
        hovertemplate='<b>2024 Actual</b><br>Account Ownership: 49%<extra></extra>'
    ))
    
    # Base forecast with confidence interval
    forecast_df_sorted = forecast_df.sort_values('Year')
    years = forecast_df_sorted['Year'].values
    access = forecast_df_sorted['Account_Ownership_%'].values
    ci_lower = forecast_df_sorted['Ownership_CI_Lower'].values
    ci_upper = forecast_df_sorted['Ownership_CI_Upper'].values
    
    # Confidence interval as shaded area
    fig.add_trace(go.Scatter(
        x=years.tolist() + years[::-1].tolist(),
        y=ci_upper.tolist() + ci_lower[::-1].tolist(),
        fill='toself',
        fillcolor='rgba(59, 130, 246, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        showlegend=True,
        name='95% Confidence Interval',
        hoverinfo='skip'
    ))
    
    # Base forecast
    fig.add_trace(go.Scatter(
        x=years,
        y=access,
        mode='lines+markers',
        name='Base Forecast',
        line=dict(color='#3B82F6', width=3),
        marker=dict(size=10),
        hovertemplate='<b>Year %{x}</b><br>Account Ownership: %{y:.1f}%<extra></extra>'
    ))
    
    # Scenario lines
    scenario_data = scenarios['scenarios']
    colors = {'Pessimistic': '#EF4444', 'Optimistic': '#10B981'}
    for scenario_name, values in scenario_data.items():
        if scenario_name != 'Base':
            fig.add_trace(go.Scatter(
                x=years,
                y=values,
                mode='lines',
                name=f'{scenario_name} Scenario',
                line=dict(color=colors.get(scenario_name, '#9CA3AF'), 
                         dash='dash' if scenario_name == 'Pessimistic' else 'dot',
                         width=2),
                hovertemplate=f'<b>{scenario_name}</b><br>Year %{{x}}<br>Account Ownership: %{{y:.1f}}%<extra></extra>'
            ))
    
    fig.update_layout(
        title='<b>Account Ownership (Access) Forecast 2025-2027</b>',
        xaxis_title='Year',
        yaxis_title='Account Ownership (%)',
        hovermode='x unified',
        height=500,
        template='plotly_white',
        font=dict(family='Arial', size=12),
        yaxis=dict(range=[45, 65])
    )
    
    return fig

def create_usage_forecast_chart(forecast_df, scenarios):
    """Create interactive usage forecast chart."""
    fig = go.Figure()
    
    # Historical reference
    fig.add_trace(go.Scatter(
        x=[2024],
        y=[35],
        mode='markers',
        name='2024 Estimated',
        marker=dict(size=12, color='#F59E0B', symbol='diamond'),
        hovertemplate='<b>2024 Estimated</b><br>Digital Payment Usage: 35%<extra></extra>'
    ))
    
    forecast_df_sorted = forecast_df.sort_values('Year')
    years = forecast_df_sorted['Year'].values
    usage = forecast_df_sorted['Digital_Payment_%'].values
    ci_lower = forecast_df_sorted['Payment_CI_Lower'].values
    ci_upper = forecast_df_sorted['Payment_CI_Upper'].values
    
    # Confidence interval
    fig.add_trace(go.Scatter(
        x=years.tolist() + years[::-1].tolist(),
        y=ci_upper.tolist() + ci_lower[::-1].tolist(),
        fill='toself',
        fillcolor='rgba(16, 185, 129, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        showlegend=True,
        name='95% Confidence Interval',
        hoverinfo='skip'
    ))
    
    # Base forecast
    fig.add_trace(go.Scatter(
        x=years,
        y=usage,
        mode='lines+markers',
        name='Base Forecast',
        line=dict(color='#10B981', width=3),
        marker=dict(size=10),
        hovertemplate='<b>Year %{x}</b><br>Digital Payment Usage: %{y:.1f}%<extra></extra>'
    ))
    
    # Scenarios
    scenario_data = scenarios['scenarios']
    colors = {'Pessimistic': '#EF4444', 'Optimistic': '#F59E0B'}
    for scenario_name, values in scenario_data.items():
        if scenario_name != 'Base':
            fig.add_trace(go.Scatter(
                x=years,
                y=[v * 0.93 if scenario_name == 'Pessimistic' else v * 1.11 
                   for v in values],  # Scenario-specific adjustments
                mode='lines',
                name=f'{scenario_name} Scenario',
                line=dict(color=colors.get(scenario_name, '#9CA3AF'),
                         dash='dash' if scenario_name == 'Pessimistic' else 'dot',
                         width=2),
                hovertemplate=f'<b>{scenario_name}</b><br>Year %{{x}}<br>Digital Payment Usage: %{{y:.1f}}%<extra></extra>'
            ))
    
    fig.update_layout(
        title='<b>Digital Payment Usage Forecast 2025-2027</b>',
        xaxis_title='Year',
        yaxis_title='Digital Payment Usage (%)',
        hovermode='x unified',
        height=500,
        template='plotly_white',
        font=dict(family='Arial', size=12),
        yaxis=dict(range=[30, 55])
    )
    
    return fig

def create_comparison_chart(forecast_df):
    """Create side-by-side comparison of access vs usage."""
    forecast_df_sorted = forecast_df.sort_values('Year')
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Account Ownership', 'Digital Payment Usage'),
        specs=[[{"type": "bar"}, {"type": "bar"}]]
    )
    
    years = forecast_df_sorted['Year'].values
    access = forecast_df_sorted['Account_Ownership_%'].values
    usage = forecast_df_sorted['Digital_Payment_%'].values
    
    fig.add_trace(
        go.Bar(x=years, y=access, name='Account Ownership',
               marker=dict(color='#3B82F6'), text=access, textposition='auto'),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(x=years, y=usage, name='Digital Payment',
               marker=dict(color='#10B981'), text=usage, textposition='auto'),
        row=1, col=2
    )
    
    fig.update_yaxes(range=[0, 100], row=1, col=1)
    fig.update_yaxes(range=[0, 100], row=1, col=2)
    fig.update_layout(height=400, showlegend=False, template='plotly_white')
    
    return fig

def create_scenario_comparison(forecast_df, scenarios):
    """Create scenario comparison chart."""
    scenario_data = scenarios['scenarios']
    years = scenarios['years']
    
    fig = go.Figure()
    
    colors = {'Pessimistic': '#EF4444', 'Base': '#3B82F6', 'Optimistic': '#10B981'}
    
    for scenario_name, values in scenario_data.items():
        fig.add_trace(go.Bar(
            x=years,
            y=values,
            name=scenario_name,
            marker=dict(color=colors.get(scenario_name, '#9CA3AF')),
            text=values,
            textposition='auto'
        ))
    
    fig.update_layout(
        title='<b>Scenario Comparison: Account Ownership 2025-2027</b>',
        xaxis_title='Year',
        yaxis_title='Account Ownership (%)',
        barmode='group',
        height=450,
        template='plotly_white',
        hovermode='x unified'
    )
    
    return fig

def create_impact_matrix_heatmap(matrix_df):
    """Create heatmap of event-indicator impacts."""
    # Convert text values to numeric for visualization
    numeric_matrix = matrix_df.copy()
    
    for col in numeric_matrix.columns:
        numeric_matrix[col] = numeric_matrix[col].apply(
            lambda x: float(x.rstrip('%')) if isinstance(x, str) and x != '-' else np.nan
        )
    
    fig = go.Figure(data=go.Heatmap(
        z=numeric_matrix.values,
        x=numeric_matrix.columns,
        y=numeric_matrix.index,
        colorscale='RdYlGn',
        text=matrix_df.values,
        texttemplate='%{text}',
        textfont={"size": 10},
        hovertemplate='<b>%{y}</b><br>%{x}<br>Impact: %{text}<extra></extra>'
    ))
    
    fig.update_layout(
        title='<b>Event-Indicator Impact Association Matrix</b>',
        xaxis_title='Indicators',
        yaxis_title='Events',
        height=400,
        font=dict(size=11)
    )
    
    return fig

def create_historical_trend():
    """Create historical account ownership trend."""
    historical = pd.DataFrame({
        'Year': [2011, 2014, 2017, 2021, 2024],
        'Account_Ownership': [14, 22, 35, 46, 49]
    })
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=historical['Year'],
        y=historical['Account_Ownership'],
        mode='lines+markers',
        name='Historical Data',
        line=dict(color='#8B5CF6', width=3),
        marker=dict(size=10),
        hovertemplate='<b>Year %{x}</b><br>Account Ownership: %{y}%<extra></extra>'
    ))
    
    # Add growth rate annotations
    fig.add_annotation(text='13pp growth',
                      x=2015.5, y=28.5, showarrow=True, arrowsize=1.5)
    fig.add_annotation(text='11pp growth',
                      x=2019, y=40.5, showarrow=True, arrowsize=1.5)
    fig.add_annotation(text='3pp growth<br>(Stagnation?)',
                      x=2022.5, y=47.5, showarrow=True, arrowsize=1.5)
    
    fig.update_layout(
        title='<b>Historical Account Ownership Trend (2011-2024)</b>',
        xaxis_title='Year',
        yaxis_title='Account Ownership (%)',
        height=400,
        template='plotly_white',
        hovermode='x unified'
    )
    
    return fig

# =============================================================================
# MAIN DASHBOARD
# =============================================================================

def main():
    """Main dashboard application."""
    
    # Load data
    forecast_df = load_forecast_data()
    scenarios = load_scenarios()
    association_matrix = load_association_matrix()
    
    # Header
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); 
                padding: 40px 20px; border-radius: 12px; margin-bottom: 30px;'>
        <h1 style='color: white; margin: 0;'>📊 Ethiopia Financial Inclusion Forecasting</h1>
        <p style='color: rgba(255, 255, 255, 0.9); font-size: 1.1rem; margin-top: 10px;'>
            Interactive Dashboard for Understanding Trends, Events & Forecasts (2025-2027)
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.radio(
        "Select Page:",
        ["📈 Overview", "📊 Trends & Analysis", "🎯 Forecasts", "🔄 Scenarios", 
         "📍 Event Impact", "💡 Key Insights", "📚 Methodology"],
        index=0
    )
    
    # PAGE: OVERVIEW
    if page == "📈 Overview":
        show_overview_page(forecast_df, scenarios)
    
    # PAGE: TRENDS & ANALYSIS
    elif page == "📊 Trends & Analysis":
        show_trends_page(forecast_df)
    
    # PAGE: FORECASTS
    elif page == "🎯 Forecasts":
        show_forecasts_page(forecast_df)
    
    # PAGE: SCENARIOS
    elif page == "🔄 Scenarios":
        show_scenarios_page(forecast_df, scenarios)
    
    # PAGE: EVENT IMPACT
    elif page == "📍 Event Impact":
        show_event_impact_page(association_matrix)
    
    # PAGE: KEY INSIGHTS
    elif page == "💡 Key Insights":
        show_insights_page()
    
    # PAGE: METHODOLOGY
    elif page == "📚 Methodology":
        show_methodology_page()

def show_overview_page(forecast_df, scenarios):
    """Display overview page."""
    st.header("Overview: Ethiopia's Financial Inclusion Journey")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Current Access (2024)",
            "49%",
            "+3pp from 2021",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            "2027 Forecast (Base)",
            "57%",
            "+8pp from 2024",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            "Digital Payment (2024)",
            "~35%",
            "9.45% mobile money"
        )
    
    with col4:
        st.metric(
            "2027 Payment Usage",
            "46%",
            "+11pp from 2024",
            delta_color="normal"
        )
    
    st.markdown("---")
    
    # Main forecasts
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_access_forecast_chart(forecast_df, scenarios), 
                       use_container_width=True)
    
    with col2:
        st.plotly_chart(create_usage_forecast_chart(forecast_df, scenarios), 
                       use_container_width=True)
    
    st.markdown("---")
    
    # Key metrics
    st.subheader("📋 Key Metrics Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Access (Account Ownership)**
        - 2024 Actual: 49%
        - 2025 Forecast: 52% [50-54%]
        - 2026 Forecast: 54% [52-56%]
        - 2027 Forecast: 57% [54-60%]
        - Growth Rate: ~2pp annually
        """)
    
    with col2:
        st.markdown("""
        **Usage (Digital Payments)**
        - 2024 Estimated: 35%
        - 2025 Forecast: 40% [37-43%]
        - 2026 Forecast: 43% [40-46%]
        - 2027 Forecast: 46% [42-50%]
        - Growth Rate: ~3-4pp annually
        """)

def show_trends_page(forecast_df):
    """Display trends and analysis page."""
    st.header("📊 Historical Trends & Analysis")
    
    st.subheader("Historical Account Ownership Trajectory")
    st.plotly_chart(create_historical_trend(), use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("Access vs Usage Comparison")
    st.plotly_chart(create_comparison_chart(forecast_df), use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📌 Key Observations
        
        **The Stagnation Paradox:**
        - Account ownership grew only +3pp (2021-2024)
        - Yet mobile money accounts more than doubled (4.7% → 9.45%)
        - Suggests: New digital services substituting for existing accounts, not driving net new inclusion
        
        **Growth Deceleration:**
        - 2011-2014: +8pp annual growth
        - 2014-2017: +13pp total growth
        - 2017-2021: +11pp total growth
        - 2021-2024: Only +3pp (slowest period)
        """)
    
    with col2:
        st.markdown("""
        ### 👥 Gender Gap Analysis
        
        **Persistent Disparity:**
        - Male ownership: 56% (2021)
        - Female ownership: 36% (2021)
        - Gap: 20 percentage points
        - Status: **Unchanged** through 2024
        
        **Structural Barriers:**
        - Limited phone ownership
        - Limited government ID access
        - Cultural and social norms
        - Require targeted interventions
        """)
    
    st.markdown("---")
    
    st.subheader("📊 Registered vs Active Gap")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Mobile Money Accounts", "9.45%", "Registered users")
    with col2:
        st.metric("Digital Payment Users", "~35%", "Broader definition")
    with col3:
        st.metric("Usage Gap", "25.5pp", "Accounts inactive")
    
    st.info("""
    💡 **Insight**: High registration but low engagement. Many account holders 
    are not actively using digital payment services. Key opportunity: 
    Activate existing account base through:
    - Merchant ecosystem development
    - User education and incentives
    - Integration with daily payment flows
    """)

def show_forecasts_page(forecast_df):
    """Display forecasts page."""
    st.header("🎯 Financial Inclusion Forecasts 2025-2027")
    
    st.markdown("""
    These forecasts are based on:
    - Historical trend analysis (linear regression on 5 Findex observations)
    - Event impact augmentation (Telebirr, M-Pesa, Fayda Digital ID, etc.)
    - 95% confidence intervals reflecting data sparsity
    """)
    
    st.markdown("---")
    
    st.subheader("📈 Access Forecast (Account Ownership)")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.plotly_chart(create_access_forecast_chart(
            forecast_df, load_scenarios()), use_container_width=True)
    
    with col2:
        st.markdown("""
        **Forecast Method:**
        - Linear trend regression
        - Event impacts (+10pp Fayda ID at 24mo lag)
        - Confidence: 95%
        
        **Key Drivers:**
        1. Fayda Digital ID
        2. Ecosystem maturation
        3. Infrastructure build-out
        4. Infrastructure expansion
        """)
    
    st.markdown("---")
    
    st.subheader("💳 Usage Forecast (Digital Payments)")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.plotly_chart(create_usage_forecast_chart(
            forecast_df, load_scenarios()), use_container_width=True)
    
    with col2:
        st.markdown("""
        **Forecast Method:**
        - Trend + ecosystem maturation
        - Activation of existing accounts
        - Confidence: 95%
        
        **Key Drivers:**
        1. Telebirr + M-Pesa ecosystem
        2. 4G infrastructure (70%+)
        3. Smartphone adoption
        4. Merchant growth
        """)
    
    st.markdown("---")
    
    st.subheader("📊 Forecast Table")
    
    # Create display table
    display_df = forecast_df[['Year', 'Account_Ownership_%', 'Ownership_CI_Lower', 
                               'Ownership_CI_Upper', 'Digital_Payment_%', 
                               'Payment_CI_Lower', 'Payment_CI_Upper']].copy()
    display_df.columns = ['Year', 'Access %', 'Access Lower', 'Access Upper', 
                          'Usage %', 'Usage Lower', 'Usage Upper']
    
    st.dataframe(display_df, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("⚠️ Forecast Uncertainties")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.warning("""
        **Data Sparsity**
        - Only 5 account ownership observations (2011-2024)
        - Confidence intervals: ±2-3pp
        - Recommend annual revalidation
        """)
    
    with col2:
        st.warning("""
        **Model Assumptions**
        - Linear trend continuation
        - Impact lags from comparable countries
        - No macroeconomic shocks
        """)
    
    with col3:
        st.warning("""
        **External Risks**
        - FX volatility (affects affordability)
        - Policy changes
        - Competitive dynamics
        - Behavioral adoption speed
        """)

def show_scenarios_page(forecast_df, scenarios):
    """Display scenarios page."""
    st.header("🔄 Scenario Analysis: Multiple Futures")
    
    st.markdown("""
    To account for uncertainty, we model three scenarios reflecting different 
    assumptions about adoption rates, ecosystem development, and event impacts.
    """)
    
    st.markdown("---")
    
    st.plotly_chart(create_scenario_comparison(forecast_df, scenarios), 
                   use_container_width=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🔴 Pessimistic Scenario
        
        **2027 Outcome:** 54% Access / 43% Usage
        
        **Assumptions:**
        - Slower Fayda rollout (30mo lag instead of 24mo)
        - Limited merchant ecosystem growth
        - Persistent affordability constraints
        - Competitive headwinds
        - Macroeconomic challenges
        
        **Probability:** ~20-25%
        """)
    
    with col2:
        st.markdown("""
        ### 🔵 Base Scenario
        
        **2027 Outcome:** 57% Access / 46% Usage
        
        **Assumptions:**
        - Fayda rollout per schedule
        - Moderate merchant growth
        - Stable macroeconomic environment
        - Continued infrastructure investment
        - Normal policy evolution
        
        **Probability:** ~50-60%
        """)
    
    with col3:
        st.markdown("""
        ### 🟢 Optimistic Scenario
        
        **2027 Outcome:** 62% Access / 51% Usage
        
        **Assumptions:**
        - Accelerated Fayda adoption (18mo lag)
        - Strong merchant ecosystem growth
        - Infrastructure ahead of schedule
        - Supportive policies
        - Rapid behavioral adoption
        
        **Probability:** ~15-25%
        """)
    
    st.markdown("---")
    
    st.subheader("📊 Progress Toward 2030 Goals")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 NFIS-II Target: 60% Account Ownership
        
        **Status by Scenario:**
        - Pessimistic: 54% (6pp short of target)
        - Base: 57% (3pp short of target)
        - Optimistic: 62% (2pp above target)
        
        **Gap Analysis:**
        - Base scenario implies continued annual growth of ~2pp post-2027
        - Would reach 60% by 2030 under baseline conditions
        - Acceleration needed for faster convergence
        """)
    
    with col2:
        st.markdown("""
        ### 💡 Acceleration Levers
        
        To achieve 65%+ by 2030, focus on:
        
        1. **Fayda Digital ID**
           - Accelerate enrollment (current: 15M → target: 30M by 2027)
           - Reduce activation friction
        
        2. **Ecosystem Development**
           - Expand merchant network (both physical and digital)
           - Increase use cases beyond P2P
        
        3. **Targeted Inclusion**
           - Close gender gap (5pp reduction needed)
           - Rural/urban equity programs
        """)

def show_event_impact_page(association_matrix):
    """Display event impact page."""
    st.header("📍 Event Impact Analysis")
    
    st.markdown("""
    This section shows how major events (policy launches, product entries, 
    infrastructure investments) affect key financial inclusion indicators.
    """)
    
    st.markdown("---")
    
    st.subheader("Event-Indicator Association Matrix")
    st.plotly_chart(create_impact_matrix_heatmap(association_matrix), 
                   use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("📋 Event Details & Impact Estimates")
    
    events = {
        'Telebirr Launch (May 2021)': {
            'category': 'Product Launch',
            'impacts': {
                'Account Ownership': '+15pp (12mo lag, medium confidence)',
                'Mobile Money Accounts': '+25pp (6mo lag, high confidence)',
                'P2P Transactions': '+25% (6mo lag)'
            },
            'status': '✅ Validated',
            'notes': 'Mobile money accounts grew from 4.7% to 9.45%, aligning with model estimates'
        },
        'Safaricom Market Entry (Aug 2022)': {
            'category': 'Market Entry / Competition',
            'impacts': {
                '4G Coverage': '+15pp (12mo lag, medium confidence)',
                'Data Affordability': '-20% costs (12mo lag, Rwanda benchmark)'
            },
            'status': '✅ Observed',
            'notes': '4G coverage expanded from 37.5% to 70.8% by 2025'
        },
        'M-Pesa Launch (Aug 2023)': {
            'category': 'Product Launch',
            'impacts': {
                'Mobile Money Accounts': '+5pp (6mo lag, incremental)',
                'Digital Payment Usage': '+8% (9mo lag)'
            },
            'status': '⚠️ Incomplete',
            'notes': 'Need 12+ months post-launch data. Likely substitution effect (users switching platforms)'
        },
        'Fayda Digital ID Expansion (Jan 2024)': {
            'category': 'Infrastructure / Policy',
            'impacts': {
                'Account Ownership': '+10pp (24mo lag, medium confidence)',
                'Gender Gap': '-5pp (24mo lag, India Aadhaar benchmark)'
            },
            'status': '📊 Pending',
            'notes': 'Enrollment at 15M+. Expected impact through 2026'
        },
        'FX Reform (Jul 2024)': {
            'category': 'Economic Policy',
            'impacts': {
                'Data Affordability': '+30% effective costs (3mo lag)',
                'Digital Payment Usage': 'Negative (indirect via affordability)'
            },
            'status': '⚠️ Headwind',
            'notes': 'Currency depreciation increases costs. Mitigated by operator cost optimization'
        }
    }
    
    for event_name, details in events.items():
        with st.expander(f"**{event_name}**"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Category:** {details['category']}")
                st.markdown(f"**Status:** {details['status']}")
            
            with col2:
                st.markdown(f"**Notes:** {details['notes']}")
            
            st.markdown("**Impact Estimates:**")
            for indicator, impact in details['impacts'].items():
                st.markdown(f"- {indicator}: {impact}")
    
    st.markdown("---")
    
    st.subheader("🔬 Methodology Notes")
    
    st.markdown("""
    **Data Sources for Impact Estimates:**
    - Telebirr: Observed change in mobile money account rates
    - Safaricom: Network expansion reports + 4G coverage data
    - M-Pesa: Kenya M-Pesa impact study (Suri & Jack 2016)
    - Fayda: India Aadhaar digital ID impact study (World Bank)
    - FX Reform: IMF analysis of currency effects on digital finance
    
    **Lag Periods:**
    - Product launches: 3-6 months for initial adoption, 12+ for full effect
    - Infrastructure: 6-12 months for behavioral adaptation
    - Policy interventions: 12-24 months for institutional adjustment
    
    **Confidence Ratings:**
    - High: Based on Ethiopian data or strong comparable cases
    - Medium: Based on reasonable comparable country analogy
    - Low: Estimated with significant uncertainty
    """)

def show_insights_page():
    """Display key insights page."""
    st.header("💡 Key Insights from Analysis")
    
    insights = [
        {
            'title': '1. The Stagnation Paradox',
            'subtitle': 'Account ownership grew only +3pp (2021-2024) despite 100% mobile money expansion',
            'description': '''
            Despite Telebirr (launched May 2021) growing to 54M users and M-Pesa entering (Aug 2023) 
            with 10M+ users, aggregate account ownership increased by only 3 percentage points (46% → 49%).
            
            **Interpretation:** New digital services are substituting for existing bank accounts rather than 
            driving net new inclusion. Users are switching platforms rather than moving from no account to an account.
            '''
        },
        {
            'title': '2. Persistent Gender Gap',
            'subtitle': '20pp gap (56% male vs 36% female) unchanged 2021-2024',
            'description': '''
            Despite massive infrastructure investments, the gender gap has not narrowed. 
            Women remain significantly underrepresented across all financial services.
            
            **Drivers:** Lack of government ID, limited phone ownership, social/cultural norms, 
            and insufficient targeted outreach.
            
            **Opportunity:** Fayda Digital ID expected to disproportionately benefit women 
            (who lack traditional identity documents).
            '''
        },
        {
            'title': '3. Registered vs Active Gap',
            'subtitle': '9.45% have mobile money accounts but only 35% make digital payments',
            'description': '''
            A large gap exists between account registration and active usage. Many accounts lie dormant, 
            suggesting adoption without sustained engagement.
            
            **Root Causes:** Limited merchant acceptance, weak use cases, affordability concerns, 
            and customer inertia.
            
            **Opportunity:** Activating the existing ~9.45% of mobile money account holders could 
            push digital payment usage from 35% to 40%+ without new account acquisition.
            '''
        },
        {
            'title': '4. P2P Dominance (Ethiopia-Specific)',
            'subtitle': 'Digital payments in Ethiopia are P2P-driven for goods/services, not global norms',
            'description': '''
            Unlike global patterns where mobile money is primarily for transfers, in Ethiopia, 
            digital payments are heavily used for actual goods and services transactions.
            
            **Implication:** Traditional "digital payment" metrics may undercount actual usage. 
            Ethiopia's framework is more mature than aggregate figures suggest.
            '''
        },
        {
            'title': '5. Infrastructure Investment Scaling',
            'subtitle': '4G doubled (37.5% → 70.8%), smartphone at 28.5%, Fayda at 15M+',
            'description': '''
            Rapid infrastructure expansion creating enabling conditions for digital inclusion:
            - 4G coverage doubled to 70.8% by 2025
            - Smartphone penetration growing (~28.5%)
            - Fayda Digital ID enrollment at 15M+ (20% of adult population)
            
            **But:** Asset availability has not yet translated to usage adoption. 
            Additional complementary factors (merchant networks, user education) remain critical.
            '''
        },
        {
            'title': '6. Event-Outcome Misalignment',
            'subtitle': 'Despite product launches (Telebirr, Safaricom, M-Pesa), account ownership stagnated',
            'description': '''
            Three major events occurred in 2021-2023:
            1. Telebirr launch (May 2021)
            2. Safaricom entry (Aug 2022)
            3. M-Pesa launch (Aug 2023)
            
            Yet account ownership grew by just 3pp total. This suggests:
            - Significant substitution effects (users switching between providers)
            - Competitive dynamics reducing net new inclusion
            - Events working in different segments without aggregation effect
            '''
        },
        {
            'title': '7. Data Quality Limitations',
            'subtitle': 'Only 5 account ownership observations over 13 years',
            'description': '''
            The sparsity of Findex data (2011, 2014, 2017, 2021, 2024) limits granular trend analysis.
            
            **Impact on Forecasting:**
            - Wider confidence intervals (±2-3pp for 2027)
            - Difficulty identifying inflection points
            - Reliance on comparable country evidence for event impacts
            
            **Recommendation:** Collect more frequent baseline surveys or use alternative proxy indicators 
            (operator-reported accounts, agent transactions, etc.)
            '''
        },
        {
            'title': '8. Critical Data Gaps',
            'subtitle': 'Missing agent density, merchant acceptance, regional variation, credit penetration',
            'description': '''
            Several important dimensions are not captured in available data:
            - **Agent Network Density:** Critical for rural inclusion
            - **Merchant Acceptance:** Key driver of payment usage
            - **Regional Disparities:** Urban/rural variation likely ±10pp
            - **Credit Penetration:** Very low (formal credit is rare)
            - **Gender-Disaggregated Usage:** Limited post-2021 data
            
            **Mitigation:** Task 5 dashboard recommendations + operator data partnerships.
            '''
        }
    ]
    
    for insight in insights:
        st.markdown(f"### {insight['title']}")
        st.markdown(f"**{insight['subtitle']}**")
        st.markdown(insight['description'])
        st.markdown("---")

def show_methodology_page():
    """Display methodology page."""
    st.header("📚 Methodology & Technical Notes")
    
    st.markdown("""
    This dashboard synthesizes analysis from four integrated tasks:
    Task 1 (Data Exploration), Task 2 (EDA), Task 3 (Impact Modeling), and Task 4 (Forecasting).
    """)
    
    st.markdown("---")
    
    st.subheader("📊 Data Sources")
    
    st.markdown("""
    **Primary Data:**
    - Global Findex Database (World Bank): Account ownership surveys 2011-2024
    - Operator Reports: Telebirr, EthSwitch, Safaricom, Ethio Telecom
    - Government Data: Fayda Digital ID enrollment, National Bank of Ethiopia
    
    **Data Quality:**
    - Findex: High confidence, demand-side surveys
    - Operator reports: Medium confidence, supply-side data
    - Regulatory data: High confidence, official records
    """)
    
    st.markdown("---")
    
    st.subheader("🔬 Forecasting Methodology")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Baseline Model:**
        - Linear regression on historical data
        - Equation: y = a + b*year
        - Applied to: Account ownership (2011-2024)
        """)
    
    with col2:
        st.markdown("""
        **Event Augmentation:**
        - Add impact of known events with estimated lags
        - Formula: y_forecast = baseline + Σ(event_impact * lag_adjustment)
        - Impacts from comparable country studies
        """)
    
    st.markdown("""
    **Uncertainty Quantification:**
    - 95% confidence intervals from residual standard error
    - Reflects both model uncertainty and data sparsity
    - Wider intervals for longer horizons
    
    **Scenario Analysis:**
    - Pessimistic: -3pp from baseline (slower adoption)
    - Base: Central estimate
    - Optimistic: +5pp from baseline (accelerated adoption)
    """)
    
    st.markdown("---")
    
    st.subheader("📍 Event Impact Estimation")
    
    st.markdown("""
    **For events with Ethiopian data:**
    - Extract pre/post differences
    - Example: Telebirr (May 2021) → mobile money accounts 4.7% → 9.45% (+4.75pp observed)
    - Model estimate: +25pp over time (accounts for delayed full adoption)
    
    **For events without Ethiopian data:**
    - Use comparable country evidence
    - Kenya M-Pesa impact: +15pp account ownership over 5 years (Suri & Jack 2016)
    - India Aadhaar: +15-20pp account opening (World Bank case study)
    - Rwanda digital ID: +8pp inclusion improvement
    
    **Confidence Adjustment:**
    - Kenya data (similar market stage): Use 1.0x multiplier
    - India data (more developed): Use 0.9x multiplier
    - Rwanda data (regional precedent): Use 0.95x multiplier
    """)
    
    st.markdown("---")
    
    st.subheader("⚠️ Key Assumptions & Limitations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Modeling Assumptions:**
        1. Linear trend continuation (no inflection points)
        2. Event impacts as specified (no unexpected delays)
        3. No major macroeconomic shocks (stable environment)
        4. Behavioral adoption follows estimated lags
        5. Comparable country impacts transfer to Ethiopia
        """)
    
    with col2:
        st.markdown("""
        **Limitations:**
        - Sparse historical data (5 points over 13 years)
        - Aggregate statistics mask regional variation
        - Gender and demographic disaggregation limited
        - Model cannot predict unexpected events
        - External shocks (crises, etc.) not modeled
        """)
    
    st.markdown("---")
    
    st.subheader("🔄 Validation Strategy")
    
    st.markdown("""
    **2025 Interim Validation (February 2026):**
    - Compare 2024 Findex (when released Q1 2026) against 2024 forecast
    - Monitor Fayda enrollment trajectory
    - Track operator-reported growth rates
    
    **Adjustment Triggers:**
    - If 2025 actual > forecast + 3pp: Revise upward for 2026-2027
    - If 2025 actual < forecast - 3pp: Revise downward
    - If major policy changes occur: Reestimate event impacts
    
    **Quarterly Monitoring:**
    - Fayda Digital ID enrollment rates
    - Operator-reported account and transaction growth
    - 4G coverage and smartphone penetration
    - Agent network density (if available)
    """)

# =============================================================================
# RUN DASHBOARD
# =============================================================================

if __name__ == "__main__":
    main()