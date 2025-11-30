# app.py – Summerlands met << Vorige / Volgende >> navigatie
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

# Sorteer voor consistente volgorde
TARTAN_LIST = sorted(TARTANS.keys())
TOTAL = len(TARTAN_LIST)

# === Sessie-state voor huidige positie ===
if "index" not in st.session_state:
    st.session_state.index = 0

def parse_threadcount(tc: str):
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

# === UI ===
st.set_page_config(page_title="Summerlands – 531 Tartans", layout="centered")
st.title("Summerlands – Scroll door 531 tartans")

# Navigatiebalk
col_prev, col_info, col_next = st.columns([1, 3, 1])

with col_prev:
    if st.button("<< Vorige", use_container_width=True):
        st.session_state.index = (st.session_state.index - 1) % TOTAL
        st.rerun()

with col_next:
    if st.button("Volgende >>", use_container_width=True):
        st.session_state.index = (st.session_state.index + 1) % TOTAL
        st.rerun()

# Huidige tartan
current_name = TARTAN_LIST[st.session_state.index]
current_tc = TARTANS[current_name]

with col_info:
    st.subheader(f"{st.session_state.index + 1} / {TOTAL}")
    st.write(f"**{current_name}**")
    st.code(current_tc)

col_scale = st.columns([3, 1])[1]
with col_scale:
    scale = st.slider("Schaal", 1, 100, 1)

# Render tartan
pattern = parse_threadcount(current_tc)
if pattern:
    img = create_tartan(pattern, size=900, scale=scale)
    st.image(img, use_column_width=True)

    buf = BytesIO()
    plt.imsave(buf, img, format="png")
    buf.seek(0)
    st.download_button(
        "Download",
        buf,
        file_name=f"Summerlands_{current_name.replace(' ', '_')}.png",
        mime="image/png"
    )

st.caption("Gebruik ← → of knoppen om te bladeren – 531 tartans, eindeloos plezier.")
