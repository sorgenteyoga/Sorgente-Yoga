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

all_a = load_a()

# --- CSS PER MENU AD APPARIZIONE (HOVER) ---
st.markdown(f"""
<style>
    .stApp {{ background-color: #FDFCF0 !important; }}
    
    /* Container dei menu */
    .menu-container {{
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-bottom: 30px;
    }}

    /* Singolo Menu */
    .dropdown {{
        position: relative;
        display: inline-block;
    }}

    /* Il Tasto Principale */
    .dropbtn {{
        background: transparent;
        color: #1A2E44;
        padding: 10px;
        font-size: 1.1rem;
        font-family: serif;
        border: none;
        cursor: pointer;
        letter-spacing: 1px;
    }}

    /* Contenuto della tendina (nascosto) */
    .dropdown-content {{
        display: none;
        position: absolute;
        background-color: #FDFCF0;
        min-width: 200px;
        box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.1);
        z-index: 1000;
        padding: 10px;
        border-top: 2px solid #C5A059; /* Unica linea elegante in alto */
    }}

    /* Mostra la tendina al passaggio del mouse */
    .dropdown:hover .dropdown-content {{
        display: block;
    }}

    /* Link/Bottoni dentro la tendina */
    .dropdown-content a {{
        color: #1A2E44;
        padding: 8px 0;
        text-decoration: none;
        display: block;
        font-family: serif;
        font-size: 1rem;
    }}

    .dropdown-content a:hover {{
        color: #C5A059;
        text-decoration: underline;
    }}

    .header-bar {{ 
        background:#1A2E44; padding:15px; color:#FDFCF0; font-family: serif; 
        text-align:center; font-size:1.6rem; letter-spacing:2px; margin-bottom:20px; 
    }}
    .art-box {{ background: white; padding:30px; border-radius:8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); color:#1A2E44; min-height:500px; }}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-bar">S O R G E N T E &nbsp; Y O G A</div>', unsafe_allow_html=True)

# --- FUNZIONE PER GENERARE IL MENU HTML ---
def render_menu(label, category):
    items = ""
    for i, a in enumerate(all_a):
        cat_match = str(a.get('cat','')).upper()
        if (category == "BLOG" and (cat_match == "BLOG" or not cat_match)) or (cat_match == category):
            # Usiamo un link speciale che Streamlit può intercettare o parametri query
            items += f'<a href="?art={i}">{a["titolo"]}</a>'
    
    html = f"""
    <div class="dropdown">
        <button class="dropbtn">{label}</button>
        <div class="dropdown-content">
            {items if items else "<a>Nessun articolo</a>"}
        </div>
    </div>
    """
    return html

# --- NAVIGAZIONE ---
cols = st.columns([1, 1, 1])
with cols[0]:
    st.markdown(render_menu("📂 ARCHIVIO", "BLOG"), unsafe_allow_html=True)
with cols[1]:
    st.markdown(render_menu("📜 TESTI ANTICHI", "TESTI"), unsafe_allow_html=True)
with cols[2]:
    st.markdown(render_menu("🔬 SCIENZA", "SCIENZA"), unsafe_allow_html=True)

# --- LOGICA DI SELEZIONE ---
# Streamlit legge l'indice dall'URL quando clicchi su un link del menu
query_params = st.query_params
if "art" in query_params:
    st.session_state['sel_idx'] = int(query_params["art"])

# --- AREA CONTENUTO ---
if 'sel_idx' not in st.session_state: 
    st.session_state['sel_idx'] = 0 if all_a else None

s_idx = st.session_state['sel_idx']

if s_idx is not None and s_idx < len(all_a):
    art = all_a[s_idx]
    st.markdown(f"""<div class="art-box">
        <h1 style="font-family:serif; color:#1A2E44; margin-top:0;">{art["titolo"]}</h1>
        <p style="color:#C5A059; font-style:italic;">{art["data"]}</p>
        <hr style="border:0; border-top:1px solid #eee; margin:20px 0;">
        <div style="font-family:serif; font-size:1.1rem; line-height:1.6; color:#333;">
            {art["testo"].replace(chr(10), '<br>')}
        </div>
    </div>""", unsafe_allow_html=True)
