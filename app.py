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

def save_a(arts):
    content = json.dumps(arts, ensure_ascii=False, indent=4)
    with open(FILE_PATH, "w", encoding="utf-8") as f: f.write(content)
    if GITHUB_TOKEN and GITHUB_REPO:
        try:
            url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FILE_PATH}"
            headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
            r = requests.get(url, headers=headers)
            sha = r.json().get('sha') if r.status_code == 200 else None
            data = {"message": "Update", "content": base64.b64encode(content.encode()).decode(), "sha": sha}
            requests.put(url, headers=headers, data=json.dumps(data))
        except: pass

all_a = load_a()

# --- CSS: NUOVI COLORI E PULIZIA TOTALE ---
st.markdown(f"""<style>
    .stApp {{ background-color: #FDFCF0 !important; }}
    
    .header-bar {{ 
        background:#1A2E44; padding:15px; color:#FDFCF0; font-family: serif; 
        text-align:center; font-size:1.6rem; letter-spacing:2px; margin-bottom:20px; 
    }}

    /* STILE TASTI MENU (PIATTI E SENZA CORNICE) */
    div.stButton > button {{
        background-color: transparent !important;
        color: #1A2E44 !important;
        border: none !important;
        border-bottom: 2px solid transparent !important;
        font-family: serif !important;
        font-size: 1.1rem !important;
        padding: 5px 10px !important;
        transition: 0.3s;
    }}
    
    div.stButton > button:hover {{
        color: #C5A059 !important;
        border-bottom: 2px solid #C5A059 !important;
        background-color: transparent !important;
    }}

    .art-box {{ background: white; padding:30px; border-radius:8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); color:#1A2E44; }}
</style>
<div class="header-bar">S O R G E N T E &nbsp; Y O G A</div>""", unsafe_allow_html=True)

# --- NAVIGAZIONE ---
if 'cat_sel' not in st.session_state: st.session_state['cat_sel'] = 'BLOG'
if 'sel_idx' not in st.session_state: st.session_state['sel_idx'] = 0 if all_a else None
if 'mode' not in st.session_state: st.session_state['mode'] = 'view'

c1, c2, c3 = st.columns(3)
with c1:
    if st.button("📂 ARCHIVIO", use_container_width=True): st.session_state.cat_sel = 'BLOG'
with c2:
    if st.button("📜 TESTI ANTICHI", use_container_width=True): st.session_state.cat_sel = 'TESTI'
with c3:
    if st.button("🔬 SCIENZA", use_container_width=True): st.session_state.cat_sel = 'SCIENZA'

# Sottotitoli articoli filtrati (senza tendina, lista semplice)
st.write("---")
filtered = [(i, a) for i, a in enumerate(all_a) if str(a.get('cat','BLOG')).upper() == st.session_state.cat_sel]

cols_art = st.columns(len(filtered) if filtered else 1)
for i, (idx, art) in enumerate(filtered):
    with cols_art[i]:
        if st.button(art['titolo'], key=f"btn_{idx}"):
            st.session_state.update({"sel_idx": idx, "mode": "view"})
            st.rerun()

# --- AREA CONTENUTO ---
if st.session_state.mode == "view" and st.session_state.sel_idx is not None:
    display = all_a[st.session_state.sel_idx]
    st.markdown(f"""<div class="art-box">
        <h1 style="font-family:serif;">{display['titolo']}</h1>
        <p style="color:#C5A059;">{display['data']}</p>
        <div style="font-size:1.1rem; line-height:1.6;">{display['testo'].replace(chr(10), '<br>')}</div>
    </div>""", unsafe_allow_html=True)
    
# Tasti Editor in fondo
st.write("<br>", unsafe_allow_html=True)
if st.button("➕ NUOVO"): st.session_state.mode = 'new'; st.rerun()
if st.button("📝 MODIFICA"): st.session_state.mode = 'edit'; st.rerun()
