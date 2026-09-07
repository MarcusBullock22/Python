import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

st.set_page_config(
    page_title="AI Data Quality Monitor",
    layout="wide"
)

st.title("AI Data Quality Monitor")

st.write(
    "AI-powered anomaly detection for identifying "
    "potential data quality issues."
)

# -----------------------------------
# Generate synthetic transaction data
# -----------------------------------

np.random.seed(42)

record_count = 500

df = pd.DataFrame({
    "transaction_id": range(1, record_count + 1),
    "quantity": np.random.randint(1, 10, record_count),
    "unit_price": np.random.uniform(5, 150, record_count).round(2),
    "discount_percent": np.random.uniform(0, 30, record_count).round(2),
    "days_to_ship": np.random.randint(1, 10, record_count)
})

normal_data = df.copy()

# -----------------------------------
# Add known anomalous records
# -----------------------------------

anomalies = pd.DataFrame({
    "transaction_id": range(501, 511),
    "quantity": [
        100, 150, 75, 200, 125,
        90, 175, 110, 250, 300
    ],
    "unit_price": [
        1200, 950, 1500, 2000, 850,
        1750, 1100, 2500, 1800, 3000
    ],
    "discount_percent": [
        80, 90, 75, 95, 85,
        70, 92, 88, 97, 99
    ],
    "days_to_ship": [
        45, 60, 35, 90, 50,
        40, 75, 55, 100, 120
    ]
})

# Label our known test anomalies
df["known_anomaly"] = 0
anomalies["known_anomaly"] = 1

# Combine normal and anomalous records
df = pd.concat(
    [df, anomalies],
    ignore_index=True
)


# -----------------------------------
# AI anomaly detection
# -----------------------------------

features = [
    "quantity",
    "unit_price",
    "discount_percent",
    "days_to_ship"
]

model = IsolationForest(
    contamination=0.02,
    random_state=42
)

model.fit(normal_data[features])

df["prediction"] = model.predict(df[features])

# Isolation Forest returns:
#  1 = normal
# -1 = anomaly

df["ai_anomaly"] = (
    df["prediction"] == -1
).astype(int)

df["anomaly_score"] = (
    -model.decision_function(df[features])
).round(4)


# -----------------------------------
# Evaluate model performance
# -----------------------------------

true_positives = (
    (df["known_anomaly"] == 1) &
    (df["ai_anomaly"] == 1)
).sum()

false_positives = (
    (df["known_anomaly"] == 0) &
    (df["ai_anomaly"] == 1)
).sum()

false_negatives = (
    (df["known_anomaly"] == 1) &
    (df["ai_anomaly"] == 0)
).sum()

precision = (
    true_positives /
    (true_positives + false_positives)
    if (true_positives + false_positives) > 0
    else 0
)

recall = (
    true_positives /
    (true_positives + false_negatives)
    if (true_positives + false_negatives) > 0
    else 0
)

# -----------------------------------
# Dashboard
# -----------------------------------

st.sidebar.header("Data Input")

uploaded_file = st.sidebar.file_uploader(
    "Upload a CSV file",
    type=["csv"]
)

if uploaded_file is not None:
    uploaded_df = pd.read_csv(uploaded_file)

    missing_columns = [
        column for column in features
        if column not in uploaded_df.columns
    ]

    if missing_columns:
        st.sidebar.error(
            "Uploaded CSV is missing required columns: "
            + ", ".join(missing_columns)
        )
    else:
        uploaded_df["prediction"] = model.predict(
            uploaded_df[features]
        )

        uploaded_df["ai_anomaly"] = (
            uploaded_df["prediction"] == -1
        ).astype(int)

        uploaded_df["anomaly_score"] = (
            -model.decision_function(
                uploaded_df[features]
            )
        ).round(4)

        st.sidebar.success(
            "CSV analyzed successfully."
        )

        st.subheader("Uploaded Dataset Results")

        upload_col1, upload_col2 = st.columns(2)

        upload_col1.metric(
            "Uploaded Records",
            len(uploaded_df)
        )

        upload_col2.metric(
            "Flagged Records",
            int(uploaded_df["ai_anomaly"].sum())
        )

        st.dataframe(
            uploaded_df[
                uploaded_df["ai_anomaly"] == 1
            ].sort_values(
                "anomaly_score",
                ascending=False
            ),
            use_container_width=True
        )
else:
    st.sidebar.info(
        "Using synthetic demonstration dataset."
    )

st.subheader("Synthetic Transaction Data")


st.metric("Total Records", len(df))

st.metric(
    "AI Flagged Records",
    int(df["ai_anomaly"].sum())
)

st.dataframe(
    df,
    use_container_width=True
)

st.subheader("AI Flagged Records")

flagged_records = df[
    df["ai_anomaly"] == 1
].sort_values(
    "anomaly_score",
    ascending=False
)

st.dataframe(
    flagged_records,
    use_container_width=True
)

st.subheader("Model Performance")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Correctly Detected",
    int(true_positives)
)

col2.metric(
    "False Positives",
    int(false_positives)
)

col3.metric(
    "Precision",
    f"{precision:.1%}"
)

col4.metric(
    "Recall",
    f"{recall:.1%}"
)