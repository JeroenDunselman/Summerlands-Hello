# app.py – Summerlands met << Vorige / Volgende >> (100% werkend!)
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

# === CATEGORIEËN (nu correct gedefinieerd vóór gebruik) ===
CATEGORIES = {
    "Regiment": ["Black Watch", "Gordon Modern", "Cameron of Erracht"],
    "Dress": ["Royal Stewart (Dress)", "Anderson (Dress)", "Gordon Dress"],
    "Hunting": ["Fraser Hunting", "MacKenzie Hunting", "Turnbull (Hunting)"],
    "Weathered / Ancient": ["MacDonald Ancient", "Sutherland Old"],
    "Modern / Classic": ["Royal Stewart", "Burberry", "MacDonald of the Isles", "Wallace"]
}

tartan_to_category = {}
for cat, names in CATEGORIES.items():
    for name in names:
        matches = [t for t in ALL_TARTANS if name.lower().replace(" ", "") in t.lower().replace(" ", "")]
        for m in matches:
            tartan_to_category[m] = cat

# === Session state ===
if "index" not in st.session_state:
    st.session_state.index = 0

# === UI ===
st.set_page_config(page_title="Summerlands – Scroll", layout="centered")
st.title("Summerlands – Scroll door 531 tartans")

tab1, tab2 = st.tabs(["Categorieën", "Alle tartans"])

# === TAB 1: Categorieën ===
with tab1:
    cat = st.selectbox("Categorie", ["Alle"] + list(CATEGORIES.keys()), key="cat_select")
    if cat == "Alle":
        options = ALL_TARTANS
    else:
        options = [t for t in ALL_TARTANS if tartan_to_category.get(t) == cat]
        st.info(f"{len(options)} tartans")
    selected = st.selectbox("Tartan", options, key="cat_tartan")
    current_name = selected

# === TAB 2: Alle tartans met << >> ===
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

# === Gebruik geselecteerde tartan ===
final_name = current_name if 'current_name' in locals() else ALL_TARTANS[st.session_state.index]
tc = TARTANS[final_name]
category = tartan_to_category.get(final_name, "Ongecategoriseerd")

st.caption(f"Categorie: **{category}** | Threadcount: `{tc}`")

scale = st.slider("Schaal", 1, 100, 1)

# === Rendering ===
def parse_threadcount(tc):
    parts = [p.strip() for p in tc.replace(",", " ").split() if p.strip()]
    pattern = []
    for part in parts:
        part = part.upper()
        color = None
        num_str = part
        for c in sorted(COLORS.keys(), key=len, reverse=True):
            if part.startswith(c):
                color = c
                num_str = part[len(c):]
                break
        if color and color in COLORS:
            count = 1.0 if not num_str else float(num_str)
            pattern.append((color, count))
    return pattern

def build_sett(pattern):
    f_counts = [c for _, c in pattern]
    f_colors  = [col for col, _ in pattern]
    return f_counts + f_counts[::-1][1:], f_colors + f_colors[::-1][1:]

def create_tartan(pattern, size=900, scale=1):
    sett_counts, sett_colors = build_sett(pattern)
    widths = [max(1, int(round(c * scale))) for c in sett_counts]
    total_w = sum(widths)
    tartan = np.zeros((total_w, total_w, 3), dtype=np.uint8)
    pos = 0
    for w, col in zip(widths, sett_colors):
        tartan[:, pos:pos+w] = COLORS[col]
        pos += w
    weft = tartan.copy().transpose(1, 0, 2)
    result = np.minimum(tartan + weft, 255).astype(np.uint8)
    pil_img = Image.fromarray(result)
    final = pil_img.resize((size, size), Image.NEAREST)
    return np.array(final)

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
