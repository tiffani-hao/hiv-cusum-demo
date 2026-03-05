import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

from mock_algo import load_and_prepare, run_mock_cusum

st.set_page_config(page_title="HIV CUSUM Demo (Mock)", layout="wide")
st.title("HIV Cluster Alerts Demo (Mock CUSUM)")
st.caption("This demo runs locally. The 'CUSUM' here is a mock algorithm for UI demonstration.")

# Sidebar settings
with st.sidebar:
    st.header("Settings")
    threshold = st.number_input("Threshold", min_value=0.0, max_value=50.0, value=4.0, step=0.5)

uploaded = st.file_uploader("Upload a CSV (month, county, cases)", type=["csv"])

if uploaded is None:
    st.info("Please upload a CSV file to begin.")
    st.stop()

df = pd.read_csv(uploaded)

if df is None:
    st.stop()

# Prepare data
try:
    prepared = load_and_prepare(df)
except Exception as e:
    st.error(str(e))
    st.stop()

st.subheader("Data preview")
c1, c2, c3 = st.columns(3)
c1.metric("Counties", prepared["county"].nunique())
c2.metric("Months", prepared["month"].nunique())
c3.metric("Range", f"{prepared['month'].min()} → {prepared['month'].max()}")
st.dataframe(prepared.head(20), use_container_width=True)

# Run mock algorithm
per_month, episodes = run_mock_cusum(prepared, threshold=threshold)

st.subheader("Alerts")
if episodes.empty:
    st.info("No alerts detected (try lowering the threshold).")
else:
    st.dataframe(episodes, use_container_width=True)

    # Download alerts
    ep_dl = episodes.copy()
    for c in ["alert_start_month", "detection_month", "alert_end_month"]:
        if c in ep_dl.columns:
            ep_dl[c] = ep_dl[c].astype(str)

    st.download_button(
        "Download alerts.csv",
        data=ep_dl.to_csv(index=False).encode("utf-8"),
        file_name="alerts.csv",
        mime="text/csv",
    )

# Download per-month metrics
pm_dl = per_month.copy()
pm_dl["month"] = pm_dl["month"].astype(str)
st.download_button(
    "Download per_month_metrics.csv",
    data=pm_dl.to_csv(index=False).encode("utf-8"),
    file_name="per_month_metrics.csv",
    mime="text/csv",
)

st.divider()

st.subheader("Visualizations")
county_list = sorted(prepared["county"].unique().tolist())
selected = st.selectbox("Select county", county_list)
col1, col2 = st.columns(2)

g = per_month[per_month["county"] == selected].sort_values("month").copy()
x = g["month"].astype(str).tolist()

# Find alert windows for shading
shades = []
if not episodes.empty:
    ep_c = episodes[episodes["county"] == selected]
    for _, row in ep_c.iterrows():
        start = str(row["alert_start_month"])
        end = None if pd.isna(row["alert_end_month"]) else str(row["alert_end_month"])
        shades.append((start, end))

# Plot 1: cases + baseline
with col1:
    fig1, ax1 = plt.subplots()

    ax1.plot(x, g["cases_raw"], label="cases_raw")
    ax1.plot(x, g["cases_smoothed"], label="cases_smoothed")
    ax1.plot(x, g["baseline"], label="baseline")

    for start, end in shades:
        if start in x:
            i0 = x.index(start)
            i1 = len(x) - 1 if end is None or end not in x else x.index(end)
            ax1.axvspan(i0, i1, alpha=0.15)

    ax1.set_title(f"{selected}: Cases + Baseline (alerts shaded)", fontsize=12)
    ax1.set_xlabel("Year", fontsize=10)
    ax1.set_ylabel("Case Count", fontsize=10)
    ax1.legend(fontsize=8)
    ax1.tick_params(axis="x", labelrotation=90, labelsize=5)
    ax1.tick_params(axis="y", labelsize=5)

    st.pyplot(fig1)

# Plot 2: "CUSUM" curve
with col2:
    fig2, ax2 = plt.subplots()

    ax2.plot(x, g["cusum"], label="cusum (mock)")
    ax2.axhline(threshold, linestyle="--", label="threshold")

    ax2.set_title(f"{selected}: CUSUM", fontsize=12)
    ax2.set_xlabel("Year", fontsize=10)
    ax2.set_ylabel("CUSUM Value", fontsize=10)
    ax2.legend(fontsize=8)
    ax2.tick_params(axis="x", labelrotation=90, labelsize=5)
    ax2.tick_params(axis="y", labelsize=5)

    st.pyplot(fig2)
