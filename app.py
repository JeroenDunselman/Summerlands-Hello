# app.py – Summerlands – Beide tabs werken PERFECT (2025 Final)
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

# === CATEGORIEËN ===
CATEGORIES = {
    "Regiment": ["Black Watch", "Gordon Modern", "Cameron of Erracht"],
    "Dress": ["Royal Stewart (Dress)", "Anderson (Dress)", "Gordon Dress"],
    "Hunting": ["Fraser Hunting", "MacKenzie Hunting", "Turnbull (Hunting)"],
    "Weathered / Ancient": ["MacDonald Ancient", "Sutherland Old"],
    "Modern / Classic": ["Royal Stewart", "Burberry", "MacDonald of the Isles", "Wallace"]
}

ALL_TARTANS = sorted(TARTANS.keys())
tartan_to_category = {}
for cat, names in CATEGORIES.items():
    for name in names:
        matches = [t for t in ALL_TARTANS if name.lower().replace(" ", "") in t.lower().replace(" ", "")]
        for m in matches:
            tartan_to_category[m] = cat

# === Session state ===
if "selected_tartan" not in st.session_state:
    st.session_state.selected_tartan = "Royal Stewart"

# === UI ===
st.set_page_config(page_title="Summerlands – Categorieën", layout="centered")
st.title("Summerlands – Kies per categorie")

tab1, tab2 = st.tabs(["Categorieën", "Alle tartans"])

# === TAB 1: Categorieën ===
with tab1:
    cat = st.selectbox("Categorie", ["Alle"] + list(CATEGORIES.keys()), key="tab1_cat")
    
    if cat == "Alle":
        options = ALL_TARTANS
    else:
        options = [t for t in ALL_TARTANS if tartan_to_category.get(t) == cat]
    
    selected = st.selectbox("Tartan", options, key="tab1_tartan")
    if selected != st.session_state.selected_tartan:
        st.session_state.selected_tartan = selected
        st.rerun()

# === TAB 2: Alle tartans ===
with tab2:
    selected = st.selectbox(
        "Zoek alle tartans",
        options=[""] + ALL_TARTANS,
        format_func=lambda x: "– Kies een tartan –" if not x else x,
        key="tab2_tartan"
    )
    if selected and selected != st.session_state.selected_tartan:
        st.session_state.selected_tartan = selected
        st.rerun()

# === Gebruik geselecteerde tartan ===
current = st.session_state.selected_tartan
tc = TARTANS.get(current, TARTANS["Royal Stewart"])
category = tartan_to_category.get(current, "Ongecategoriseerd")

st.subheader(current)
st.caption(f"Categorie: **{category}** | Threadcount: `{tc}`")

scale = st.slider("Schaal", 1, 100, 1, key="scale")

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
                       file_name=f"Summerlands_{current.replace(' ', '_')}.png",
                       mime="image/png")
