import streamlit as st
import base64, os, json, requests
from datetime import datetime as dt

st.set_page_config(page_title="SORGENTE YOGA", layout="wide", page_icon="🧘")

# --- GITHUB CONFIG ---
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

# --- CSS DEFINITIVO (BLU #1A2E44 + TESTO BIANCO #FDFCF0) ---
st.markdown(f"""
<style>
    /* Sfondo generale */
    .stApp {{ background-color: #FDFCF0 !important; }}
    
    /* Header Immagine */
    .header-img {{ 
        width:100%; height:150px; background: url('data:image/png;base64,{ih}') no-repeat center; 
        background-size: contain; margin-bottom: 10px;
    }}
    
    /* Barra del titolo blu */
    .header-bar {{ 
        background:#1A2E44 !important; padding:15px; color:#FDFCF0 !important; 
        font-family: serif; text-align:center; font-size:1.6rem; 
        letter-spacing:2px; margin-bottom:20px; border-bottom: 3px solid #C5A059;
    }}

    /* TASTI POPOVER: BLU CON SCRITTA BIANCA */
    div[data-testid="stPopover"] > button {{
        background-color: #1A2E44 !important;
        color: #FDFCF0 !important;
        border: 1px solid #C5A059 !important;
        border-radius: 4px !important;
        padding: 12px 20px !important;
        font-family: serif !important;
        font-size: 1.1rem !important;
        width: 100% !important;
    }}

    /* Hover tasti menu */
    div[data-testid="stPopover"] > button:hover {{
        background-color: #C5A059 !important;
        color: #1A2E44 !important;
    }}

    /* Box Articolo */
    .art-box {{ 
        background: white; padding:40px; border-radius:8px; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); color:#1A2E44; 
    }}
</style>
<div class="header-img"></div>
<div class="header-bar">S O R G E N T E &nbsp; Y O G A</div>
""", unsafe_allow_html=True)

# --- LOGICA NAVIGAZIONE ---
if 'sel_idx' not in st.session_state: st.session_state['sel_idx'] = 0 if all_a else None
if 'mode' not in st.session_state: st.session_state['mode'] = 'view'

# Menu a tendina
c1, c2, c3 = st.columns(3)
with c1:
    with st.popover("📂 ARCHIVIO"):
        for i, a in enumerate(all_a):
            if str(a.get('cat','BLOG')).upper() in ['BLOG', '']:
                if st.button(a['titolo'], key=f"ar_{i}", use_container_width=True):
                    st.session_state.update({"sel_idx": i, "mode": "view"}); st.rerun()
with c2:
    with st.popover("📜 TESTI ANTICHI"):
        for i, a in enumerate(all_a):
            if str(a.get('cat','')).upper() == 'TESTI':
                if st.button(a['titolo'], key=f"te_{i}", use_container_width=True):
                    st.session_state.update({"sel_idx": i, "mode": "view"}); st.rerun()
with c3:
    with st.popover("🔬 SCIENZA"):
        for i, a in enumerate(all_a):
            if str(a.get('cat','')).upper() == 'SCIENZA':
                if st.button(a['titolo'], key=f"sc_{i}", use_container_width=True):
                    st.session_state.update({"sel_idx": i, "mode": "view"}); st.rerun()

st.write("---")

# --- VISUALIZZAZIONE / EDITOR ---
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

elif st.session_state.mode == "edit":
    st.subheader("Modifica Articolo")
    curr = all_a[s_idx]
    n_t = st.text_input("Titolo", value=curr['titolo'])
    n_c = st.selectbox("Categoria", ["BLOG", "TESTI", "SCIENZA"], index=["BLOG", "TESTI", "SCIENZA"].index(str(curr.get('cat','BLOG')).upper()))
    n_x = st.text_area("Testo", value=curr['testo'], height=400)
    if st.button("SALVA"):
        all_a[s_idx].update({"titolo": n_t, "testo": n_x, "cat": n_c})
        save_a(all_a); st.session_state.mode = "view"; st.rerun()

elif st.session_state.mode == "new":
    st.subheader("Nuovo Articolo")
    n_t = st.text_input("Titolo")
    n_c = st.selectbox("Categoria", ["BLOG", "TESTI", "SCIENZA"])
    n_x = st.text_area("Testo", height=400)
    if st.button("PUBBLICA"):
        all_a.insert(0, {"data": dt.now().strftime("%d/%m/%Y"), "titolo": n_t, "testo": n_x, "cat": n_c})
        save_a(all_a); st.session_state.update({"sel_idx": 0, "mode": "view"}); st.rerun()

# --- TASTI GESTIONE IN FONDO ---
st.write("<br><br>", unsafe_allow_html=True)
ce1, ce2 = st.columns(2)
with ce1:
    if st.button("➕ NUOVO ARTICOLO", use_container_width=True):
        st.session_state.mode = 'new'; st.rerun()
with ce2:
    if st.button("📝 MODIFICA QUESTO", use_container_width=True):
        st.session_state.mode = 'edit'; st.rerun()
