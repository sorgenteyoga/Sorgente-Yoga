import streamlit as st
import base64, os, json, requests
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

# --- CSS DEFINITIVO PER COPIARE "COME DOVREBBE.JPG" ---
st.markdown(f"""
<style>
    /* 1. ELIMINA LO SPAZIO BIANCO IN ALTO (HEADER DI SISTEMA) */
    [data-testid="stHeader"] {{
        display: none !important;
    }}
    
    /* 2. AZZERA MARGINI E PADDING DEL CONTENITORE PRINCIPALE */
    .block-container {{
        padding: 0px !important;
        margin: 0px !important;
        max-width: 100% !important;
    }}

    /* 3. FORZA L'APP A PARTIRE DA ZERO */
    .stApp {{
        margin-top: -60px !important;
    }}

    /* 4. IMMAGINE HEADER: GRANDE, FULL-WIDTH E SENZA SPAZI */
    .header-img {{ 
        width: 100vw; 
        height: 380px; 
        background: url('data:image/png;base64,{ih}') no-repeat center; 
        background-size: cover; 
        margin: 0px !important;
        padding: 0px !important;
        display: block;
    }}
    
    /* 5. BARRA BLU: INCOLLATA ALL'IMMAGINE */
    .header-bar {{ 
        background:#1A2E44 !important; 
        padding:25px 10px; 
        color:#FDFCF0 !important; 
        font-family: serif; 
        text-align:center; 
        font-size:2.2rem; 
        letter-spacing:5px; 
        margin-top: -2px !important; /* Salda l'immagine alla barra */
        border-bottom: 5px solid #C5A059;
        text-transform: uppercase;
    }}

    /* 6. CORPO DEL SITO: SPAZIATURA ELEGANTE PER TESTO E TASTI */
    .main-wrapper {{
        padding: 40px 8%;
        background-color: #FDFCF0;
    }}

    /* 7. SCATOLA ARTICOLO */
    .art-box {{ 
        background: white; padding:40px; border-radius:8px; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.08); color:#1A2E44; 
    }}
</style>

<div class="header-img"></div>
<div class="header-bar">SORGENTE YOGA</div>
""", unsafe_allow_html=True)

# Inizio area contenuti
st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)

if 'sel_idx' not in st.session_state: st.session_state['sel_idx'] = 0 if all_a else None
if 'mode' not in st.session_state: st.session_state['mode'] = 'view'

# Navigazione a 3 colonne come nel tuo schizzo
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

# Visualizzazione Contenuto
s_idx = st.session_state['sel_idx']
if st.session_state.mode == "view" and s_idx is not None:
    art = all_a[s_idx]
    st.markdown(f"""<div class="art-box">
        <h1 style="font-family:serif; color:#1A2E44; margin-top:0;">{art['titolo']}</h1>
        <p style="color:#C5A059; font-style:italic;">{art['data']}</p>
        <div style="font-size:1.2rem; line-height:1.7; font-family:serif;">
            {art['testo'].replace(chr(10), '<br>')}
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
