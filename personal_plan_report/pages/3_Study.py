import streamlit as st
from utils import load_data, apply_date_filter, get_targets
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Study", layout="wide")
st.title("Study")

df = load_data()
df_filt = apply_date_filter(df)
_, study_target, _, _ = get_targets()

st.header("Study Consistency")

study_df = df_filt.copy()
study_df["Studied"] = study_df["Study Hours"].fillna(0) > 0
study_df["Hit_target"] = study_df["Study Hours"].fillna(0) >= study_target

pct_any = study_df["Studied"].mean() * 100
pct_target = study_df["Hit_target"].mean() * 100

streak = 0
for val in reversed(study_df["Studied"].tolist()):
    if val:
        streak += 1
    else:
        break

col1, col2, col3 = st.columns(3)
col1.metric("% Days with Study", f"{pct_any:.0f}%")
col2.metric(f"% Days ≥ {study_target} hrs", f"{pct_target:.0f}%")
col3.metric("Current Streak", f"{streak} days")

study_df["7d_avg"] = study_df["Study Hours"].fillna(0).rolling(7, min_periods=1).mean()
fig2 = px.line(study_df, x="Date", y="7d_avg", title="7-day Average Study Hours")
st.plotly_chart(fig2, use_container_width=True)

if len(study_df) >= 28:
    recent_s = study_df["Study Hours"].fillna(0).tail(14).mean()
    prior_s = study_df["Study Hours"].fillna(0).iloc[-28:-14].mean()
    if recent_s > prior_s + 0.2:
        s_trend = "Improving"
    elif recent_s < prior_s - 0.2:
        s_trend = "Declining"
    else:
        s_trend = "Stable"
    st.metric("Study Trend (last 14 vs prior 14)", s_trend,
              delta=f"{recent_s - prior_s:+.1f} hrs/day")
else:
    st.info("Need ~4 weeks of data for trend comparison.")

st.header("Daily Study Hours")
fig_study = px.bar(study_df, x="Date", y="Study Hours", title="Daily Study Hours")
fig_study.add_hline(y=study_target, line_dash="dash", annotation_text="Target")
st.plotly_chart(fig_study, use_container_width=True)
