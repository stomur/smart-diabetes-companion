
"""
Smart Diabetes Companion – Final Demo
Features:
  • Glucose tracker
  • Dallas CVS price finder
  • Static Google Maps thumbnails (Static Maps API)
  • Insulin options table
  • NEJM highlights
Set GOOGLE_STATIC_KEY in Streamlit Secrets.
"""

import streamlit as st
import pandas as pd
from contextlib import contextmanager

# ---------- Config & Styles ----------
st.set_page_config(page_title="Smart Diabetes Companion", page_icon="💉", layout="centered")

BG_URL = "https://images.unsplash.com/photo-1580281657441-8236aa7f2930?auto=format&fit=crop&w=1950&q=80"

css = """<style>
html, body, .stApp {{
  background-image: url('{bg}');
  background-size: cover;
  background-attachment: fixed;
}}
.card {{
  background: rgba(255, 255, 255, 0.9);
  padding: 2rem;
  border-radius: 1.25rem;
  box-shadow: 0 6px 16px rgba(0,0,0,0.1);
}}
</style>""".format(bg=BG_URL)
st.markdown(css, unsafe_allow_html=True)

@contextmanager
def card():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    yield
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Header ----------
with card():
    st.image("https://images.unsplash.com/photo-1526256262350-7da7584cf5eb?auto=format&fit=crop&w=200&q=60", width=70)
    st.title("Smart Diabetes Companion")
    st.caption("Glucose • CVS pricing • Maps • Insulin guide • NEJM evidence")

# ---------- Sidebar ----------
st.sidebar.header("Targets")
target = st.sidebar.number_input("Target BG", 120, step=5)
isf    = st.sidebar.number_input("ISF (mg/dL per unit)", 50)
user_zip = st.sidebar.text_input("ZIP (Dallas)", "75201")

# ---------- Data ----------
def cvs_data():
    return pd.DataFrame([
        {"zip":75201,"store":"CVS – Downtown","med":"insulin glargine (Lantus)","price":92,"lat":32.7791,"lon":-96.7989},
        {"zip":75205,"store":"CVS – Knox","med":"insulin glargine (Lantus)","price":95,"lat":32.8212,"lon":-96.7879},
        {"zip":75230,"store":"CVS – Preston","med":"insulin glargine (Lantus)","price":98,"lat":32.8637,"lon":-96.8070},
        {"zip":75201,"store":"CVS – Downtown","med":"metformin","price":6,"lat":32.7791,"lon":-96.7989},
        {"zip":75205,"store":"CVS – Knox","med":"metformin","price":7,"lat":32.8212,"lon":-96.7879},
        {"zip":75230,"store":"CVS – Preston","med":"metformin","price":8,"lat":32.8637,"lon":-96.8070},
    ])

df_prices = cvs_data()
maps_key  = st.secrets.get("GOOGLE_STATIC_KEY", "YOUR_API_KEY")

# ---------- Tabs ----------
tab_g, tab_p, tab_m, tab_i, tab_n = st.tabs(
    ["📈 Glucose", "💊 CVS Prices", "📍 CVS Maps", "🩺 Insulin Guide", "📚 NEJM"])

# ---------- Glucose tab ----------
with tab_g:
    with card():
        st.header("CGM / Glucometer CSV")
        sample = "timestamp,glucose\n2025-05-15 08:00,58\n2025-05-15 08:30,92"
        st.download_button("Sample CSV", sample, file_name="sample.csv", mime="text/csv")
        file = st.file_uploader("Upload CSV", type="csv")
        if file:
            df = pd.read_csv(file)
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
            df = df.dropna().sort_values('timestamp')
            st.line_chart(df.set_index('timestamp')['glucose'])

# ---------- CVS Prices tab ----------
with tab_p:
    with card():
        st.header("Find Cheapest CVS")
        med = st.selectbox("Medication", df_prices['med'].unique())
        if st.button("Search"):
            if not user_zip.isnumeric():
                st.error("ZIP must be numeric")
            else:
                z = int(user_zip)
                sub = df_prices[df_prices['med']==med]
                local = sub[sub['zip']==z]
                res = local if not local.empty else sub
                res = res.sort_values('price')
                st.table(res[['store','price']])
                st.success(f"Cheapest: {res.iloc[0]['store']} – ${res.iloc[0]['price']}")

# ---------- Maps tab ----------
with tab_m:
    with card():
        st.header("Dallas CVS Locations")
        if maps_key == "YOUR_API_KEY":
            st.warning("Add GOOGLE_STATIC_KEY to Secrets for map images.")
        for _,row in df_prices[['store','lat','lon']].drop_duplicates().iterrows():
            url = ("https://maps.googleapis.com/maps/api/staticmap"
                   f"?center={row.lat},{row.lon}&zoom=15&size=600x300"
                   f"&markers=color:red%7C{row.lat},{row.lon}&key={maps_key}")
            st.image(url, caption=row['store'])

# ---------- Insulin guide ----------
with tab_i:
    with card():
        st.header("Insulin Categories & Examples")
        data = {
            "Category":["Long‑acting","Rapid‑acting","Ultra‑rapid"],
            "Brand":["Lantus (glargine)","Humalog (lispro)","Fiasp (aspart)"],
            "Onset":["1‑2 h","15 min","5 min"],
            "Duration":["24 h","4‑6 h","3‑4 h"]
        }
        st.table(pd.DataFrame(data))

# ---------- NEJM tab ----------
with tab_n:
    with card():
        st.header("NEJM Highlights")
        for title, blurb in [
            ("Automated Insulin Delivery 2025","Closed‑loop pumps ↑ Time‑in‑Range by 15 pp."),
            ("Weekly Basal Insulin 2024","Once‑weekly efsitora matched daily degludec.")
        ]:
            with st.expander(title):
                st.write(blurb)

st.caption("© 2025 – Demo app. Static Maps images require Google API key.")
