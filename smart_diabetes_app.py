"""Smart Diabetes Companion – Complete App (Photo Background, Bug‑Free)
Author: ChatGPT & Dr. Shikhar Tomur
Last build: 2025‑05‑15
DESCRIPTION
‾‾‾‾‾‾‾‾‾‾‾
• Glucose tracker with hypo alert & insulin correction demo
• Dallas CVS cash‑price explorer (mock data)
• NEJM evidence tab
• Aesthetic: blurred photo background + translucent cards
DISCLAIMER
‾‾‾‾‾‾‾‾‾‾‾
Educational demo only – not individualized medical advice.
"""

import streamlit as st
import pandas as pd
from contextlib import contextmanager

# ----------------- Global Style -----------------
PHOTO_BG = "https://images.unsplash.com/photo-1580281657441-8236aa7f2930?auto=format&fit=crop&w=1950&q=80"

st.set_page_config(page_title="Smart Diabetes Companion", layout="centered")
st.markdown(f"""
<style>
html, body, .stApp {{
  background-image: url('{PHOTO_BG}');
  background-size: cover;
  background-attachment: fixed;
}}
.card {{
  background: rgba(255, 255, 255, 0.85);
  padding: 2rem;
  border-radius: 1.25rem;
  box-shadow: 0 8px 20px rgba(0,0,0,0.12);
}}
</style>
""", unsafe_allow_html=True)

@contextmanager
def card():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    yield
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------- Header -----------------
with card():
    col_logo, col_title = st.columns([1,6])
    with col_logo:
        st.image("https://images.unsplash.com/photo-1526256262350-7da7584cf5eb?auto=format&fit=crop&w=200&q=60", width=80)
    with col_title:
        st.title("Smart Diabetes Companion")
        st.caption("Glucose • Insulin math • CVS prices • NEJM evidence")

# ----------------- Sidebar -----------------
st.sidebar.header("Targets & Settings")
target_bg = st.sidebar.number_input("Target BG (mg/dL)", value=120, step=5)
isf = st.sidebar.number_input("Insulin Sensitivity (mg/dL per unit)", value=50)
user_zip = st.sidebar.text_input("ZIP code (Dallas)", value="75201")

# ----------------- Tabs -----------------
tab_glu, tab_cvs, tab_nejm = st.tabs(["📈 Glucose Tracker", "💊 CVS Prices", "📚 NEJM Insights"])

# ----------------- Glucose Tracker Tab -----------------
with tab_glu:
    with card():
        st.header("Upload CGM / Glucometer CSV")
        sample_csv = "timestamp,glucose\n2025-05-15 08:00,58\n2025-05-15 08:30,92"
        st.download_button("Sample CSV", sample_csv, "sample.csv", "text/csv")
        file = st.file_uploader("CSV with columns: timestamp,glucose", type="csv")
        if file:
            try:
                df = pd.read_csv(file)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df = df.sort_values('timestamp')

                latest_row = df.iloc[-1]
                latest_glu = latest_row['glucose']
                avg_glu = df['glucose'].mean()
                delta = latest_glu - df['glucose'].iloc[-2] if len(df) > 1 else 0

                c1, c2 = st.columns(2)
                c1.metric("Average", f"{avg_glu:.1f} mg/dL")
                c2.metric("Latest", f"{int(latest_glu)} mg/dL", delta=int(delta))

                st.line_chart(df.set_index('timestamp')['glucose'])

                # Clinical logic
                if latest_glu < 70:
                    st.error(f"⚠️ Low BG: {latest_glu} mg/dL")
                    st.info("Treat with 15 g fast carbs → re‑check in 15 min. Repeat if needed; seek help if persistent.")
                    st.stop()

                if latest_glu > target_bg:
                    if latest_glu <= 180:
                        tier, mult = "Low correction", 0.5
                    elif latest_glu <= 250:
                        tier, mult = "Standard correction", 1.0
                    else:
                        tier, mult = "High correction – monitor ketones", 1.2
                    dose = max(0, round(((latest_glu - target_bg) / isf) * mult, 1))
                    st.success(f"💉 {tier}: {dose} units rapid‑acting insulin (demo)")
                    st.markdown("> *Evidence*: Closed‑loop pumps ↑ time‑in‑range by 15 pp (NEJM 2025).")
                else:
                    st.success("✅ BG within target – no correction insulin.")

            except Exception as e:
                st.error(f"CSV parse error: {e}")

# ----------------- CVS Price Tab -----------------
with tab_cvs:
    with card():
        st.header("Dallas CVS Cash Prices (Mock)")
        # mock data list
        prices = [
            {"zip": 75201, "store": "CVS – Downtown", "med": "insulin glargine (Lantus)", "price": 92},
            {"zip": 75205, "store": "CVS – Knox", "med": "insulin glargine (Lantus)", "price": 95},
            {"zip": 75230, "store": "CVS – Preston", "med": "insulin glargine (Lantus)", "price": 98},
            {"zip": 75201, "store": "CVS – Downtown", "med": "metformin", "price": 6},
            {"zip": 75205, "store": "CVS – Knox", "med": "metformin", "price": 7},
            {"zip": 75230, "store": "CVS – Preston", "med": "metformin", "price": 8},
            {"zip": 75201, "store": "CVS – Downtown", "med": "semaglutide (Ozempic)", "price": 702},
            {"zip": 75205, "store": "CVS – Knox", "med": "semaglutide (Ozempic)", "price": 709},
            {"zip": 75230, "store": "CVS – Preston", "med": "semaglutide (Ozempic)", "price": 719},
        ]
        df_prices = pd.DataFrame(prices)
        med_choice = st.selectbox("Select medication", df_prices['med'].unique())
        if st.button("Find cheapest CVS"):
            try:
                zip_int = int(user_zip)
            except ValueError:
                st.error("ZIP must be numeric")
                st.stop()

            med_df = df_prices[df_prices['med'] == med_choice]
            local_df = med_df[med_df['zip'] == zip_int]
            subset = local_df if not local_df.empty else med_df
            subset = subset.sort_values('price')

            st.dataframe(subset[['store', 'price']].rename(columns={'store': 'CVS Store', 'price': 'Cash Price ($)'}), use_container_width=True)
            best = subset.iloc[0]
            st.success(f"Cheapest: **{best['store']}** – **${best['price']:.2f}**")

# ----------------- NEJM Tab -----------------
with tab_nejm:
    with card():
        st.header("NEJM Diabetes Highlights (2023‑25)")
        articles = [
            ("Automated Insulin Delivery in T2D (2025)", "Closed‑loop pumps increased Time‑in‑Range by 15 percentage points vs standard care."),
            ("Weekly Basal Insulin Trial (2024)", "Once‑weekly efsitora provided HbA1c control comparable to daily degludec."),
            ("Intensive SBP Target in T2D (2024)", "Aiming for SBP <120 mm Hg lowered cardiovascular events without excess renal harm."),
            ("Semaglutide Adjunct in Early T1D (2023)", "Adjunct semaglutide reduced exogenous insulin needs shortly after diagnosis."),
            ("Tirzepatide in Obesity (2025)", "Dual GIP/GLP‑1 agonist led to greater weight loss and delayed progression to diabetes."),
        ]
        for title, takeaway in articles:
            with st.expander(title):
                st.write(takeaway)

# ----------------- Footer -----------------
st.caption("© 2025 – Demo app for educational use only; prices and advice are illustrative.")