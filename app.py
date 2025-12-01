# app.py – Summerlands met PERFECT werkende Categorie-tab
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

# === Session state voor tab-selecties ===
if "cat_selection" not in st.session_state:
    st.session_state.cat_selection = ALL_TARTANS[0]

if "all_selection" not in st.session_state:
    st.session_state.all_selection = ALL_TARTANS[0]

# === UI ===
st.set_page_config(page_title="Summerlands – Categorieën", layout="centered")
st.title("Summerlands – Kies per categorie")

tab1, tab2 = st.tabs(["Categorieën", "Alle tartans"])

# === TAB 1: Categorieën ===
with tab1:
    selected_cat = st.selectbox("Categorie", ["Alle"] + list(CATEGORIES.keys()), key="cat_select")
    
    if selected_cat == "Alle":
        options = ALL_TARTANS
    else:
        options = [t for t in ALL_TARTANS if tartan_to_category.get(t) == selected_cat]
        st.info(f"{len(options)} tartans in deze categorie")
    
    selected = st.selectbox(
        "Tartan",
        options=options,
        index=0,
        key="cat_tartan_select",
        on_change=lambda: st.session_state.update(cat_selection=st.session_state.cat_tartan_select)
    )
    st.session_state.cat_selection = selected

# === TAB 2: Alle tartans ===
with tab2:
    selected = st.selectbox(
        "Zoek alle tartans",
        options=[""] + ALL_TARTANS,
        format_func=lambda x: "– Kies een tartan –" if not x else x,
        key="all_tartan_select"
    )
    if selected:
        st.session_state.all_selection = selected

# === Gebruik juiste selectie ===
final_selection = st.session_state.cat_selection if 'cat_selection' in st.session_state else st.session_state.all_selection
final_selection = final_selection or ALL_TARTANS[0]

tc = TARTANS.get(final_selection, TARTANS["Royal Stewart"])
category = tartan_to_category.get(final_selection, "Ongecategoriseerd")

st.subheader(final_selection)
st.caption(f"Categorie: **{category}** | Threadcount: `{tc}`")

scale = st.slider("Schaal", 1, 100, 1, key="scale")

# === Rendering functies (jouw bestaande) ===
def parse_threadcount(tc): ...  # jouw functie
def build_sett(pattern): ...    
