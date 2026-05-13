import streamlit as st
import base64, os, json, requests
from datetime import datetime as dt

st.set_page_config(page_title="SORGENTE YOGA", layout="wide", page_icon="🧘")

# --- GITHUB CONFIG (Invariato) ---
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
GITHUB_REPO = st.secrets.get("GITHUB_REPO")
FILE_PATH = "archivio_articoli.json"

def save_to_github(content):
    if not GITHUB_TOKEN or not GITHUB_REPO: return
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FILE_PATH}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
        r = requests.get(url, headers=headers)
        sha = r.json().get('sha') if r.status_code == 200 else None
        data = {
            "message": f"Update {dt.now().strftime('%d/%m/%Y %H:%M')}",
            "content": base64.b64encode(content.encode("utf-8")).decode("utf-8"),
            "sha": sha
        }
        requests.put(url, headers=headers, data=json.dumps(data))
    except: pass

def load_a():
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                d = json.load(f)
                return d if isinstance(d, list) else []
        except: return []
    return []

def save_a(arts):
    content = json.dumps(arts, ensure_ascii=False, indent=4)
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    save_to_github(content)

def get_img(p):
    if os.path.exists(p):
        try:
            with open(p, "rb") as f: return base64.b64encode(f.read()).decode()
        except: return ""
    return ""

all_a = load_a()
ih = get_img("header_yoga.png")

# --- CSS DEFINITIVO: PULIZIA TOTALE ---
st.markdown(f"""<style>
    .stApp {{ background-color: #FDFCF0 !important; }}
    
    .header-img {{ 
        width:100%; height:120px; background: url('data:image/png;base64,{ih}') no-repeat center; 
        background-size: contain; border-bottom: 3px solid #C5A059; 
    }}
    
    .header-bar {{ 
        background:#1A2E44; padding:15px; color:#FDFCF0; font-family: serif; 
        text-align:center; font-size:1.6rem; letter-spacing:2px; margin-bottom:20px; 
    }}

    /* ELIMINA BORDI, OMBRE E CORNICETTE DAI POPOVER */
    div[data-testid="stPopoverContent"] {{
        background-color: #FDFCF0 !important;
        border: none !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05) !important;
        min-width: 150px !important;
        max-width: 220px !important;
        padding: 5px !important;
    }}
    
    /* Rimuove il triangolino/freccia */
    div[data-testid="stPopoverContent"] > div:first-child {{ display: none !important; }}

    /* Rende i bottoni dei menu invisibili come testo semplice */
    div[data-testid="stPopover"] > button {{
        background: transparent !important; border: none !important; color: #1A2E44 !important;
        font-family: serif !important; font-size: 1.1rem !important;
    }}

    /* Bottoni dentro la tendina: stretti e puliti */
    div[data-testid="stPopoverContent"] button {{
        background: transparent !important; border: none !important;
        text-align: left !important; justify-content: flex-start !important;
        width: 100% !important; padding: 2px 5px !important;
        font-size: 0.95rem !important; color: #1A2E44 !important;
    }}
    div[data-testid="stPopoverContent"] button:hover {{ color: #C5A059 !important; text-decoration: underline !important; }}

    .art-box {{ background: white; padding:30px; border-radius:8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); color:#1A2E44; min-height:500px; }}
</style>
<div class="header-img"></div>
<div class="header-bar">S O R G E N T E &nbsp; Y O G A</div>""", unsafe_allow_html=True)

if 'sel_idx' not in st.session_state: st.session_state['sel_idx'] = 0 if all_a else None
if 'mode' not in st.session_state: st.session_state['mode'] = "view"

# --- NAVIGAZIONE (Usando st.popover nativo ma "pulito" dal CSS) ---
vuoto, c1, c2, c3 = st.columns([0.15, 0.25, 0.25, 0.25])

with c1:
    with st.popover("📂 ARCHIVIO"):
        for idx, a in enumerate(all_a):
            if str(a.get('cat','')).upper() in ['BLOG', '']:
                if st.button(a['titolo'], key=f"b_{idx}", use_container_width=True):
                    st.session_state.update({"sel_idx": idx, "mode": "view"}); st.rerun()

with c2:
    with st.popover("📜 TESTI ANTICHI"):
        for idx, a in enumerate(all_a):
            if str(a.get('cat','')).upper() == 'TESTI':
                if st.button(a['titolo'], key=f"t_{idx}", use_container_width=True):
                    st.session_state.update({"sel_idx": idx, "mode": "view"}); st.rerun()

with c3:
    with st.popover("🔬 SCIENZA"):
        for idx, a in enumerate(all_a):
            if str(a.get('cat','')).upper() == 'SCIENZA':
                if st.button(a['titolo'], key=f"s_{idx}", use_container_width=True):
                    st.session_state.update({"sel_idx": idx, "mode": "view"}); st.rerun()

# --- AREA CONTENUTO & EDITOR (Invariati) ---
s_idx = st.session_state['sel_idx']

if st.session_state['mode'] == "view" and s_idx is not None:
    art = all_a[s_idx]
    st.markdown(f"""<div class="art-box">
        <h1 style="font-family:serif; color:#1A2E44; margin-top:0;">{art["titolo"]}</h1>
        <p style="color:#C5A059; font-style:italic;">{art["data"]}</p>
        <hr style="border:0; border-top:1px solid #eee; margin:20px 0;">
        <div style="font-family:serif; font-size:1.1rem; line-height:1.6; color:#333;">{art["testo"].replace(chr(10), '<br>')}</div>
    </div>""", unsafe_allow_html=True)
elif st.session_state['mode'] == "edit":
    # ... (Codice editore come prima)
    pass 

# Tasti in fondo
st.write("<br><br>---", unsafe_allow_html=True)
ce1, ce2 = st.columns(2)
with ce1:
    if st.button("➕ NUOVO ARTICOLO", use_container_width=True): st.session_state.mode = "new"; st.rerun()
with ce2:
    if st.button("📝 MODIFICA QUESTO ARTICOLO", use_container_width=True): st.session_state.mode = "edit"; st.rerun()
        
