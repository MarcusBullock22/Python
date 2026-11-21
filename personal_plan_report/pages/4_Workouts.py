import streamlit as st
from utils import load_data, apply_date_filter
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Workouts", layout="wide")
st.title("Workouts")

df = load_data()
df_filt = apply_date_filter(df)

st.header("Workout Consistency")

workout_df = df_filt.copy()
workout_df["Worked_out"] = workout_df["Workout Minutes"].fillna(0) > 0

pct_workout = workout_df["Worked_out"].mean() * 100

w_streak = 0
for val in reversed(workout_df["Worked_out"].tolist()):
    if val:
        w_streak += 1
    else:
        break

col1, col2 = st.columns(2)
col1.metric("% Days with Workout", f"{pct_workout:.0f}%")
col2.metric("Current Streak", f"{w_streak} days")

workout_df["7d_avg_min"] = workout_df["Workout Minutes"].fillna(0).rolling(7, min_periods=1).mean()
fig_w = px.line(workout_df, x="Date", y="7d_avg_min", title="7-day Average Workout Minutes")
st.plotly_chart(fig_w, use_container_width=True)

if len(workout_df) >= 28:
    recent_w = workout_df["Workout Minutes"].fillna(0).tail(14).mean()
    prior_w = workout_df["Workout Minutes"].fillna(0).iloc[-28:-14].mean()
    if recent_w > prior_w + 5:
        w_trend = "Improving"
    elif recent_w < prior_w - 5:
        w_trend = "Declining"
    else:
        w_trend = "Stable"
    st.metric("Workout Trend (last 14 vs prior 14)", w_trend,
              delta=f"{recent_w - prior_w:+.0f} min/day")
else:
    st.info("Need ~4 weeks of data for workout trend comparison.")

st.header("Daily Workout Minutes")
fig_daily = px.bar(workout_df, x="Date", y="Workout Minutes", title="Daily Workout Minutes")
st.plotly_chart(fig_daily, use_container_width=True)
