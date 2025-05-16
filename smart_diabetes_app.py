"""
Smart Diabetes Companion Pro – Streamlit Demo App (Beauty Pass)
Author: ChatGPT & Dr. Shikhar Tomur
Purpose: MBA final project showcase – now with polished UI, hero imagery, and API-ready drug pricing module.

DISCLAIMER: Educational demo only – NOT individualized medical advice.
"""

import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import datetime

# --------------------------------------------------
# 🎨  GLOBAL LOOK-AND-FEEL (simple CSS)
# --------------------------------------------------
page_bg = "https://images.unsplash.com/photo-1580281657441-8236aa7f2930?auto=format&fit=crop&w=1950&q=80"
page_overlay_css = f"""
<style>
.stApp {{
    background-image: url({page_bg});
    background-size: cover;
    background-attachment: fixed;
}}
.main-block {{
    background-color: rgba(255, 255, 255, 0.85);
    padding: 2rem 2rem 3rem 2rem;
    border-radius: 1.25rem;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}}
</style>
"""

st.markdown(page_overlay_css, unsafe_allow_html=True)

from contextlib import contextmanager
@contextmanager
def card():
    with st.container():
        st.markdown('<div class="main-block">', unsafe_allow_html=True)
        yield
        st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# 🚀  HEADER
# --------------------------------------------------
with card():
    col_logo, col_title = st.columns([1,6])
    with col_logo:
        st.image("https://images.unsplash.com/photo-1526256262350-7da7584cf5eb?auto=format&fit=crop&w=200&q=60", width=80)
    with col_title:
        st.title("Smart Diabetes Companion Pro")
        st.caption("Glucose insights • Insulin math • Local CVS savings")

# --------------------------------------------------
# 🩺 SIDEBAR – Patient Settings
# --------------------------------------------------
st.sidebar.header("Settings")
target_bg = st.sidebar.number_input("Target BG (mg/dL)", value=120, step=5)
isf = st.sidebar.number_input("Insulin Sensitivity (mg/dL ↑ per unit)", value=50)
user_zip = st.sidebar.text_input("ZIP code (Dallas)", value="75201")
st.sidebar.markdown("<small>Correction tiers: 0.5× (120‑180) | 1× (181‑250) | 1.2× (>250)</small>", unsafe_allow_html=True)

# --------------------------------------------------
# 🔄  MAIN TABS
# --------------------------------------------------
glu_tab, price_tab = st.tabs(["📈 Glucose Tracker", "💊 CVS Prices"])

# ========================================================
# 1️⃣  GLUCOSE TAB
# ========================================================
with glu_tab:
    with card():
        st.header("Upload CGM / Glucometer CSV")
        st.markdown("Columns required: **timestamp**, **glucose** (mg/dL). Example: `2025-05-15 08:00,132`. Use the sample file below for a quick spin.")
        st.download_button("Download sample low-BG CSV", "timestamp,glucose\n2025-05-14 07:15,58\n2025-05-14 07:45,92", file_name="sample_low.csv", type="text/csv")

        upl = st.file_uploader("Drag & drop CSV", type="csv")
        if upl:
            try:
                df = pd.read_csv(upl)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df = df.sort_values('timestamp')

                latest = df.iloc[-1]
                avg = df['glucose'].mean()
                delta = latest['glucose'] - df['glucose'].iloc[-2] if len(df) > 1 else 0

                m1, m2 = st.columns(2)
                m1.metric("Average", f"{avg:.1f} mg/dL")
                m2.metric("Latest", f"{int(latest['glucose'])} mg/dL", delta=int(delta))

                st.line_chart(df.set_index('timestamp')['glucose'])

                current = latest['glucose']

                if current < 70:
                    st.error(f"⚠️ Low BG: {current} mg/dL (<70)")
                    st.markdown("### 15-15 Rule – Immediate Action")
                    st.info("1️⃣ Eat **15 g** fast carbs (4 oz juice / 3-4 glucose tabs).\n\n2️⃣ Re-check BG after **15 min**.\n\n3️⃣ If still <70 → repeat once & call provider/911 if symptoms persist.")
                    st.stop()

                if current > target_bg:
                    if current <= 180:
                        tier, mult = "Low correction", 0.5
                    elif current <= 250:
                        tier, mult = "Standard correction", 1.0
                    else:
                        tier, mult = "High correction – monitor ketones", 1.2
                    dose = max(0, round(((current - target_bg)/isf)*mult, 1))
                    st.success(f"💉 **{tier}: {dose} units** rapid-acting insulin suggested (demo)")
                else:
                    st.success("✔️ BG within target – no correction insulin needed.")
            except Exception as e:
                st.error(f"Failed to parse CSV: {e}")

# ========================================================
# 2️⃣  CVS PRICE TAB – API READY
# ========================================================
with price_tab:
    with card():
        st.header("Compare Cash Prices (CVS Dallas)")
        st.markdown("Prices via <small>mock data</small>. Replace **`get_cvs_prices()`** with live GoodRx API call for production.", unsafe_allow_html=True)

        def get_cvs_prices(zip_code: int, med: str):
            MOCK = [
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
            df = pd.DataFrame(MOCK)
            df = df[df['med'] == med]
            local = df[df['zip'] == zip_code]
            return local if not local.empty else df

        meds_list = ["insulin glargine (Lantus)", "metformin", "semaglutide (Ozempic)"]
        med_choice = st.selectbox("Medication", meds_list)
        if st.button("Find Cheapest CVS", use_container_width=True):
            try:
                zip_int = int(user_zip)
            except ValueError:
                st.error("ZIP must be numeric")
                st.stop()
            prices_df = get_cvs_prices(zip_int, med_choice).sort_values('price')
            st.dataframe(prices_df[['store', 'price']].rename(columns={'store':'CVS Store','price':'Cash Price ($)'}), use_container_width=True)
            best = prices_df.iloc[0]
            st.success(f"Best price: **${best['price']:.2f}** at **{best['store']}**")
            st.image("https://images.unsplash.com/photo-1604441596988-c3944a58b126?auto=format&fit=crop&w=1200&q=80", caption="CVS Pharmacy – Dallas", use_column_width=True)

# ----------------- FOOTER -----------------
st.markdown("<hr style='border-top: 1px solid #bbb;'>", unsafe_allow_html=True)
st.caption("© 2025 – Demo only. Data and guidance for educational purposes.")