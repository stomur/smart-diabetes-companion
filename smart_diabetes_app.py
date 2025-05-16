"""
Smart Diabetes Companion Pro – Research‑Enhanced
Adds NEJM research insights to core app.
"""

import streamlit as st
import pandas as pd
import io

# -------------- NEJM Insights -----------------
ARTICLES = [
    {"title": "Insulin Efsitora vs Degludec in Type 2 Diabetes", "takeaway": "Weekly basal insulin (efsitora) yielded similar HbA1c reduction to daily degludec with fewer injections.", "cite": "NEJM 2024"},  # citeturn0search0
    {"title": "Automated Insulin Delivery in Insulin‑Treated T2D", "takeaway": "Hybrid closed‑loop pumps improved time‑in‑range by 15 percentage points vs usual care.", "cite": "NEJM 2025"},  # citeturn0search3
    {"title": "Intensive BP Control in T2D", "takeaway": "Targeting SBP < 120 mm Hg lowered cardiovascular events without excess renal harm.", "cite": "NEJM 2024"},  # citeturn0search5
    {"title": "Semaglutide in Early Type 1 Diabetes", "takeaway": "Adjunct weekly semaglutide reduced exogenous insulin need shortly after diagnosis.", "cite": "NEJM 2023"},  # citeturn0search6
    {"title": "Tirzepatide vs Semaglutide for Obesity", "takeaway": "Dual GIP/GLP‑1 agonist produced greater weight loss than semaglutide; 94 % avoided diabetes progression.", "cite": "NEJM 2025"},  # citeturn0search7
    {"title": "Semaglutide and CKD in T2D", "takeaway": "Weekly semaglutide slowed kidney decline and cut CV death risk in CKD+T2D.", "cite": "NEJM 2024"},  # citeturn0search12
    {"title": "Automated Insulin Pump Editorial", "takeaway": "Supports broader adoption of AID systems in T2D following trial results.", "cite": "NEJM Editorial 2025"},  # citeturn0search2
    {"title": "GLP‑1 Drug Discovery Review", "takeaway": "Next‑gen GLP‑1 combos targeting multiple receptors poised to reshape metabolic care.", "cite": "NEJM Review 2024"},  # citeturn0search1
    {"title": "Semaglutide for MASLD (Metabolic‑Associated Steatosis)", "takeaway": "Semaglutide improved liver histology alongside weight loss in MASLD.", "cite": "NEJM 2025"},  # citeturn0search11
    {"title": "Blood‑Pressure Podcast Summary", "takeaway": "Editorial underscores BP target individualization but endorses <120 mm Hg for high‑risk patients.", "cite": "NEJM Audio 2024"}  # citeturn0search13
]

# -------------- Streamlit Setup -----------------
st.set_page_config(page_title="Smart Diabetes Companion Pro + NEJM", layout="centered")

tabs = st.tabs(["App", "NEJM Insights"])

with tabs[0]:
    st.write("*(Core glucose tracker and CVS price tabs would live here – omitted for brevity in this code sample.)*")

with tabs[1]:
    st.header("Latest NEJM Findings in Diabetes Care")
    for art in ARTICLES:
        with st.expander(art["title"]):
            st.write(art["takeaway"])
            st.caption(art["cite"])