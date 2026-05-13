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

ih = get_img("header_yoga.png")

# --- CSS RADICALE PER ELIMINARE GLI SPAZI BIANCHI ---
st.markdown(f"""
<style>
    /* 1. ELIMINA LA BARRA DI SISTEMA IN ALTO E I SUOI MARGINI */
    header[data-testid="stHeader"] {{
        display: none !important;
    }}
    
    /* 2. AZZERA TUTTI I PADDING DEL CONTENITORE PRINCIPALE */
    .block-container {{
        padding: 0px !important;
        margin: 0px !important;
        max-width: 100% !important;
    }}

    /* 3. RIMUOVE LO SPAZIO BIANCO EXTRA IN CIMA */
    .stApp {{
        margin-top: -60px !important;
    }}

    /* 4. IMMAGINE: FULL WIDTH E ALTEZZA MAGGIORE */
    .header-img {{ 
        width: 100vw; 
        height: 380px; /* Qui puoi aumentare ancora se la vuoi più grande */
        background: url('data:image/png;base64,{ih}') no-repeat center; 
        background-size: cover; 
        margin: 0px !important;
        padding: 0px !important;
        display: block;
    }}
    
    /* 5. BARRA BLU: ATTACCATA ALL'IMMAGINE (MARGIN-TOP 0) */
    .header-bar {{ 
        background:#1A2E44 !important; 
        padding:30px 10px; 
        color:#FDFCF0 !important; 
        font-family: serif; 
        text-align:center; 
        font-size:2.2rem; 
        letter-spacing:5px; 
        margin-top: -5px !important; /* Piccola correzione per eliminare micro-spazi */
        border-bottom: 5px solid #C5A059;
        text-transform: uppercase;
    }}

    /* 6. CORPO DEL SITO: RIPRISTINA I MARGINI SOLO PER IL TESTO */
    .content-wrapper {{
        padding: 40px 10%;
        background-color: #FDFCF0;
    }}
</style>

<div class="header-img"></div>
<div class="header-bar">Sorgente Yoga</div>
""", unsafe_allow_html=True)

# Tutto ciò che segue va dentro questo "wrapper" per non stare attaccato ai bordi dello schermo
st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

# Qui metti il resto del codice per i menu e gli articoli...
st.info("Carica l'altra immagine per sistemare i tasti del menu!")

st.markdown('</div>', unsafe_allow_html=True)
