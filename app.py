"""Streamlit web page for the Name Screening Tool.
Run with:  streamlit run app.py
"""
import pandas as pd
import streamlit as st
from screening import screen_name, screen_customers, HIT_THRESHOLD, REVIEW_THRESHOLD

st.set_page_config(page_title="KYC Name Screening", page_icon="🔎", layout="wide")
st.title("🔎 KYC Name Screening Tool")
st.caption("Checks names against a sanctions / PEP list using fuzzy matching. Demo with FAKE data.")

# --- Watchlist: sample file or your own upload --------------------------------
st.sidebar.header("Settings")
uploaded = st.sidebar.file_uploader("Upload your own watchlist (CSV with column: name, list_type)", type="csv")
if uploaded:
    watchlist = pd.read_csv(uploaded)
    if "list_type" not in watchlist.columns:
        watchlist["list_type"] = "UNKNOWN"
else:
    watchlist = pd.read_csv("sanctions_sample.csv")
st.sidebar.write(f"Watchlist size: **{len(watchlist)}** names")
st.sidebar.write(f"HIT: score ≥ {HIT_THRESHOLD}  \nPOSSIBLE: score ≥ {REVIEW_THRESHOLD}")

tab1, tab2 = st.tabs(["Check one name", "Check a customer file"])

# --- Tab 1: single name --------------------------------------------------------
with tab1:
    name = st.text_input("Customer name", placeholder="e.g. Mohamad Al Hasan")
    if name:
        res = screen_name(name, watchlist, top_n=5)
        best = res.iloc[0]
        if best["status"] == "HIT":
            st.error(f"HIT: '{name}' is very similar to '{best['name']}' ({best['match_score']}%)")
        elif best["status"] == "POSSIBLE":
            st.warning(f"POSSIBLE match with '{best['name']}' ({best['match_score']}%). Check by hand.")
        else:
            st.success("No match found. CLEAR.")
        st.dataframe(res, use_container_width=True)

# --- Tab 2: CSV of customers ---------------------------------------------------
with tab2:
    file = st.file_uploader("Upload customers CSV (columns: customer_id, full_name)", type="csv", key="cust")
    if file:
        customers = pd.read_csv(file)
    else:
        customers = pd.read_csv("customers.csv")
        st.info("Showing the sample customers. Upload your own CSV to replace them.")
    report = screen_customers(customers, watchlist)

    c1, c2, c3 = st.columns(3)
    c1.metric("HIT", int((report["status"] == "HIT").sum()))
    c2.metric("POSSIBLE", int((report["status"] == "POSSIBLE").sum()))
    c3.metric("CLEAR", int((report["status"] == "CLEAR").sum()))

    st.dataframe(report, use_container_width=True)
    st.download_button("Download report (CSV)", report.to_csv(index=False), "screening_report.csv")
