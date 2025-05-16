import streamlit as st
import pandas as pd
from contextlib import contextmanager

# Force light theme and white background
st.set_page_config(page_title="Smart Diabetes Companion", layout="centered")

st.markdown("""
<style>
/* Force white background */
html, body, .stApp {
    background-color: #ffffff !important;
}
.block {
    background: #ffffff;
    padding: 2rem;
    border-radius: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

@contextmanager
def block():
    st.markdown('<div class="block">', unsafe_allow_html=True)
    yield
    st.markdown('</div>', unsafe_allow_html=True)

with block():
    st.title("Smart Diabetes Companion – White Theme Demo")
    st.write("Clean white background enforced via CSS.")

st.write("Upload glucose CSV etc. (omitted for brevity)")