"""
Non-Human Identity Management Dashboard
-----------------------------------------
A lightweight Streamlit interface on top of the existing pipeline
(discovery.py, risk_scoring.py, classification.py). Run with:

    streamlit run dashboard.py

This must be run from the src/ folder (same place main.py lives),
since it imports from the other modules and expects the CSV at
../data/nhi_inventory.csv, same as main.py.
"""

import pandas as pd
import streamlit as st

from discovery import discover_identities
from risk_scoring import calculate_risk_score
from classification import classify_risk

st.set_page_config(page_title="NHI Management Dashboard", layout="wide")

RISK_COLORS = {
    "CRITICAL": "#dc2626",
    "HIGH": "#f97316",
    "MEDIUM": "#eab308",
    "LOW": "#22c55e",
}


@st.cache_data
def load_and_score(source_path: str) -> pd.DataFrame:
    identities = discover_identities(source_path)

    rows = []
    for identity in identities:
        score = calculate_risk_score(identity)
        label = classify_risk(score)
        rows.append({
            "ID": identity["id"],
            "Name": identity["name"],
            "Type": identity["type"],
            "Owner": identity["owner"],
            "Age (days)": identity["age_days"],
            "Idle (days)": identity["idle_days"],
            "Active": identity["active"],
            "Permissions": ", ".join(identity["permissions"]),
            "Risk Score": score,
            "Risk Level": label,
        })
    return pd.DataFrame(rows)


def color_risk(val):
    color = RISK_COLORS.get(val, "#000000")
    return f"background-color: {color}; color: white; font-weight: bold;"


# ---------- Header ----------
st.title("🔐 Non-Human Identity Management Dashboard")
st.caption("Discovery, risk scoring, and classification for machine identities "
           "(API keys, service accounts, bot tokens, IoT credentials).")

DATA_PATH = "../data/nhi_inventory.csv"

try:
    df = load_and_score(DATA_PATH)
except FileNotFoundError:
    st.error(f"Could not find data file at {DATA_PATH}. "
             f"Run this app from inside the src/ folder.")
    st.stop()

# ---------- Summary metrics ----------
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Identities", len(df))
col2.metric("Critical", int((df["Risk Level"] == "CRITICAL").sum()))
col3.metric("High", int((df["Risk Level"] == "HIGH").sum()))
col4.metric("Medium", int((df["Risk Level"] == "MEDIUM").sum()))
col5.metric("Low", int((df["Risk Level"] == "LOW").sum()))

st.divider()

# ---------- Filters ----------
st.subheader("Identity Inventory")

filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    risk_filter = st.multiselect(
        "Filter by Risk Level",
        options=["CRITICAL", "HIGH", "MEDIUM", "LOW"],
        default=["CRITICAL", "HIGH", "MEDIUM", "LOW"],
    )

with filter_col2:
    type_filter = st.multiselect(
        "Filter by Type",
        options=sorted(df["Type"].unique()),
        default=sorted(df["Type"].unique()),
    )

with filter_col3:
    owner_filter = st.multiselect(
        "Filter by Owner",
        options=sorted(df["Owner"].unique()),
        default=sorted(df["Owner"].unique()),
    )

filtered_df = df[
    df["Risk Level"].isin(risk_filter)
    & df["Type"].isin(type_filter)
    & df["Owner"].isin(owner_filter)
].sort_values("Risk Score", ascending=False)

st.dataframe(
    filtered_df.style.map(color_risk, subset=["Risk Level"]),
    use_container_width=True,
    hide_index=True,
)

# ---------- Alerts panel ----------
st.divider()
st.subheader("🚨 Active Alerts (High / Critical)")

alerts_df = df[df["Risk Level"].isin(["HIGH", "CRITICAL"])].sort_values(
    "Risk Score", ascending=False
)

if alerts_df.empty:
    st.success("No High or Critical risk identities found.")
else:
    for _, row in alerts_df.iterrows():
        icon = "🔴" if row["Risk Level"] == "CRITICAL" else "🟠"
        st.warning(
            f"{icon} **{row['Name']}** (owner: {row['Owner']}) — "
            f"{row['Risk Level']} risk, score {row['Risk Score']}/100"
        )
