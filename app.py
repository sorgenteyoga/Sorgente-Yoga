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

all_a = [] # Carica qui i tuoi articoli
ih = get_img("header_yoga.png")

# --- CSS PER ALZARE TUTTO IL SITO ---
st.markdown(f"""
<style>
    /* 1. ELIMINA LO SPAZIO BIANCO IN ALTO (Header di sistema) */
    [data-testid="stHeader"] {{
        display: none !important;
    }}

    /* 2. RIDUCE IL MARGINE SUPERIORE DEL CONTENITORE PRINCIPALE */
    .block-container {{
        padding-top: 0rem !important; /* Azzera il padding in alto */
        margin-top: -30px !important; /* "Tira" tutto il sito verso l'alto */
    }}

    /* 3. STILE HEADER (Immagine) */
    .header-img {{ 
        width:100%; height:250px; /* Aumentata un po' per equilibrio */
        background: url('data:image/png;base64,{ih}') no-repeat center; 
        background-size: cover; 
        margin-bottom: 0px !important;
    }}
    
    /* 4. BARRA BLU SORGENTE YOGA */
    .header-bar {{ 
        background:#1A2E44; padding:20px; color:#FDFCF0; 
        font-family: serif; text-align:center; font-size:2rem; 
        letter-spacing:4px; margin-top: 0px !important;
        border-bottom: 4px solid #C5A059;
    }}

    .stApp {{ background-color: #FDFCF0 !important; }}
</style>
""", unsafe_allow_html=True)

# Visualizzazione sequenziale corretta
st.markdown('<div class="header-img"></div>', unsafe_allow_html=True)
st.markdown('<div class="header-bar">S O R G E N T E &nbsp; Y O G A</div>', unsafe_allow_html=True)

# --- RESTO DEL SITO (Tasti e Contenuti) ---
st.markdown('<div style="padding: 30px 10%;">', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1: st.popover("📂 ARCHIVIO", use_container_width=True)
with c2: st.popover("📜 TESTI ANTICHI", use_container_width=True)
with c3: st.popover("🔬 SCIENZA", use_container_width=True)

st.write("---")
# Qui appariranno i tuoi articoli...

st.markdown('</div>', unsafe_allow_html=True)
