"""Smart Diabetes Companion Pro – Full App with NEJM Insights
Author: ChatGPT & Dr. Shikhar Tomur
DISCLAIMER: Educational demo only – NOT individualized medical advice.
"""

import streamlit as st
import pandas as pd
import io

# ---------- UI CSS ----------
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

from contextlib import contextmanager
@contextmanager
def card():
    with st.container():
        st.markdown('<div class="main-block">', unsafe_allow_html=True)
        yield
        st.markdown('</div>', unsafe_allow_html=True)

# ---------- Header ----------
with card():
    c1,c2 = st.columns([1,6])
    with c1:
        st.image("https://images.unsplash.com/photo-1526256262350-7da7584cf5eb?auto=format&fit=crop&w=200&q=60", width=80)
    with c2:
        st.title("Smart Diabetes Companion Pro")
        st.caption("Glucose insights • Insulin math • CVS savings • NEJM evidence")

# ---------- Sidebar ----------
st.sidebar.header("Settings")
target_bg = st.sidebar.number_input("Target BG (mg/dL)", 120, step=5)
isf = st.sidebar.number_input("Insulin Sensitivity (mg/dL per unit)", 50)
user_zip = st.sidebar.text_input("ZIP (Dallas)", "75201")

# ---------- Tabs ----------
glu_tab, price_tab, nejm_tab = st.tabs(["📈 Glucose Tracker", "💊 CVS Prices", "📚 NEJM Insights"])

# ---------- Glucose Tracker ----------
with glu_tab:
    with card():
        st.header("Upload CGM / Glucometer CSV")
        st.download_button("Sample CSV", "timestamp,glucose\n2025-05-14 07:15,58\n2025-05-14 07:45,92", file_name="sample.csv", type="text/csv")
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
                    # NEJM evidence prompts
                    st.markdown("> **Evidence tip:** A recent NEJM RCT of automated insulin delivery added **15 % more time‑in‑range** for insulin‑treated T2D (McAuley *et al.*, 2025). Consider discussing AID systems with your provider.")
                else:
                    st.success("✔️ Within target – no correction insulin.")
            except Exception as e:
                st.error(f"Parse error: {e}")

# ---------- CVS Prices ----------
with price_tab:
    with card():
        st.header("Dallas CVS Cash Prices (Mock)")
        meds = ["insulin glargine (Lantus)", "metformin", "semaglutide (Ozempic)"]
        med_choice = st.selectbox("Medication", meds)
        if st.button("Cheapest CVS", key="price_btn"):
            try:
                z = int(user_zip)
            except ValueError:
                st.error("ZIP must be numeric")
                st.stop()
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
            local = df[df['zip']==z]
            subset = local if not local.empty else df
            subset = subset.sort_values('price')
            st.dataframe(subset[['store','price']].rename(columns={'store':'CVS Store','price':'Cash Price ($)'}), use_container_width=True)
            best = subset.iloc[0]
            st.success(f"Best price: ${best['price']:.2f} at {best['store']}")

# ---------- NEJM Insights ----------
with nejm_tab:
    with card():
        st.header("NEJM Highlights (2023‑25)")
        ARTICLES = [
            ("Insulin Efsitora vs Degludec, 2024", "Once‑weekly basal insulin matched daily degludec for HbA1c with fewer injections."),
            ("Automated Insulin Delivery in T2D, 2025", "Closed‑loop pumps increased time‑in‑range by 15 pp vs standard care."),
            ("Intensive BP Control in T2D, 2024", "Target SBP <120 mm Hg lowered CV events without renal harm."),
            ("Semaglutide in Early T1D, 2023", "Adjunct semaglutide reduced insulin needs shortly after diagnosis."),
            ("Tirzepatide vs Semaglutide in Obesity, 2025", "Dual GIP/GLP‑1 agonist produced greater weight loss and delayed diabetes."),
            ("Semaglutide for CKD in T2D, 2024", "Weekly semaglutide slowed kidney decline & reduced CV death."),
            ("GLP‑1 Multi‑Agonist Review, 2024", "Next‑gen GLP‑1 combos poised to transform metabolic care."),
            ("Semaglutide Improves MASLD, 2025", "Weight‑loss agent also improved liver histology in MASLD."),
            ("AID Editorial, 2025", "NEJM editors support mainstream adoption of AID in insulin‑treated T2D."),
            ("BP Target Podcast, 2024", "Expert panel endorses <120 mm Hg SBP for high‑risk diabetes.")
        ]
        for title, takeaway in ARTICLES:
            with st.expander(title):
                st.write(takeaway)

# ---------- Footer ----------
st.markdown("<hr style='border-top:1px solid #bbb;'>", unsafe_allow_html=True)
st.caption("© 2025 – Demo only. Evidence summaries from NEJM 2023‑2025.")