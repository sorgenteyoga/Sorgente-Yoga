import streamlit as st
import base64, os, json, requests
from datetime import datetime as dt

st.set_page_config(page_title="SORGENTE YOGA", layout="wide", page_icon="🧘")

# --- GITHUB CONFIG (Invariato) ---
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
GITHUB_REPO = st.secrets.get("GITHUB_REPO")
FILE_PATH = "archivio_articoli.json"

def get_img(p):
    if os.path.exists(p):
        try:
            with open(p, "rb") as f: return base64.b64encode(f.read()).decode()
        except: return ""
    return ""

ih = get_img("header_yoga.png")

# --- CSS: AZZERAMENTO TOTALE E PARTENZA DALL'ALTO ---
st.markdown(f"""
<style>
    /* 1. NASCONDE LA BARRA TECNICA DI STREAMLIT */
    header[data-testid="stHeader"] {{
        visibility: hidden;
        height: 0% !important;
    }}

    /* 2. ELIMINA OGNI MARGINE E PADDING DELLA PAGINA */
    .block-container {{
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
    }}
    
    /* 3. FORZA L'APP A NON AVERE SPAZI VUOTI */
    .stApp {{ 
        background-color: #FDFCF0 !important; 
        margin-top: -50px !important; /* Recupera lo spazio della barra nascosta */
    }}

    /* 4. IMMAGINE GIGANTE CHE PARTE DA CIMA PAGINA */
    .header-img {{ 
        width: 100vw; 
        height: 400px; /* Puoi regolarla come preferisci */
        background: url('data:image/png;base64,{ih}') no-repeat center; 
        background-size: cover; 
        margin: 0 !important;
        padding: 0 !important;
    }}
    
    /* 5. BARRA BLU SORGENTE YOGA */
    .header-bar {{ 
        background:#1A2E44 !important; 
        padding:20px; 
        color:#FDFCF0 !important; 
        font-family: serif; 
        text-align:center; 
        font-size:2rem; 
        letter-spacing:4px; 
        margin: 0 !important;
        border-bottom: 4px solid #C5A059;
    }}

    .main-content {{
        padding: 40px;
    }}
</style>

<div class="header-img"></div>
<div class="header-bar">S O R G E N T E &nbsp; Y O G A</div>
""", unsafe_allow_html=True)

# Tutto il resto del codice (Popover e Articoli) va dentro il container per avere i margini corretti
with st.container():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # ... qui inserisci la logica dei popover e del contenuto come prima ...
    
    st.markdown('</div>', unsafe_allow_html=True)
