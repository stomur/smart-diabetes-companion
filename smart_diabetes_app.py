"""Smart Diabetes Companion – Full App (Download Button Fixed)
Author: ChatGPT & Dr. Shikhar Tomur
"""

import streamlit as st
import pandas as pd
import io
from contextlib import contextmanager

# ------------- CSS -------------
BACKGROUND = "https://images.unsplash.com/photo-1580281657441-8236aa7f2930?auto=format&fit=crop&w=1950&q=80"
st.markdown(f"""<style>
.stApp {{
 background-image:url('{BACKGROUND}');
 background-size:cover;
 background-attachment:fixed;
}}
.main-block {{
 background:rgba(255,255,255,0.85);
 padding:2rem;
 border-radius:1.25rem;
 box-shadow:0 10px 25px rgba(0,0,0,0.1);
}}
</style>""", unsafe_allow_html=True)

@contextmanager
def card():
    with st.container():
        st.markdown('<div class="main-block">', unsafe_allow_html=True)
        yield
        st.markdown('</div>', unsafe_allow_html=True)

# Header
with card():
    c1,c2 = st.columns([1,6])
    with c1:
        st.image("https://images.unsplash.com/photo-1526256262350-7da7584cf5eb?auto=format&fit=crop&w=200&q=60", width=80)
    with c2:
        st.title("Smart Diabetes Companion Pro")
        st.caption("Glucose insights • Insulin math • CVS savings • NEJM evidence")

# Sidebar
st.sidebar.header("Settings")
target_bg = st.sidebar.number_input("Target BG (mg/dL)", 120, step=5)
isf = st.sidebar.number_input("Insulin Sensitivity (mg/dL per unit)", 50)
user_zip = st.sidebar.text_input("ZIP (Dallas)", "75201")

# Tabs
glu_tab, price_tab, nejm_tab = st.tabs(["📈 Glucose Tracker", "💊 CVS Prices", "📚 NEJM Insights"])

# --- Glucose tab ---
with glu_tab:
    with card():
        st.header("Upload CGM / Glucometer CSV")
        sample_csv = "timestamp,glucose\n2025-05-14 07:15,58\n2025-05-14 07:45,92"
        st.download_button("Sample CSV", data=sample_csv, file_name="sample.csv", mime="text/csv")
        file = st.file_uploader("CSV (timestamp,glucose)", type="csv")
        if file:
            try:
                df = pd.read_csv(file)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df = df.sort_values('timestamp')
                latest = df.iloc[-1]
                avg = df['glucose'].mean()
                delta = latest['glucose'] - df['glucose'].iloc[-2] if len(df) > 1 else 0
                m1,m2 = st.columns(2)
                m1.metric("Average", f"{avg:.1f} mg/dL")
                m2.metric("Latest", f"{int(latest['glucose'])} mg/dL", delta=int(delta))
                st.line_chart(df.set_index('timestamp')['glucose'])
                current = latest['glucose']
                if current < 70:
                    st.error(f"⚠️ Low BG: {current} mg/dL (<70)")
                    st.info("15‑15 rule: 15 g fast carbs → wait 15 min → re‑check.")
                    st.stop()
                if current > target_bg:
                    if current <= 180:
                        tier,mult = "Low correction",0.5
                    elif current <= 250:
                        tier,mult = "Standard correction",1.0
                    else:
                        tier,mult = "High correction – monitor ketones",1.2
                    dose = max(0, round(((current-target_bg)/isf)*mult,1))
                    st.success(f"💉 {tier}: {dose} units rapid‑acting insulin (demo)")
                    st.markdown("> **Evidence tip:** Closed‑loop pumps improved time‑in‑range by 15 % in NEJM 2025.")
                else:
                    st.success("✔️ Within target – no correction insulin.")
            except Exception as e:
                st.error(f"Parse error: {e}")

# --- CVS Prices ---
with price_tab:
    with card():
        st.header("Dallas CVS Cash Prices (Mock)")
        meds = ["insulin glargine (Lantus)", "metformin", "semaglutide (Ozempic)"]
        med_choice = st.selectbox("Medication", meds)
        if st.button("Cheapest CVS"):
            try:
                z = int(user_zip)
            except ValueError:
                st.error("ZIP must be numeric"); st.stop()
            data = [
                {"zip":75201,"store":"CVS – Downtown","med":"insulin glargine (Lantus)","price":92},
                {"zip":75205,"store":"CVS – Knox","med":"insulin glargine (Lantus)","price":95},
                {"zip":75230,"store":"CVS – Preston","med":"insulin glargine (Lantus)","price":98},
                {"zip":75201,"store":"CVS – Downtown","med":"metformin","price":6},
                {"zip":75205,"store":"CVS – Knox","med":"metformin","price":7},
                {"zip":75230,"store":"CVS – Preston","med":"metformin","price":8},
                {"zip":75201,"store":"CVS – Downtown","med":"semaglutide (Ozempic)","price":702},
                {"zip":75205,"store":"CVS – Knox","med":"semaglutide (Ozempic)","price":709},
                {"zip":75230,"store":"CVS – Preston","med":"semaglutide (Ozempic)","price":719},
            ]
            df = pd.DataFrame(data)
            df = df[df['med']==med_choice]
            subset = df[df['zip']==z] or df
            subset = (df[df['zip']==z] if not df[df['zip']==z].empty else df).sort_values('price')
            st.dataframe(subset[['store','price']].rename(columns={'store':'CVS Store','price':'Cash Price ($)'}), use_container_width=True)
            best = subset.iloc[0]
            st.success(f"Best price: ${best['price']:.2f} at {best['store']}")

# --- NEJM ---
with nejm_tab:
    with card():
        st.header("NEJM Highlights 2023‑25")
        articles = [
            ("Insulin Efsitora vs Degludec, 2024","Weekly basal insulin similar HbA1c, fewer injections."),
            ("Automated Insulin Delivery in T2D, 2025","Closed‑loop pumps ↑ time‑in‑range by 15 pp."),
            ("Intensive BP Control in T2D, 2024","Target SBP <120 mm Hg lowered CV events."),
            ("Semaglutide Early T1D, 2023","Adjunct semaglutide cut insulin needs."),
            ("Tirzepatide vs Semaglutide, 2025","GIP/GLP‑1 agonist > weight loss, diabetes delay."),
        ]
        for t, d in articles:
            with st.expander(t):
                st.write(d)

st.caption("© 2025 Demo – fixed download button")