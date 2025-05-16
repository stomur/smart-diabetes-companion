
"""
Smart Diabetes Companion – META Summit Edition
Showcase-level Streamlit app combining:
  • Glucose analytics
  • Dynamic medication pricing (Dallas CVS)
  • Static map thumbnails
  • Comprehensive medication & emergency guide
  • Evidence feed from NEJM
  • Performance best practices (cache, forms, session state)
"""

import streamlit as st
import pandas as pd
from contextlib import contextmanager

# ---------- Config ----------
st.set_page_config(page_title="Smart Diabetes Companion", page_icon="💉", layout="centered")

# ---------- Styles ----------
BG = "https://images.unsplash.com/photo-1580281657441-8236aa7f2930?auto=format&fit=crop&w=1950&q=80"
st.markdown(
    f"""
    <style>
    html,body,.stApp {{
        background-image:url('{BG}');
        background-size:cover;
        background-attachment:fixed;
    }}
    .card {{
        background:rgba(255,255,255,.9);
        padding:2rem;
        border-radius:1.25rem;
        box-shadow:0 6px 16px rgba(0,0,0,.1);
    }}
    .small {{font-size:0.85rem}}
    </style>
    """, unsafe_allow_html=True)

@contextmanager
def card():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    yield
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Header ----------
with card():
    st.image("https://images.unsplash.com/photo-1526256262350-7da7584cf5eb?auto=format&fit=crop&w=200&q=60", width=70)
    st.title("Smart Diabetes Companion – META Summit Demo")
    st.caption("Evidence‑powered, patient‑centric diabetes assistant")

# ---------- Sidebar Targets ----------
st.sidebar.header("Patient Targets")
target_bg = st.sidebar.number_input("Target BG (mg/dL)", 120, step=5)
isf       = st.sidebar.number_input("Insulin Sensitivity Factor", 50)
user_zip  = st.sidebar.text_input("ZIP (Dallas)", "75201")

# ---------- Data ----------
@st.cache_data
def cvs_data():
    return pd.DataFrame([
        {"zip":75201,"store":"CVS Downtown","med":"insulin glargine (Lantus)","price":92,"lat":32.779,"lon":-96.799},
        {"zip":75205,"store":"CVS Knox","med":"insulin glargine (Lantus)","price":95,"lat":32.821,"lon":-96.788},
        {"zip":75230,"store":"CVS Preston","med":"insulin glargine (Lantus)","price":98,"lat":32.864,"lon":-96.807},
        {"zip":75201,"store":"CVS Downtown","med":"metformin","price":6,"lat":32.779,"lon":-96.799},
        {"zip":75205,"store":"CVS Knox","med":"metformin","price":7,"lat":32.821,"lon":-96.788},
        {"zip":75230,"store":"CVS Preston","med":"metformin","price":8,"lat":32.864,"lon":-96.807},
        {"zip":75201,"store":"CVS Downtown","med":"semaglutide (Ozempic)","price":702,"lat":32.779,"lon":-96.799},
        {"zip":75205,"store":"CVS Knox","med":"semaglutide (Ozempic)","price":709,"lat":32.821,"lon":-96.788},
        {"zip":75230,"store":"CVS Preston","med":"semaglutide (Ozempic)","price":719,"lat":32.864,"lon":-96.807},
    ])

df_prices = cvs_data()
maps_key = st.secrets.get("GOOGLE_STATIC_KEY", "YOUR_KEY")

# ---------- Tabs ----------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["📈 Glucose", "💰 Prices", "🗺️ CVS Maps", "💊 Meds", "🆘 Emergency", "📚 Evidence"])

# ---------- Glucose Tab ----------
with tab1:
    with card():
        st.header("📈 Glucose Trend")
        sample = "timestamp,glucose\n2025-05-15 08:00,58\n2025-05-15 08:30,92"
        st.download_button("Sample CSV", sample, "sample.csv", "text/csv")
        if "df" not in st.session_state: st.session_state.df=None
        up = st.file_uploader("Upload CGM / Glucometer CSV", type="csv")
        if up:
            df = pd.read_csv(up)
            df['timestamp']=pd.to_datetime(df['timestamp'], errors='coerce')
            df=df.dropna().sort_values('timestamp')
            st.session_state.df = df
        if st.session_state.df is not None:
            df=st.session_state.df
            st.line_chart(df.set_index('timestamp')['glucose'])
            latest=df.iloc[-1]['glucose']
            if latest < 70:
                st.error("⚠️ Hypoglycemia detected (<70 mg/dL)")
            elif latest > 250:
                st.warning("High BG – consider correction")
            else:
                st.success("BG in acceptable range")

