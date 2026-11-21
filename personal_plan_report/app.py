import streamlit as st
import pandas as pd
from utils import load_data, apply_date_filter

st.set_page_config(page_title="Personal Plan", layout="wide", page_icon="📊")
st.title("Personal Plan")
st.caption("Overview — use the sidebar to dive into each area.")

if st.sidebar.button("Refresh Data"):
    st.cache_data.clear()
    st.rerun()

df = load_data()
df_filt = apply_date_filter(df)

if df_filt.empty:
    st.warning("No data in the selected range.")
    st.stop()

# Snapshot metrics
st.header("Current Snapshot")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    latest_weight = df_filt["Weight (lbs)"].dropna()
    val = latest_weight.iloc[-1] if not latest_weight.empty else None
    st.metric("Latest Weight", f"{val:.1f} lbs" if val else "—")

with col2:
    avg_cals = df_filt["Calories"].mean()
    st.metric("Avg Calories / Day", f"{avg_cals:,.0f}" if pd.notna(avg_cals) else "—")

with col3:
    total_workout = df_filt["Workout Minutes"].sum()
    st.metric("Total Workout Min", f"{total_workout:,.0f}" if pd.notna(total_workout) else "—")

with col4:
    total_study = df_filt["Study Hours"].sum()
    st.metric("Total Study Hours", f"{total_study:.1f}" if pd.notna(total_study) else "—")

with col5:
    total_gaming = df_filt["Gaming Hours"].sum()
    st.metric("Total Gaming Hours", f"{total_gaming:.1f}" if pd.notna(total_gaming) else "—")

st.info("Select a page on the left for detailed trends, predictions, and consistency tracking.")

# Quick recent milestones
st.header("Recent Milestones")
if "Milestone / Career Note" in df_filt.columns:
    milestones = df_filt.dropna(subset=["Milestone / Career Note"])
    if not milestones.empty:
        for _, row in milestones.tail(5).iloc[::-1].iterrows():
            st.write(f"**{row['Date'].strftime('%Y-%m-%d')}**: {row['Milestone / Career Note']}")
    else:
        st.write("None logged yet.")
