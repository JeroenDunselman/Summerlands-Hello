# app.py – Summerlands met Categorieën (Dress / Hunting / Modern / Weathered / Regiment)
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

# === CATEGORIEËN (handmatig samengesteld uit jouw 531 tartans) ===
CATEGORIES = {
    "Regiment": [
        "Black Watch", "Gordon Modern", "Cameron of Erracht", "Seaforth Highlanders",
        "Argyll & Sutherland", "Scots Guards", "Royal Scots", "Queen's Own Highlanders"
    ],
    "Dress": [
        "Royal Stewart (Dress)", "Stewart Dress", "Anderson (Dress)", "MacLeod Dress",
        "Fraser Dress", "Gordon Dress", "MacKenzie Dress", "Dress Gordon"
    ],
    "Hunting": [
        "Fraser Hunting", "MacKenzie Hunting", "MacRae Hunting", "MacKay Hunting",
        "Turnbull (Hunting)", "Ferguson Hunting", "Grant Hunting", "MacPherson Hunting"
    ],
    "Weathered / Ancient": [
        "MacDonald Ancient", "MacLeod of Harris (Weathered)", "Anderson Weathered",
        "MacKinnon Weathered", "MacLeod of Lewis (Weathered)", "Sutherland Old"
    ],
    "Modern / Classic": [
        "Royal Stewart", "Burberry", "Black Watch", "Gordon Modern", "MacDonald of the Isles",
        "MacLeod of Harris", "Wallace", "Robertson", "Campbell of Argyll"
    ]
}

# Maak een platte lijst + categorie-toewijzing
ALL_TARTANS = sorted(TARTANS.keys())
tartan_to_category = {}
for cat, names in CATEGORIES.items():
    for name in names:
        # Fuzzy matching voor varianten
        matches = [t for t in ALL_TARTANS if name.lower().replace(" ", "").replace("&", "") in t.lower().replace(" ", "")]
        for m in matches:
            tartan_to_category[m] = cat

# === UI ===
st.set_page_config(page_title="Summerlands – Categorieën", layout="centered")
st.title("Summerlands – Kies per categorie")

tab1, tab2 = st.tabs(["Categorieën", "Alle tartans"])

with tab1:
    selected_cat = st.selectbox("Kies een categorie", ["Alle"] + list(CATEGORIES.keys()))
    
    if selected_cat == "Alle":
        options = ALL_TARTANS
    else:
        options = [t for t in ALL_TARTANS if tartan_to_category.get(t) == selected_cat]
        st.info(f"{len(options)} tartans in deze categorie")

    selected = st.selectbox("Kies een tartan", options, key="cat_select")

with tab2:
    selected = st.selectbox("Zoek alle tartans", [""] + ALL_TARTANS, format_func=lambda x: "– Kies –" if not x else x)

# Gebruik geselecteerde tartan
if not selected:
    selected = "Royal Stewart"

tc = TARTANS.get(selected, TARTANS["Royal Stewart"])
category = tartan_to_category.get(selected, "Ongecategoriseerd")

st.subheader(f"{selected}")
st.caption(f"Categorie: **{category}** | Threadcount: `{tc}`")

col1, col2 = st.columns([3, 1])
with col2:
    scale =  st.slider("Schaal", 1, 100, 1)

# Render
def parse_threadcount(tc): ...  # (jouw bestaande functie)
def build_sett(pattern): ...     # (jouw bestaande functie)
def create_tartan(pattern, size=900, scale=1): ...  # (jouw bestaande functie)

pattern = parse_threadcount(tc)
if pattern:
    img = create_tartan(pattern, size=900, scale=scale)
    st.image(img, use_column_width=True)
    buf = BytesIO()
    plt.imsave(buf, img, format="png")
    buf.seek(0)
    st.download_button("Download", buf,
                       file_name=f"Summerlands_{selected.replace(' ', '_')}.png",
                       mime="image/png")
