import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
import io

st.set_page_config(page_title="Smart Diabetes Companion", page_icon="💉", layout="centered")

st.title("💉 Smart Diabetes Companion – Savings & Glucose Coach")
st.caption("Instant insights for healthier care *and* cheaper meds.")

glu_tab, med_tab = st.tabs(["📈 Glucose Tracker", "💊 Medication Price Explorer"])

with glu_tab:
    st.header("📈 Upload CGM or Glucometer CSV")
    st.markdown("**Columns required:** `timestamp` (YYYY-MM-DD HH:MM) & `glucose` (mg/dL). Example: `2025-05-15 08:00,132`.")
    up = st.file_uploader("Upload readings", type="csv")
    if up is not None:
        try:
            df = pd.read_csv(up)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            avg = df['glucose'].mean()
            latest = df.iloc[-1]
            delta = latest['glucose'] - df['glucose'].iloc[-2] if len(df) > 1 else 0
            col1, col2 = st.columns(2)
            col1.metric("Average", f"{avg:.1f} mg/dL")
            col2.metric("Latest", f"{int(latest['glucose'])} mg/dL", delta=int(delta))
            st.line_chart(df.set_index('timestamp')['glucose'])
            if avg > 180:
                st.warning("Average above ADA target – consider management change.")
            elif avg < 70:
                st.warning("Risk of hypoglycemia – please consult provider.")
            else:
                st.success("Average appears on-target – keep it up!")
        except Exception as e:
            st.error(f"Error parsing CSV: {e}")

with med_tab:
    st.header("💊 Compare Cash Prices – Multiple Drugs")
    st.markdown("Mock dataset below simulates GoodRx or CostPlus feeds. Select one **or more** meds.")
    CSV = """zip,pharmacy,med,price
75201,CostPlus Pharmacy,insulin glargine (Lantus),92
75201,Walmart,insulin glargine (Lantus),108
75201,Walgreens,insulin glargine (Lantus),127
75201,CostPlus Pharmacy,metformin,6
75201,Walmart,metformin,8
75201,CVS,metformin,12
75201,CostPlus Pharmacy,semaglutide (Ozempic),682
75201,Walgreens,semaglutide (Ozempic),799
75201,Costco,semaglutide (Ozempic),709
"""
    base_df = pd.read_csv(io.StringIO(CSV))
    user_zip = st.text_input("ZIP code", value="75201")
    meds = base_df['med'].unique().tolist()
    chosen = st.multiselect("Select medication(s)", meds, default=[meds[0]])
    if st.button("Search Prices", use_container_width=True):
        try:
            z = int(user_zip)
        except ValueError:
            st.error("ZIP must be numeric")
            st.stop()
        results = []
        for med in chosen:
            sub = base_df[(base_df['zip'] == z) & (base_df['med'] == med)]
            if sub.empty:
                sub = base_df[base_df['med'] == med]
            sub = sub.sort_values('price')
            best = sub.iloc[0]
            worst = sub.iloc[-1]
            savings = worst['price'] - best['price']
            results.append({
                'Medication': med,
                'Best Pharmacy': best['pharmacy'],
                'Best Price ($)': best['price'],
                'Worst Price ($)': worst['price'],
                'Potential Savings ($)': savings
            })
        res_df = pd.DataFrame(results).sort_values('Potential Savings ($)', ascending=False)
        st.table(res_df.set_index('Medication'))
        total_save = res_df['Potential Savings ($)'].sum()
        if total_save > 0:
            st.success(f"💰 Total savings if you shop smart: **${total_save:.2f} / fill**")
        else:
            st.info("Prices fairly consistent across pharmacies for selected meds.")

st.divider()
st.caption("© 2025 - Smart Diabetes Companion (demo). Data & suggestions are illustrative only.")