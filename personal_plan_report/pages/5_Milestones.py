import streamlit as st
from utils import load_data, apply_date_filter

st.set_page_config(page_title="Milestones", layout="wide")
st.title("Milestones")

df = load_data()
df_filt = apply_date_filter(df)

st.header("All Milestones")

if "Milestone / Career Note" in df_filt.columns:
    milestones = df_filt.dropna(subset=["Milestone / Career Note"])
    if not milestones.empty:
        for _, row in milestones.iloc[::-1].iterrows():
            st.write(f"**{row['Date'].strftime('%Y-%m-%d')}**: {row['Milestone / Career Note']}")
    else:
        st.info("No milestones logged yet.")
else:
    st.info("Milestone column not found.")
