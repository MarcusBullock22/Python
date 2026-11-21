import streamlit as st
from utils import load_data, apply_date_filter, get_targets
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Calories", layout="wide")
st.title("Calories")

df = load_data()
df_filt = apply_date_filter(df)
calorie_target, _, _, _ = get_targets()

st.header("Calorie Deficit")

cal_df = df_filt.dropna(subset=["Calories"]).copy()
if not cal_df.empty:
    cal_df["Deficit"] = calorie_target - cal_df["Calories"]
    cal_df["7d_avg_deficit"] = cal_df["Deficit"].rolling(7, min_periods=1).mean()

    fig = px.line(cal_df, x="Date", y=["Deficit", "7d_avg_deficit"],
                  title="Daily Deficit vs 7-day Average")
    fig.add_hline(y=0, line_dash="dash")
    st.plotly_chart(fig, use_container_width=True)

    avg_deficit = cal_df["Deficit"].mean()
    st.metric("Average Daily Deficit", f"{avg_deficit:,.0f} cal")

    if len(cal_df) >= 28:
        recent = cal_df["Deficit"].tail(14).mean()
        prior = cal_df["Deficit"].iloc[-28:-14].mean()
        if recent > prior + 50:
            trend = "Improving (larger deficit)"
        elif recent < prior - 50:
            trend = "Declining (smaller deficit / surplus)"
        else:
            trend = "Stable"
        st.metric("Deficit Trend (last 14 vs prior 14)", trend,
                  delta=f"{recent - prior:+.0f} cal")
    else:
        st.info("Need ~4 weeks of calorie data for trend comparison.")
else:
    st.info("No calorie data yet.")

st.header("Daily Calories")
if not cal_df.empty:
    fig_cal = px.line(cal_df, x="Date", y="Calories", markers=True, title="Daily Calories")
    fig_cal.add_hline(y=calorie_target, line_dash="dash", annotation_text="Target")
    fig_cal.add_hline(y=cal_df["Calories"].mean(), line_dash="dot", annotation_text="Average")
    st.plotly_chart(fig_cal, use_container_width=True)
