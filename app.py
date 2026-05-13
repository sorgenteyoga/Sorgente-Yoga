import streamlit as st
import base64, os, json, requests
from datetime import datetime as dt

st.set_page_config(page_title="SORGENTE YOGA", layout="wide", page_icon="🧘")

# --- GITHUB CONFIG ---
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

# --- CSS: MIMETIZZAZIONE CORNICE E RIPRISTINO HEADER ---
st.markdown(f"""<style>
    .stApp {{ background-color: #FDFCF0 !important; }}
    
    /* Immagine in alto ripristinata */
    .header-img {{ 
        width:100%; height:150px; background: url('data:image/png;base64,{ih}') no-repeat center; 
        background-size: contain; margin-bottom: 10px;
    }}
    
    .header-bar {{ 
        background:#1A2E44; padding:15px; color:#FDFCF0; font-family: serif; 
        text-align:center; font-size:1.6rem; letter-spacing:2px; margin-bottom:20px; 
    }}

    /* STILE POPOVER (IL TASTO) */
    div[data-testid="stPopover"] > button {{
        background-color: transparent !important;
        color: #1A2E44 !important;
        border: 1px solid #C5A059 !important; /* Cornice dorata sottile sul tasto */
        border-radius: 0px !important;
        font-family: serif !important;
    }}

    /* STILE TENDINA (IL CONTENUTO CHE APPARE) */
    div[data-testid="stPopoverContent"] {{
        background-color: #FDFCF0 !important;
        border: 1px solid #C5A059 !important; /* Rendiamo la cornice dorata invece che grigia */
        box-shadow: none !important;
        padding: 10px !important;
        width: 250px !important;
    }}
    
    /* Bottoni dentro la tendina */
    div[data-testid="stPopoverContent"] button {{
        text-align: left !important;
        background: transparent !important;
        border: none !important;
        color: #1A2E44 !important;
        padding: 5px 0px !important;
    }}
    
    div[data-testid="stPopoverContent"] button:hover {{
        color: #C5A059 !important;
        text-decoration: underline !important;
    }}

    .art-box {{ background: white; padding:30px; border-radius:8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); color:#1A2E44; }}
</style>
<div class="header-img"></div>
<div class="header-bar">S O R G E N T E &nbsp; Y O G A</div>""", unsafe_allow_html=True)

# --- NAVIGAZIONE ---
if 'sel_idx' not in st.session_state: st.session_state['sel_idx'] = 0 if all_a else None
if 'mode' not in st.session_state: st.session_state['mode'] = 'view'

# Colonne per i menu a tendina
c1, c2, c3 = st.columns(3)

with c1:
    with st.popover("📂 ARCHIVIO", use_container_width=True):
        for i, a in enumerate(all_a):
            if str(a.get('cat','BLOG')).upper() == 'BLOG' or not a.get('cat'):
                if st.button(a['titolo'], key=f"arch_{i}"):
                    st.session_state.update({"sel_idx": i, "mode": "view"}); st.rerun()

with c2:
    with st.popover("📜 TESTI ANTICHI", use_container_width=True):
        for i, a in enumerate(all_a):
            if str(a.get('cat','')).upper() == 'TESTI':
                if st.button(a['titolo'], key=f"testi_{i}"):
                    st.session_state.update({"sel_idx": i, "mode": "view"}); st.rerun()

with c3:
    with st.popover("🔬 SCIENZA", use_container_width=True):
        for i, a in enumerate(all_a):
            if str(a.get('cat','')).upper() == 'SCIENZA':
                if st.button(a['titolo'], key=f"sci_{i}"):
                    st.session_state.update({"sel_idx": i, "mode": "view"}); st.rerun()

# --- AREA CONTENUTO ---
st.write("---")
if st.session_state.sel_idx is not None and st.session_state.mode == "view":
    art = all_a[st.session_state.sel_idx]
    st.markdown(f"""<div class="art-box">
        <h1 style="font-family:serif; margin-top:0;">{art['titolo']}</h1>
        <p style="color:#C5A059; font-style:italic;">{art['data']}</p>
        <div style="font-size:1.1rem; line-height:1.6; font-family:serif;">
            {art['testo'].replace(chr(10), '<br>')}
        </div>
    </div>""", unsafe_allow_html=True)

# --- TASTI GESTIONE IN FONDO ---
st.write("<br><br>", unsafe_allow_html=True)
col_ed1, col_ed2 = st.columns(2)
with col_ed1:
    if st.button("➕ NUOVO ARTICOLO", use_container_width=True):
        st.session_state.mode = 'new'; st.rerun()
with col_ed2:
    if st.button("📝 MODIFICA QUESTO", use_container_width=True):
        st.session_state.mode = 'edit'; st.rerun()