# ---------- Price Tab ----------
with tab2:
    with card():
        st.header("💰 Dallas CVS Price Finder")
        meds = df_prices['med'].unique().tolist()
        with st.form("price"):
            med=st.selectbox("Select Medication", meds)
            submit=st.form_submit_button("Find Cheapest")
        if submit:
            if not user_zip.isnumeric(): st.error("ZIP numeric")
            else:
                z=int(user_zip)
                med_df=df_prices[df_prices['med']==med]
                local=med_df[med_df['zip']==z]
                res=local if not local.empty else med_df
                res=res.sort_values('price')
                st.table(res[['store','price']])
                st.success(f"Best: {res.iloc[0]['store']} – ${res.iloc[0]['price']}")

# ---------- Maps Tab ----------
with tab3:
    with card():
        st.header("🗺️ Dallas CVS Static Maps")
        if maps_key=="YOUR_KEY":
            st.warning("Add GOOGLE_STATIC_KEY to Secrets to view maps.")
        for _,r in df_prices[['store','lat','lon']].drop_duplicates().iterrows():
            url=("https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom=15&size=600x300&markers=color:red%7C{lat},{lon}&key={key}"
                 .format(lat=r.lat,lon=r.lon,key=maps_key))
            st.image(url, caption=r.store)

# ---------- Meds Tab ----------
with tab4:
    with card():
        st.header("Comprehensive Medication Guide")
        meds_df=pd.DataFrame({
            "Class":["Biguanide","SGLT2 inhibitor","GLP‑1 agonist","Sulfonylurea","DPP‑4 inhibitor","TZD","Basal insulin","Rapid insulin"],
            "Example":["Metformin","Empagliflozin","Semaglutide","Glipizide","Sitagliptin","Pioglitazone","Glargine","Lispro"],
            "Route":["Oral"]*6+["Injection","Injection"],
            "Notes":[
                "First‑line, weight neutral",
                "CV + renal benefit",
                "Weight loss, weekly injection",
                "Risk of hypoglycemia",
                "Weight neutral, modest A1c drop",
                "Weight gain risk",
                "24‑hr coverage",
                "Mealtime coverage"
            ]
        })
        st.dataframe(meds_df, use_container_width=True)

# ---------- Emergency Tab ----------
with tab5:
    with card():
        st.header("🆘 Emergency Playbook")
        cols=st.columns(2)
        with cols[0]:
            st.subheader("Hypoglycemia (<70 mg/dL)")
            st.markdown("""- 15 g fast carbs (4 oz juice)<br>- Re‑check in 15 min<br>- Repeat once if needed<br>- Call 911 if unconscious""", unsafe_allow_html=True)
        with cols[1]:
            st.subheader("Hyperglycemia (>300 mg/dL)")
            st.markdown("""- Check ketones<br>- If positive or vomiting → ER<br>- Correction insulin per plan<br>- Hydrate (water every hr)""", unsafe_allow_html=True)
        st.divider()
        st.subheader("Sick‑Day Rules")
        st.markdown("Never stop basal insulin. Check BG q2‑4h, drink fluids, monitor ketones.")
        st.info("☎️ Emergency contacts: 911 for severe symptoms, endocrinologist on‑call: 555‑123‑4567")

# ---------- Evidence Tab ----------
with tab6:
    with card():
        st.header("NEJM Evidence Feed")
        evid=[
            ("Automated Insulin Delivery Trial 2025","Hybrid closed‑loop pumps improved Time‑in‑Range by 15 pp."),
            ("Weekly Basal Insulin (Efsitora) 2024","Once‑weekly basal insulin non‑inferior to daily degludec."),
            ("Intensive SBP Target 2024","SBP <120 mm Hg reduced CV events in T2D without renal harm.")
        ]
        for t,b in evid:
            with st.expander(t): st.write(b)

st.caption("© 2025 – META Summit demo. Maps require Google Static Maps API key in Secrets.")
