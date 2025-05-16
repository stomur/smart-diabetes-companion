"""
Smart Diabetes Companion Pro – Streamlit Demo App
Author: ChatGPT & Dr. Shikhar Tomur
Purpose: MBA final project showcase – combines glucose analytics, insulin dose calculator,
hypoglycemia management tips, and Dallas‑only CVS cash‑price explorer.

DISCLAIMER: Educational demo only – NOT individualized medical advice.
"""

import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import datetime

# ---------- Page config ----------
st.set_page_config(page_title="Smart Diabetes Companion Pro", page_icon="💉", layout="centered")

st.title("💉 Smart Diabetes Companion Pro")
st.caption("Glucose insights, on‑the‑fly insulin math, and local CVS price savings – all in one demo.")

# ---------- Sidebar – patient profile ----------
st.sidebar.header("🩺 Patient Profile & Settings")
target_bg = st.sidebar.number_input("Target BG (mg/dL)", value=120, step=5)
isf = st.sidebar.number_input("Insulin Sensitivity Factor (mg/dL ↓ per unit)", value=50, step=1)
user_zip = st.sidebar.text_input("ZIP code (Dallas only demo)", value="75201")

st.sidebar.markdown("""---  
**How doses are calculated**  
* Low tier 120‑180 mg/dL → 0.5 × standard correction  
* Mid tier 181‑250 mg/dL → standard correction  
* High tier > 250 mg/dL → 1.2 × standard correction  
(Standard: (current – target)/ISF)  
""")

# ---------- Tab layout ----------
glu_tab, price_tab = st.tabs(["📈 Glucose Tracker", "💊 Dallas CVS Prices"])

# ================================================================
# 1. Glucose Tracker tab
# ================================================================
with glu_tab:
    st.header("📈 Upload CGM/Glucometer CSV")
    st.markdown("CSV must include `timestamp` and `glucose` columns. Example row: `2025-05-15 08:00,132`.")
    up = st.file_uploader("Upload readings", type="csv")

    if up:
        try:
            df = pd.read_csv(up)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            latest = df.iloc[-1]
            avg = df['glucose'].mean()
            delta = latest['glucose'] - df['glucose'].iloc[-2] if len(df) > 1 else 0

            col1, col2 = st.columns(2)
            col1.metric("Average", f"{avg:.1f} mg/dL")
            col2.metric("Latest", f"{int(latest['glucose'])} mg/dL", delta=int(delta))

            st.line_chart(df.set_index('timestamp')['glucose'])

            current = latest['glucose']

            # Hypoglycemia workflow
            if current < 70:
                st.error(f"❗ Low blood sugar detected: **{current} mg/dL** (target ≥ 70)")
                st.markdown("### Immediate Treatment (15‑15 Rule)")
                st.info("Eat **15 g** of fast‑acting carbs (e.g., 4 oz juice, 3‑4 glucose tabs).\n\nRe‑check BG after **15 minutes**. If still < 70 mg/dL, repeat once and call your provider / 911 if symptoms persist.")
                st.stop()

            # Hyperglycemia – calculate correction dose
            if current > target_bg:
                if current <= 180:
                    tier = "Low correction"
                    factor = 0.5
                elif current <= 250:
                    tier = "Standard correction"
                    factor = 1.0
                else:
                    tier = "High correction – monitor ketones"
                    factor = 1.2
                dose = ((current - target_bg) / isf) * factor
                dose = max(0, round(dose, 1))
                st.success(f"💉 **{tier}: {dose} units** of rapid‑acting insulin suggested (education only)")
            else:
                st.success("✔️ BG at or below target – no correction insulin needed.")

        except Exception as e:
            st.error(f"Error parsing CSV: {e}")

# ================================================================
# 2. Price Explorer tab – Dallas CVS
# ================================================================
with price_tab:
    st.header("💊 Compare Cash Prices – Dallas CVS Pharmacies")
    st.markdown("All prices are demo values. Query limited to CVS stores in Dallas ZIPs.")

    DATA = [
        {"zip": 75201, "store": "CVS – Downtown Main St", "med": "insulin glargine (Lantus)", "price": 92},
        {"zip": 75205, "store": "CVS – Knox & Henderson", "med": "insulin glargine (Lantus)", "price": 95},
        {"zip": 75230, "store": "CVS – Preston Center", "med": "insulin glargine (Lantus)", "price": 98},
        {"zip": 75201, "store": "CVS – Downtown Main St", "med": "metformin", "price": 6},
        {"zip": 75205, "store": "CVS – Knox & Henderson", "med": "metformin", "price": 7},
        {"zip": 75230, "store": "CVS – Preston Center", "med": "metformin", "price": 8},
        {"zip": 75201, "store": "CVS – Downtown Main St", "med": "semaglutide (Ozempic)", "price": 702},
        {"zip": 75205, "store": "CVS – Knox & Henderson", "med": "semaglutide (Ozempic)", "price": 709},
        {"zip": 75230, "store": "CVS – Preston Center", "med": "semaglutide (Ozempic)", "price": 719},
    ]
    price_df = pd.DataFrame(DATA)
    meds = price_df['med'].unique().tolist()
    selected_med = st.selectbox("Medication", meds)
    if st.button("Find Cheapest CVS", use_container_width=True):
        try:
            z = int(user_zip)
        except ValueError:
            st.error("ZIP must be numeric")
            st.stop()
        subset = price_df[(price_df['zip'] == z) & (price_df['med'] == selected_med)]
        if subset.empty():
            subset = price_df[price_df['med'] == selected_med]  # show all Dallas CVS as fallback
            st.info("No CVS store in that ZIP – showing other Dallas CVS prices instead.")
        subset = subset.sort_values('price')
        st.table(subset[['store', 'price']].rename(columns={'store': 'CVS Store', 'price': 'Cash Price ($)'}).set_index('CVS Store'))
        best = subset.iloc[0]
        st.success(f"Best CVS price: **${best['price']:.2f}** at **{best['store']}**")

# ---------- Footer ----------
st.divider()
st.caption("© 2025 – Demo app for educational use only. Not medical advice. Prices mock‑data.")