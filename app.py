import streamlit as st
import base64, os, json, requests
from datetime import datetime as dt

st.set_page_config(page_title="SORGENTE YOGA", layout="wide", page_icon="🧘")

# --- GITHUB CONFIG (Invariato) ---
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
GITHUB_REPO = st.secrets.get("GITHUB_REPO")
FILE_PATH = "archivio_articoli.json"

def load_a():
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                d = json.load(f)
                return d if isinstance(d, list) else []
        except: return []
    return []

def get_img(p):
    if os.path.exists(p):
        try:
            with open(p, "rb") as f: return base64.b64encode(f.read()).decode()
        except: return ""
    return ""

all_a = load_a()
ih = get_img("header_yoga.png")

# --- CSS: HEADER GIGANTE E ZERO MARGINI ---
st.markdown(f"""
<style>
    /* ELIMINA I MARGINI DI STREAMLIT IN ALTO E AI LATI */
    .block-container {{
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
    }}
    
    .stApp {{ background-color: #FDFCF0 !important; }}

    /* IMMAGINE FULL-WIDTH (TAGLIATA AI LATI SE NECESSARIO) */
    .header-img {{ 
        width: 100vw; 
        height: 350px; /* Aumentato per renderla più grande */
        background: url('data:image/png;base64,{ih}') no-repeat center; 
        background-size: cover; /* Forza il riempimento totale */
        margin: 0 !important;
        padding: 0 !important;
    }}
    
    /* BARRA BLU ATTACCATA ALL'IMMAGINE */
    .header-bar {{ 
        background:#1A2E44 !important; 
        padding:20px; 
        color:#FDFCF0 !important; 
        font-family: serif; 
        text-align:center; 
        font-size:1.8rem; 
        letter-spacing:4px; 
        margin: 0 !important;
        border-bottom: 4px solid #C5A059;
    }}

    /* SPAZIATURA PER IL CONTENUTO (Per non farlo stare attaccato ai bordi dopo il menu) */
    .main-content {{
        padding: 40px;
    }}

    .art-box {{ 
        background: white; padding:40px; border-radius:8px; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); color:#1A2E44; 
    }}
</style>
<div class="header-img"></div>
<div class="header-bar">S O R G E N T E &nbsp; Y O G A</div>
""", unsafe_allow_html=True)

# Container per staccare il resto del sito dai bordi
with st.container():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # --- LOGICA NAVIGAZIONE (Manteniamo i Popover per ora) ---
    if 'sel_idx' not in st.session_state: st.session_state['sel_idx'] = 0 if all_a else None
    if 'mode' not in st.session_state: st.session_state['mode'] = 'view'

    c1, c2, c3 = st.columns(3)
    with c1:
        with st.popover("📂 ARCHIVIO", use_container_width=True):
            for i, a in enumerate(all_a):
                if str(a.get('cat','BLOG')).upper() in ['BLOG', '']:
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

    # --- AREA CONTENUTO ---
    s_idx = st.session_state['sel_idx']
    if st.session_state.mode == "view" and s_idx is not None:
        art = all_a[s_idx]
        st.markdown(f"""<div class="art-box">
            <h1 style="font-family:serif; color:#1A2E44;">{art['titolo']}</h1>
            <p style="color:#C5A059;">{art['data']}</p>
            <div style="font-size:1.2rem; line-height:1.7; font-family:serif;">
                {art['testo'].replace(chr(10), '<br>')}
            </div>
        </div>""", unsafe_allow_html=True)
    
    # ... (Resto dei pulsanti Nuovo/Modifica)
    st.markdown('</div>', unsafe_allow_html=True)
