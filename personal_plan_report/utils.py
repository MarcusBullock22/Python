import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

SHEET_ID = os.environ.get("GOOGLE_SHEET_ID")
GID = os.environ.get("GOOGLE_SHEET_GID")
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}" if SHEET_ID and GID else None

@st.cache_data(ttl=60)
def load_data():
    if not SHEET_ID or not GID:
        st.error("Missing environment variables: GOOGLE_SHEET_ID and/or GOOGLE_SHEET_GID")
        st.stop()

    df = pd.read_csv(CSV_URL)
    df = df.dropna(subset=["Date"]).copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"]).sort_values("Date").reset_index(drop=True)

    numeric_cols = [
        "Weight (lbs)", "Workout Minutes", "Eating Score (1-5)",
        "Calories", "Study Hours", "Gaming Hours"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(",", "", regex=False)
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

def apply_date_filter(df):
    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key="date_filter"
    )
    if len(date_range) == 2:
        mask = (df["Date"].dt.date >= date_range[0]) & (df["Date"].dt.date <= date_range[1])
        return df.loc[mask].copy()
    return df.copy()

def get_targets():
    st.sidebar.header("Targets")
    calorie_target = st.sidebar.number_input("Daily Calorie Target", value=2000, step=50, key="cal_target")
    study_target = st.sidebar.number_input("Daily Study Hours Target", value=1.0, step=0.5, key="study_target")
    goal_weight = st.sidebar.number_input("Goal Weight (lbs)", value=190.0, step=1.0, key="goal_weight")
    workout_cal_per_min = st.sidebar.number_input("Est. Cal Burned per Workout Min", value=8.0, step=0.5, key="workout_cal")
    return calorie_target, study_target, goal_weight, workout_cal_per_min
