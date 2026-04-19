"""
I-REC Market Dashboard - March 2026
A comprehensive dashboard for understanding the I-REC market
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="I-REC Market Dashboard - March 2026",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a more colorful, modern look
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #43cea2 0%, #185a9d 100%);
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .metric-value {
        font-size: 36px;
        font-weight: bold;
        color: #fff;
        text-shadow: 1px 1px 2px #185a9d44;
    }
    .metric-label {
        font-size: 15px;
        color: #e0e0e0;
    }
    .section-header {
        background: linear-gradient(90deg, #43cea2 0%, #185a9d 100%);
        color: white;
        padding: 10px;
        border-radius: 7px;
        margin-bottom: 20px;
        font-size: 20px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


def load_data():
    """Load only March 2026 data from large sheets for speed.
    
    The data source can be configured via environment variable:
    - IREC_DATA_URL: URL to download the Excel file from (e.g., GitHub raw URL)
    - IREC_DATA_FILE: Local file path (default: I-REC-Registry-Data-March-2026.xlsx)
    """
    import os
    
    # Check for environment variable first (for GitHub/online deployment)
    file_url = os.environ.get('IREC_DATA_URL', '')
    file_path = os.environ.get('IREC_DATA_FILE', 'I-REC-Registry-Data-March-2026.xlsx')
    
    # If URL is provided, download the file
    if file_url:
        import urllib.request
        import io
        st.info(f"📥 Downloading data from: {file_url}")
        response = urllib.request.urlopen(file_url)
        xl = pd.ExcelFile(io.BytesIO(response.read()))
    else:
        # Use local file
        xl = pd.ExcelFile(file_path)

    # Only load March 2026 rows for large sheets
    issuances = pd.read_excel(xl, sheet_name="Issuances", parse_dates=['Issue Date', 'Commissioning Date'])
    issuances = issuances[issuances['Issue Date'].dt.month == 3]
    redemptions = pd.read_excel(xl, sheet_name="Redemptions", parse_dates=['Redemption Date'])
    redemptions = redemptions[redemptions['Redemption Date'].dt.month == 3]

    # Load all for smaller sheets
    organisations = pd.read_excel(xl, sheet_name="Organisations", parse_dates=['Registration Date'])
    facilities = pd.read_excel(xl, sheet_name="Facilities", parse_dates=['Registration Date', 'Commissioning Date'])

    return issuances, organisations, facilities, redemptions


# Load data with spinner
with st.spinner('Loading I-REC data...'):
    issuances, organisations, facilities, redemptions = load_data()
    # Data is already filtered for March 2026
    march_issuances = issuances
    march_redemptions = redemptions

# Sidebar
st.sidebar.title("📊 I-REC Dashboard")
st.sidebar.markdown("### March 2026 Data")
st.sidebar.info(f"Data reflects: January 2014 to March 2026")

# Main title
st.title("⚡ I-REC Market Dashboard")
st.markdown("### March 2026 - Understanding the I-REC Market")

# ============================================
# KEY METRICS SECTION
# ============================================
st.markdown("## 📈 Key Market Metrics")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{march_issuances["Volume Issued"].sum():,.0f}</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">I-RECs Issued (March)</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{march_redemptions["Volume Redeemed"].sum():,.0f}</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">I-RECs Redeemed (March)</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{len(march_issuances):,}</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Issuance Transactions</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{len(facilities[facilities["Active Status"] == True]):,}</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Active Facilities</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col5:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{len(organisations):,}</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Total Organisations</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# ============================================
# DAY-WISE ANALYSIS
# ============================================
st.markdown("## 📅 Day-wise Analysis (March 2026)")

# Daily issuance trend
daily_issuance = march_issuances.groupby(march_issuances['Issue Date'].dt.date)['Volume Issued'].sum().reset_index()
daily_issuance.columns = ['Date', 'Volume Issued']

fig = px.line(
    daily_issuance,
    x='Date',
    y='Volume Issued',
    title='Daily I-REC Issuance Volume',
    markers=True,
    line_shape='spline'
)
fig.update_layout(height=350, xaxis_title="Date", yaxis_title="Volume Issued")
st.plotly_chart(fig, use_container_width=True)

# Daily redemption trend
daily_redemption = march_redemptions.groupby(march_redemptions['Redemption Date'].dt.date)['Volume Redeemed'].sum().reset_index()
daily_redemption.columns = ['Date', 'Volume Redeemed']

fig = px.line(
    daily_redemption,
    x='Date',
    y='Volume Redeemed',
    title='Daily I-REC Redemption Volume',
    markers=True,
    line_shape='spline',
    color_discrete_sequence=['green']
)
fig.update_layout(height=350, xaxis_title="Date", yaxis_title="Volume Redeemed")
st.plotly_chart(fig, use_container_width=True)

# Combined issuance vs redemption
combined = pd.merge(daily_issuance, daily_redemption, on='Date', how='outer').fillna(0)
combined = combined.sort_values('Date')

fig = go.Figure()
fig.add_trace(go.Scatter(x=combined['Date'], y=combined['Volume Issued'], name='Issued', line=dict(color='blue', width=2), fill='tozeroy', fillcolor='rgba(0,0,255,0.2)'))
fig.add_trace(go.Scatter(x=combined['Date'], y=combined['Volume Redeemed'], name='Redeemed', line=dict(color='green', width=2), fill='tozeroy', fillcolor='rgba(0,128,0,0.2)'))
fig.update_layout(title='Daily Issuance vs Redemption Comparison', height=400, xaxis_title="Date", yaxis_title="Volume", hovermode='x unified')
st.plotly_chart(fig, use_container_width=True)

# Daily transaction count
daily_issuance_count = march_issuances.groupby(march_issuances['Issue Date'].dt.date).size().reset_index(name='Issuance Transactions')
daily_redemption_count = march_redemptions.groupby(march_redemptions['Redemption Date'].dt.date).size().reset_index(name='Redemption Transactions')

fig = make_subplots(rows=1, cols=2, subplot_titles=('Daily Issuance Transactions', 'Daily Redemption Transactions'))

fig.add_trace(go.Bar(x=daily_issuance_count.iloc[:,0], y=daily_issuance_count.iloc[:,1], name='Issuances', marker_color='blue'), row=1, col=1)
fig.add_trace(go.Bar(x=daily_redemption_count.iloc[:,0], y=daily_redemption_count.iloc[:,1], name='Redemptions', marker_color='green'), row=1, col=2)

fig.update_layout(height=350, showlegend=False)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================
# ISSUANCE ANALYSIS
# ============================================
st.markdown("## 🔋 Issuance Analysis")

col1, col2 = st.columns(2)

with col1:
    # Top countries by issuance
    country_issuance = march_issuances.groupby('Country Name')['Volume Issued'].sum().sort_values(ascending=False).head(10)
    fig = px.bar(
        x=country_issuance.values,
        y=country_issuance.index,
        orientation='h',
        title='Top 10 Countries by Issuance Volume',
        labels={'x': 'Volume Issued', 'y': 'Country'},
        color=country_issuance.values,
        color_continuous_scale='Blues'
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Technology breakdown
    tech_issuance = march_issuances.groupby('Technology')['Volume Issued'].sum().sort_values(ascending=False)
    fig = px.pie(
        values=tech_issuance.values,
        names=tech_issuance.index,
        title='Issuance by Technology Type',
        hole=0.4
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# Region analysis
col1, col2 = st.columns(2)

with col1:
    region_issuance = march_issuances.groupby('Region')['Volume Issued'].sum().sort_values(ascending=False)
    fig = px.bar(
        x=region_issuance.index,
        y=region_issuance.values,
        title='Issuance by Region',
        labels={'x': 'Region', 'y': 'Volume Issued'},
        color=region_issuance.values,
        color_continuous_scale='Viridis'
    )
    fig.update_layout(height=350, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Top Issuers
    issuer_issuance = march_issuances.groupby('Issuer')['Volume Issued'].sum().sort_values(ascending=False).head(10)
    fig = px.bar(
        x=issuer_issuance.values,
        y=issuer_issuance.index,
        orientation='h',
        title='Top 10 Issuers by Volume',
        labels={'x': 'Volume Issued', 'y': 'Issuer'},
        color=issuer_issuance.values,
        color_continuous_scale='Greens'
    )
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================
# REDEMPTION ANALYSIS
# ============================================
st.markdown("## ✅ Redemption Analysis")

col1, col2 = st.columns(2)

with col1:
    # Top beneficiary countries
    beneficiary = march_redemptions.groupby('Country Name - Beneficiary')['Volume Redeemed'].sum().sort_values(ascending=False).head(10)
    fig = px.bar(
        x=beneficiary.values,
        y=beneficiary.index,
        orientation='h',
        title='Top 10 Beneficiary Countries (Who redeemed)',
        labels={'x': 'Volume Redeemed', 'y': 'Country'},
        color=beneficiary.values,
        color_continuous_scale='Oranges'
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Redemption by technology
    tech_redemption = march_redemptions.groupby('Technology')['Volume Redeemed'].sum().sort_values(ascending=False)
    fig = px.pie(
        values=tech_redemption.values,
        names=tech_redemption.index,
        title='Redemption by Technology Type',
        hole=0.4
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# Issue vs Redemption comparison
col1, col2 = st.columns(2)

with col1:
    # Where redemptions came from (issue country)
    issue_origin = march_redemptions.groupby('Issue Country')['Volume Redeemed'].sum().sort_values(ascending=False).head(10)
    fig = px.bar(
        x=issue_origin.values,
        y=issue_origin.index,
        orientation='h',
        title='Top 10 Issue Countries (Where RECs came from)',
        labels={'x': 'Volume Redeemed', 'y': 'Country'},
        color=issue_origin.values,
        color_continuous_scale='Reds'
    )
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Redemption by region (beneficiary)
    region_redemption = march_redemptions.groupby('Region - Beneficiary')['Volume Redeemed'].sum().sort_values(ascending=False)
    fig = px.bar(
        x=region_redemption.index,
        y=region_redemption.values,
        title='Redemption by Beneficiary Region',
        labels={'x': 'Region', 'y': 'Volume Redeemed'},
        color=region_redemption.values,
        color_continuous_scale='Purples'
    )
    fig.update_layout(height=350, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================
# FACILITIES ANALYSIS
# ============================================
st.markdown("## 🏭 Facilities Analysis")

col1, col2, col3 = st.columns(3)

with col1:
    active_facilities = facilities[facilities['Active Status'] == True]
    st.metric("Active Facilities", len(active_facilities))

with col2:
    total_capacity = active_facilities['Capacity MW'].sum()
    st.metric("Total Active Capacity (MW)", f"{total_capacity:,.1f}")

with col3:
    avg_capacity = active_facilities['Capacity MW'].mean()
    st.metric("Average Facility Capacity (MW)", f"{avg_capacity:.2f}")

col1, col2 = st.columns(2)

with col1:
    # Facilities by country
    fac_country = active_facilities.groupby('Country Name').size().sort_values(ascending=False).head(10)
    fig = px.bar(
        x=fac_country.index,
        y=fac_country.values,
        title='Top 10 Countries by Number of Facilities',
        labels={'x': 'Country', 'y': 'Number of Facilities'},
        color=fac_country.values,
        color_continuous_scale='Teal'
    )
    fig.update_layout(height=350, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Facilities by technology
    fac_tech = active_facilities.groupby('Technology').size().sort_values(ascending=False)
    fig = px.bar(
        x=fac_tech.index,
        y=fac_tech.values,
        title='Facilities by Technology Type',
        labels={'x': 'Technology', 'y': 'Number of Facilities'},
        color=fac_tech.values,
        color_continuous_scale='Cividis'
    )
    fig.update_layout(height=350, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================
# ORGANISATIONS ANALYSIS
# ============================================
st.markdown("## 🏢 Organisations Analysis")

col1, col2 = st.columns(2)

with col1:
    # Organisations by role
    org_role = organisations.groupby('Role').size()
    fig = px.pie(
        values=org_role.values,
        names=org_role.index,
        title='Organisations by Role',
        hole=0.4
    )
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Organisations by region
    org_region = organisations.groupby('Region').size().sort_values(ascending=False)
    fig = px.bar(
        x=org_region.index,
        y=org_region.values,
        title='Organisations by Region',
        labels={'x': 'Region', 'y': 'Number of Organisations'},
        color=org_region.values,
        color_continuous_scale='Plasma'
    )
    fig.update_layout(height=350, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

# March registrations
march_orgs = organisations[organisations['Registration Date'].dt.month == 3]
st.metric("New Organisations in March 2026", len(march_orgs))

st.markdown("---")


# ============================================
# DAY-WISE ANALYSIS & INTERACTIVITY
# ============================================
st.markdown("<div class='section-header'>📅 Day-wise & Interactive Analysis (March 2026)</div>", unsafe_allow_html=True)

# --- INTERACTIVE FILTERS ---
with st.expander("🔎 Filter Data", expanded=True):
    min_date = march_issuances['Issue Date'].min()
    max_date = march_issuances['Issue Date'].max()
    date_range = st.slider("Select Date Range", min_value=min_date, max_value=max_date, value=(min_date, max_date), format="%Y-%m-%d")
    country_options = sorted(march_issuances['Country Name'].dropna().unique())
    country = st.multiselect("Country (Issuance)", country_options, default=country_options[:3])
    tech_options = sorted(march_issuances['Technology'].dropna().unique())
    tech = st.multiselect("Technology (Issuance)", tech_options, default=tech_options)

    # Filter
    filtered_issuances = march_issuances[
        (march_issuances['Issue Date'] >= date_range[0]) &
        (march_issuances['Issue Date'] <= date_range[1]) &
        (march_issuances['Country Name'].isin(country)) &
        (march_issuances['Technology'].isin(tech))
    ]
    filtered_redemptions = march_redemptions[
        (march_redemptions['Redemption Date'] >= date_range[0]) &
        (march_redemptions['Redemption Date'] <= date_range[1])
    ]

# --- DAY-WISE ISSUANCE ---
daily_issuance = filtered_issuances.groupby(filtered_issuances['Issue Date'].dt.date)['Volume Issued'].sum().reset_index()
daily_issuance.columns = ['Date', 'Volume Issued']

fig = px.line(
    daily_issuance,
    x='Date',
    y='Volume Issued',
    title='Daily I-REC Issuance Volume',
    line_shape='spline',
    color_discrete_sequence=['#43cea2']
)
fig.update_traces(mode='lines', line=dict(width=4))

fig.update_layout(height=350, xaxis_title="Date", yaxis_title="Volume Issued", plot_bgcolor='#181c24', paper_bgcolor='#181c24', font_color='#fff')

# --- DAY-WISE REDEMPTION ---
daily_redemption = filtered_redemptions.groupby(filtered_redemptions['Redemption Date'].dt.date)['Volume Redeemed'].sum().reset_index()
daily_redemption.columns = ['Date', 'Volume Redeemed']

fig = px.line(
    daily_redemption,
    x='Date',
    y='Volume Redeemed',
    title='Daily I-REC Redemption Volume',
    line_shape='spline',
    color_discrete_sequence=['#ff6e7f']
)
fig.update_traces(mode='lines', line=dict(width=4))

fig.update_layout(height=350, xaxis_title="Date", yaxis_title="Volume Redeemed", plot_bgcolor='#181c24', paper_bgcolor='#181c24', font_color='#fff')

# --- COMBINED ISSUANCE VS REDEMPTION ---
combined = pd.merge(daily_issuance, daily_redemption, on='Date', how='outer').fillna(0)
combined = combined.sort_values('Date')

fig = go.Figure()
fig.add_trace(go.Scatter(x=combined['Date'], y=combined['Volume Issued'], name='Issued', line=dict(color='#43cea2', width=4), fill='tozeroy', fillcolor='rgba(67,206,162,0.15)'))
fig.add_trace(go.Scatter(x=combined['Date'], y=combined['Volume Redeemed'], name='Redeemed', line=dict(color='#ff6e7f', width=4), fill='tozeroy', fillcolor='rgba(255,110,127,0.15)'))

fig.update_layout(title='Daily Issuance vs Redemption Comparison', height=400, xaxis_title="Date", yaxis_title="Volume", hovermode='x unified', plot_bgcolor='#181c24', paper_bgcolor='#181c24', font_color='#fff')

# --- DAILY TRANSACTION COUNTS ---
daily_issuance_count = filtered_issuances.groupby(filtered_issuances['Issue Date'].dt.date).size().reset_index(name='Issuance Transactions')
daily_redemption_count = filtered_redemptions.groupby(filtered_redemptions['Redemption Date'].dt.date).size().reset_index(name='Redemption Transactions')

fig = make_subplots(rows=1, cols=2, subplot_titles=('Daily Issuance Transactions', 'Daily Redemption Transactions'))
fig.add_trace(go.Bar(x=daily_issuance_count.iloc[:,0], y=daily_issuance_count.iloc[:,1], name='Issuances', marker_color='#43cea2'), row=1, col=1)
fig.add_trace(go.Bar(x=daily_redemption_count.iloc[:,0], y=daily_redemption_count.iloc[:,1], name='Redemptions', marker_color='#ff6e7f'), row=1, col=2)

fig.update_layout(height=350, showlegend=False, plot_bgcolor='#181c24', paper_bgcolor='#181c24', font_color='#fff')

with tab3:
    st.subheader("Active Facilities")
    st.dataframe(
        active_facilities.groupby(['Country Name', 'Region', 'Technology']).agg({
            'Capacity MW': 'sum',
            'Issuer': 'nunique'
        }).reset_index().sort_values('Capacity MW', ascending=False).head(20),
        use_container_width=True
    )

with tab4:
    st.subheader("Organisations by Region")
    st.dataframe(
        organisations.groupby(['Region', 'Role']).size().unstack(fill_value=0),
        use_container_width=True
    )

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("""
**Data Source:** Evident I-REC Registry Monthly Statistics  
**Reporting Period:** January 2014 to March 2026  
**Compiled:** 7th April 2026
""")