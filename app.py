# app.py – Summerlands met << Vorige / Volgende >> op "Alle tartans"
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import json

# === Laad data ===
@st.cache_data
def load_data():
    with open("colors.json") as f:
        colors = json.load(f)
    with open("tartans.json") as f:
        tartans = json.load(f)
    return colors, tartans

COLORS, TARTANS = load_data()
ALL_TARTANS = sorted(TARTANS.keys())
TOTAL = len(ALL_TARTANS)

# === Session state ===
if "index" not in st.session_state:
    st.session_state.index = 0

# === UI ===
st.set_page_config(page_title="Summerlands – Scroll", layout="centered")
st.title("Summerlands – Scroll door 531 tartans")

tab1, tab2 = st.tabs(["Categorieën", "Alle tartans"])

# === TAB 1: Categorieën (blijft zoals voorheen) ===
with tab1:
    cat = st.selectbox("Categorie", ["Alle"] + list(CATEGORIES.keys()), key="cat")
    if cat == "Alle":
        options = ALL_TARTANS
    else:
        options = [t for t in ALL_TARTANS if tartan_to_category.get(t) == cat]
    selected = st.selectbox("Tartan", options, key="cat_tartan")
    current_name = selected

# === TAB 2: Alle tartans met << >> knoppen ===
with tab2:
    col_prev, col_info, col_next = st.columns([1, 3, 1])
    
    with col_prev:
        if st.button("<< Vorige", use_container_width=True):
            st.session_state.index = (st.session_state.index - 1) % TOTAL
            st.rerun()
    
    with col_next:
        if st.button("Volgende >>", use_container_width=True):
            st.session_state.index = (st.session_state.index + 1) % TOTAL
            st.rerun()
    
    with col_info:
        current_name = ALL_TARTANS[st.session_state.index]
        st.subheader(f"{st.session_state.index + 1} / {TOTAL}")
        st.write(f"**{current_name}**")
        st.code(TARTANS[current_name])

# === Gebruik geselecteerde tartan (van beide tabs) ===
final_name = current_name if 'current_name' in locals() else ALL_TARTANS[st.session_state.index]
tc = TARTANS[final_name]
category = tartan_to_category.get(final_name, "Ongecategoriseerd")

st.caption(f"Categorie: **{category}** | Threadcount: `{tc}`")

scale = st.slider("Schaal", 1, 100, 1)

# === Rendering ===
def parse_threadcount(tc): ...  # jouw functie
def build_sett(pattern): ...     # jouw functie
def create_tartan(pattern, size=900, scale=1): ...  # jouw functie

pattern = parse_threadcount(tc)
if pattern:
    img = create_tartan(pattern, size=900, scale=scale)
    st.image(img, use_column_width=True)
    buf = BytesIO()
    plt.imsave(buf, img, format="png")
    buf.seek(0)
    st.download_button("Download", buf,
                       file_name=f"Summerlands_{final_name.replace(' ', '_')}.png",
                       mime="image/png")
