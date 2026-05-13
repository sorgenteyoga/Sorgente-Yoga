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

# --- CSS SEMPLIFICATO E PULITO ---
st.markdown(f"""
<style>
    /* 1. Rimuoviamo solo il padding eccessivo, senza nascondere l'header di sistema */
    .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        max-width: 100% !important;
    }}
    
    .stApp {{ background-color: #FDFCF0 !important; }}

    /* 2. Immagine grande e piena, ma senza spostamenti negativi */
    .header-img {{ 
        width: 100%; 
        height: 400px; 
        background: url('data:image/png;base64,{ih}') no-repeat center; 
        background-size: cover; 
        margin-bottom: 0px !important;
    }}
    
    /* 3. Barra blu che segue l'immagine naturalmente */
    .header-bar {{ 
        background:#1A2E44 !important; 
        padding:20px; 
        color:#FDFCF0 !important; 
        font-family: serif; 
        text-align:center; 
        font-size:2rem; 
        letter-spacing:4px; 
        border-bottom: 4px solid #C5A059;
        margin-top: 0px !important;
    }}

    .main-body {{
        padding: 40px 10%;
    }}

    .art-box {{ 
        background: white; padding:40px; border-radius:8px; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); color:#1A2E44; 
    }}
</style>
""", unsafe_allow_html=True)

# Visualizzazione Header sequenziale (uno sotto l'altro, niente sovrapposizioni)
st.markdown('<div class="header-img"></div>', unsafe_allow_html=True)
st.markdown('<div class="header-bar">S O R G E N T E &nbsp; Y O G A</div>', unsafe_allow_html=True)

st.markdown('<div class="main-body">', unsafe_allow_html=True)

if 'sel_idx' not in st.session_state: st.session_state['sel_idx'] = 0 if all_a else None
if 'mode' not in st.session_state: st.session_state['mode'] = 'view'

# Menu a tendina
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

# Visualizzazione Articolo
s_idx = st.session_state['sel_idx']
if st.session_state.mode == "view" and s_idx is not None:
    art = all_a[s_idx]
    st.markdown(f"""<div class="art-box">
        <h1 style="font-family:serif; color:#1A2E44;">{art['titolo']}</h1>
        <p style="color:#C5A059; font-style:italic;">{art['data']}</p>
        <div style="font-size:1.2rem; line-height:1.7; font-family:serif;">
            {art['testo'].replace(chr(10), '<br>')}
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
