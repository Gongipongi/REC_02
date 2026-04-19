"""
I-REC Market Dashboard - March 2026
A comprehensive dashboard for understanding the I-REC market
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="I-REC Market Dashboard - March 2026",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# CSS
# ==============================
st.markdown("""
<style>
.metric-card {
    background: linear-gradient(135deg, #43cea2 0%, #185a9d 100%);
    border-radius: 14px;
    padding: 20px;
    text-align: center;
}
.metric-value {
    font-size: 36px;
    font-weight: bold;
    color: #fff;
}
.metric-label {
    font-size: 15px;
    color: #e0e0e0;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# LOAD DATA (FIXED ONLY HERE)
# ==============================
@st.cache_data
def load_data():
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        # 👇 IMPORTANT: matches your GitHub file EXACTLY
        file_path = os.path.join(BASE_DIR, "I-REC-Registry-Data-March-2026 (1).xlsx")

        xl = pd.ExcelFile(file_path)

        issuances = pd.read_excel(
            xl,
            sheet_name="Issuances",
            parse_dates=['Issue Date', 'Commissioning Date']
        )
        issuances = issuances[issuances['Issue Date'].dt.month == 3]

        redemptions = pd.read_excel(
            xl,
            sheet_name="Redemptions",
            parse_dates=['Redemption Date']
        )
        redemptions = redemptions[redemptions['Redemption Date'].dt.month == 3]

        organisations = pd.read_excel(
            xl,
            sheet_name="Organisations",
            parse_dates=['Registration Date']
        )

        facilities = pd.read_excel(
            xl,
            sheet_name="Facilities",
            parse_dates=['Registration Date', 'Commissioning Date']
        )

        return issuances, organisations, facilities, redemptions

    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

# ==============================
# LOAD DATA
# ==============================
with st.spinner("Loading I-REC data..."):
    issuances, organisations, facilities, redemptions = load_data()

march_issuances = issuances
march_redemptions = redemptions

# ==============================
# SIDEBAR
# ==============================
st.sidebar.title("📊 I-REC Dashboard")
st.sidebar.markdown("### March 2026 Data")
st.sidebar.info("Data: Jan 2014 → March 2026")

# ==============================
# TITLE
# ==============================
st.title("⚡ I-REC Market Dashboard")
st.markdown("### March 2026")

# ==============================
# METRICS
# ==============================
st.markdown("## 📈 Key Metrics")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Issued", f"{march_issuances['Volume Issued'].sum():,.0f}")

with col2:
    st.metric("Redeemed", f"{march_redemptions['Volume Redeemed'].sum():,.0f}")

with col3:
    st.metric("Transactions", len(march_issuances))

with col4:
    st.metric("Active Facilities", len(facilities[facilities["Active Status"] == True]))

with col5:
    st.metric("Organisations", len(organisations))

st.markdown("---")

# ==============================
# DAILY ISSUANCE
# ==============================
daily_issuance = march_issuances.groupby(
    march_issuances['Issue Date'].dt.date
)['Volume Issued'].sum().reset_index()

daily_issuance.columns = ['Date', 'Volume']

fig = px.line(daily_issuance, x='Date', y='Volume', title="Daily Issuance", markers=True)
st.plotly_chart(fig, use_container_width=True)

# ==============================
# DAILY REDEMPTION
# ==============================
daily_redemption = march_redemptions.groupby(
    march_redemptions['Redemption Date'].dt.date
)['Volume Redeemed'].sum().reset_index()

daily_redemption.columns = ['Date', 'Volume']

fig = px.line(daily_redemption, x='Date', y='Volume', title="Daily Redemption", markers=True)
st.plotly_chart(fig, use_container_width=True)

# ==============================
# ISSUANCE ANALYSIS
# ==============================
st.markdown("## 🔋 Issuance Analysis")

country_issuance = march_issuances.groupby(
    'Country Name'
)['Volume Issued'].sum().sort_values(ascending=False).head(10)

fig = px.bar(
    x=country_issuance.values,
    y=country_issuance.index,
    orientation='h',
    title='Top Countries by Issuance'
)
st.plotly_chart(fig, use_container_width=True)

# ==============================
# REDEMPTION ANALYSIS
# ==============================
st.markdown("## ✅ Redemption Analysis")

beneficiary = march_redemptions.groupby(
    'Country Name - Beneficiary'
)['Volume Redeemed'].sum().sort_values(ascending=False).head(10)

fig = px.bar(
    x=beneficiary.values,
    y=beneficiary.index,
    orientation='h',
    title='Top Beneficiary Countries'
)
st.plotly_chart(fig, use_container_width=True)

# ==============================
# FACILITIES
# ==============================
st.markdown("## 🏭 Facilities")

active_facilities = facilities[facilities['Active Status'] == True]

st.metric("Total Active Capacity (MW)", f"{active_facilities['Capacity MW'].sum():,.0f}")

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.markdown("""
**Data Source:** Evident I-REC Registry  
**Reporting Period:** Jan 2014 → March 2026  
""")
