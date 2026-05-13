import streamlit as st
import base64, os, json
from datetime import datetime as dt

st.set_page_config(page_title="SORGENTE YOGA", layout="wide", page_icon="🧘")

def get_img(p):
    if os.path.exists(p):
        try:
            with open(p, "rb") as f: return base64.b64encode(f.read()).decode()
        except: return ""
    return ""

def load_a():
    if os.path.exists("archivio_articoli.json"):
        try:
            with open("archivio_articoli.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except: return []
    return []

all_a = load_a()
ih = get_img("header_yoga.png")

# --- CSS DEFINITIVO: COLPISCE DIRETTAMENTE I CONTENITORI DI STREAMLIT ---
st.markdown(f"""
<style>
    /* Rimuove lo spazio bianco in cima alla pagina forzatamente */
    .stApp {{
        background-color: #FDFCF0 !important;
    }}
    
    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0) !important;
        height: 0px !important;
    }}

    .block-container {{
        padding-top: 0px !important;
        max-width: 100% !important;
        margin: 0px !important;
    }}

    /* L'immagine diventa un blocco che occupa la cima senza margini */
    .hero-section {{
        width: 100vw;
        height: 400px;
        background-image: url('data:image/png;base64,{ih}');
        background-size: cover;
        background-position: center;
        margin: 0px !important;
        padding: 0px !important;
    }}

    .header-bar {{
        background-color: #1A2E44 !important;
        color: #FDFCF0 !important;
        text-align: center;
        padding: 25px 0;
        font-family: serif;
        font-size: 2.2rem;
        letter-spacing: 5px;
        border-bottom: 5px solid #C5A059;
        margin-bottom: 30px;
    }}

    .main-body {{
        padding: 0 10%;
    }}
    
    .art-box {{ 
        background: white; padding:40px; border-radius:8px; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); color:#1A2E44; 
    }}
</style>
""", unsafe_allow_html=True)

# Layout: Hero Image -> Barra Blu -> Contenuti
st.markdown('<div class="hero-section"></div>', unsafe_allow_html=True)
st.markdown('<div class="header-bar">SORGENTE YOGA</div>', unsafe_allow_html=True)

st.markdown('<div class="main-body">', unsafe_allow_html=True)

if 'sel_idx' not in st.session_state: st.session_state['sel_idx'] = 0 if all_a else None
if 'mode' not in st.session_state: st.session_state['mode'] = 'view'

# Menu
c1, c2, c3 = st.columns(3)
with c1:
    with st.popover("📂 ARCHIVIO", use_container_width=True):
        for i, a in enumerate(all_a):
            if str(a.get('cat','')).upper() in ['BLOG', '']:
                if st.button(a['titolo'], key=f"ar_{i}", use_container_width=True):
                    st.session_state.update({"sel_idx": i, "mode": "view"}); st.rerun()
with c2:
    with st.popover("📜 TESTI ANTICHI", use_container_width=True):
        for i, a in enumerate(all_a):
            if str(a.get('cat','')).upper() == 'TESTI':
                if st.button(a['titolo'], key=f"te_{i}", use_container_width=True):
                    st.session_state.update({"sel_idx": i, "mode": "view"}); st.rerun()
with c3:
    with st.popover("🔬 SCIENZA", use_container_width=True):
        for i, a in enumerate(all_a):
            if str(a.get('cat','')).upper() == 'SCIENZA':
                if st.button(a['titolo'], key=f"sc_{i}", use_container_width=True):
                    st.session_state.update({"sel_idx": i, "mode": "view"}); st.rerun()

st.write("---")

# Visualizzazione
s_idx = st.session_state['sel_idx']
if st.session_state.mode == "view" and s_idx is not None:
    art = all_a[s_idx]
    st.markdown(f"""<div class="art-box">
        <h1 style="font-family:serif; color:#1A2E44; margin-top:0;">{art['titolo']}</h1>
        <div style="font-size:1.2rem; line-height:1.7; font-family:serif;">
            {art['testo'].replace(chr(10), '<br>')}
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
