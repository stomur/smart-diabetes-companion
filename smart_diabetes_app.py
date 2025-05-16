import streamlit as st
import pandas as pd
from contextlib import contextmanager

# Restore original light-on-photo aesthetic
st.set_page_config(page_title="Smart Diabetes Companion", layout="centered")

BACKGROUND_URL = "https://images.unsplash.com/photo-1580281657441-8236aa7f2930?auto=format&fit=crop&w=1950&q=80"

st.markdown(f"""
<style>
html, body, .stApp {{
    background-image: url('{BACKGROUND_URL}');
    background-size: cover;
    background-attachment: fixed;
}}
.card {{
    background: rgba(255,255,255,0.85);
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

with card():
    st.title("Smart Diabetes Companion")
    st.caption("Re‑enabled background photo with translucent cards.")

st.write("Full app code goes here (same as previous bug‑free build).")