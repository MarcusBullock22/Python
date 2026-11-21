import streamlit as st
from utils import load_data, apply_date_filter, get_targets
import plotly.graph_objects as go
from datetime import timedelta
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Weight", layout="wide")
st.title("Weight")

df = load_data()
df_filt = apply_date_filter(df)
calorie_target, study_target, goal_weight, workout_cal_per_min = get_targets()

# ========== WEIGHT TREND + PROJECTION ==========
st.header("Weight Trend & Projection")

weight_df = df_filt.dropna(subset=["Weight (lbs)"]).copy()
if len(weight_df) >= 3:
    X = np.arange(len(weight_df)).reshape(-1, 1)
    y = weight_df["Weight (lbs)"].values
    model = LinearRegression().fit(X, y)
    slope = model.coef_[0]

    future_days = 90
    future_X = np.arange(len(weight_df), len(weight_df) + future_days).reshape(-1, 1)
    future_pred = model.predict(future_X)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=weight_df["Date"], y=weight_df["Weight (lbs)"],
        mode="lines+markers", name="Actual",
        line=dict(color="#2F5496")
    ))
    fig.add_trace(go.Scatter(
        x=weight_df["Date"], y=model.predict(X),
        mode="lines", name="Trend",
        line=dict(dash="dash", color="orange")
    ))
    future_dates = [weight_df["Date"].iloc[-1] + timedelta(days=i) for i in range(1, future_days + 1)]
    fig.add_trace(go.Scatter(
        x=future_dates, y=future_pred,
        mode="lines", name="90-day Projection",
        line=dict(dash="dot", color="red")
    ))
    fig.update_layout(height=400, xaxis_title="Date", yaxis_title="Weight (lbs)", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Daily Rate", f"{slope:+.3f} lbs/day")
    with col_b:
        st.metric("30-day Projection", f"{future_pred[29]:.1f} lbs")
    with col_c:
        st.metric("90-day Projection", f"{future_pred[89]:.1f} lbs")
else:
    st.info("Need at least 3 weight entries for trend projection.")

# ========== WEIGHT GOAL PREDICTION ==========
st.header("Weight Goal Prediction")

latest_weight = df_filt["Weight (lbs)"].dropna()
if latest_weight.empty:
    st.info("Need at least one weight entry.")
else:
    current_weight = latest_weight.iloc[-1]
    lbs_to_go = current_weight - goal_weight

    recent = df_filt.tail(14)
    avg_cals = recent["Calories"].mean()
    avg_workout_min = recent["Workout Minutes"].fillna(0).mean()

    if pd.isna(avg_cals):
        st.warning("Not enough calorie data for prediction.")
    else:
        st.subheader("What-if adjustments")
        c1, c2 = st.columns(2)
        with c1:
            extra_deficit = st.slider("Extra daily calorie deficit", -500, 1000, 0, 50)
        with c2:
            extra_workout = st.slider("Extra workout minutes / day", -30, 60, 0, 5)

        diet_deficit = calorie_target - avg_cals + extra_deficit
        workout_burn = (avg_workout_min + extra_workout) * workout_cal_per_min
        net_daily_deficit = diet_deficit + workout_burn

        st.write(f"**Current weight:** {current_weight:.1f} lbs")
        st.write(f"**Goal:** {goal_weight:.1f} lbs ({lbs_to_go:+.1f} lbs)")
        st.write(f"**Recent avg calories:** {avg_cals:,.0f}")
        st.write(f"**Recent avg workout:** {avg_workout_min:.0f} min/day")
        st.write(f"**Estimated net daily deficit (with what-if):** {net_daily_deficit:,.0f} cal")

        if net_daily_deficit <= 0:
            st.warning("At this rate you are not in a deficit — projection not available.")
        elif lbs_to_go <= 0:
            st.success("You're already at or below your goal weight.")
        else:
            days_to_goal = (lbs_to_go * 3500) / net_daily_deficit
            weeks = days_to_goal / 7
            st.metric("Estimated days to goal", f"{days_to_goal:.0f} days",
                      delta=f"{weeks:.1f} weeks")

            if days_to_goal < 365:
                future_dates = [df_filt["Date"].max() + timedelta(days=i) for i in range(1, int(days_to_goal)+1)]
                projected_weights = [
                    current_weight - (lbs_to_go * (i / days_to_goal))
                    for i in range(1, int(days_to_goal)+1)
                ]
                fig_proj = go.Figure()
                fig_proj.add_trace(go.Scatter(
                    x=df_filt.dropna(subset=["Weight (lbs)"])["Date"],
                    y=df_filt.dropna(subset=["Weight (lbs)"])["Weight (lbs)"],
                    mode="lines+markers", name="Actual"
                ))
                fig_proj.add_trace(go.Scatter(
                    x=future_dates, y=projected_weights,
                    mode="lines", name="Projected path to goal",
                    line=dict(dash="dot", color="green")
                ))
                fig_proj.add_hline(y=goal_weight, line_dash="dash", annotation_text="Goal")
                fig_proj.update_layout(height=400, title="Projected Path to Goal Weight")
                st.plotly_chart(fig_proj, use_container_width=True)
