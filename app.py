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

# --- CSS INTEGRATO (MENU HOVER + HEADER + EDITOR) ---
st.markdown(f"""
<style>
    .stApp {{ background-color: #FDFCF0 !important; }}
    
    .header-img {{ 
        width:100%; height:120px; background: url('data:image/png;base64,{ih}') no-repeat center; 
        background-size: contain; border-bottom: 3px solid #C5A059; 
    }}

    .header-bar {{ 
        background:#1A2E44; padding:15px; color:#FDFCF0; font-family: serif; 
        text-align:center; font-size:1.6rem; letter-spacing:2px; margin-bottom:20px; 
    }}

    /* Container dei menu */
    .menu-row {{
        display: flex;
        justify-content: center;
        gap: 50px;
        margin-bottom: 30px;
    }}

    .dropdown {{ position: relative; display: inline-block; }}

    .dropbtn {{
        background: transparent; color: #1A2E44; padding: 10px;
        font-size: 1.1rem; font-family: serif; border: none;
        cursor: pointer; letter-spacing: 1px;
    }}

    .dropdown-content {{
        display: none; position: absolute; background-color: #FDFCF0;
        min-width: 220px; box-shadow: 0px 8px 16px rgba(0,0,0,0.1);
        z-index: 1000; padding: 10px; border-top: 2px solid #C5A059;
    }}

    .dropdown:hover .dropdown-content {{ display: block; }}

    .dropdown-content a {{
        color: #1A2E44; padding: 8px 0; text-decoration: none;
        display: block; font-family: serif; font-size: 1rem;
    }}

    .dropdown-content a:hover {{ color: #C5A059; text-decoration: underline; }}

    .art-box {{ background: white; padding:30px; border-radius:8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); color:#1A2E44; min-height:500px; }}
</style>
<div class="header-img"></div>
<div class="header-bar">S O R G E N T E &nbsp; Y O G A</div>
""", unsafe_allow_html=True)

# --- LOGICA DI NAVIGAZIONE ---
def render_menu(label, category):
    items = ""
    for i, a in enumerate(all_a):
        cat_match = str(a.get('cat','')).upper()
        if (category == "BLOG" and (cat_match == "BLOG" or not cat_match)) or (cat_match == category):
            items += f'<a href="?art={i}">{a["titolo"]}</a>'
    return f'<div class="dropdown"><button class="dropbtn">{label}</button><div class="dropdown-content">{items if items else "<a>Vuoto</a>"}</div></div>'

# Visualizzazione Menu
st.markdown(f"""
<div class="menu-row">
    {render_menu("📂 ARCHIVIO", "BLOG")}
    {render_menu("📜 TESTI ANTICHI", "TESTI")}
    {render_menu("🔬 SCIENZA", "SCIENZA")}
</div>
""", unsafe_allow_html=True)

# Gestione parametri URL e Session State
if "art" in st.query_params:
    st.session_state['sel_idx'] = int(st.query_params["art"])
    st.session_state['mode'] = "view"

if 'sel_idx' not in st.session_state: st.session_state['sel_idx'] = 0 if all_a else None
if 'mode' not in st.session_state: st.session_state['mode'] = "view"

# --- AREA CONTENUTO ---
s_idx = st.session_state['sel_idx']

if st.session_state['mode'] == "view":
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

elif st.session_state['mode'] == "edit" and s_idx is not None:
    st.subheader("Modifica Articolo")
    curr = all_a[s_idx]
    new_t = st.text_input("Titolo", value=curr['titolo'])
    new_c = st.radio("Sezione", ["BLOG", "TESTI", "SCIENZA"], index=["BLOG", "TESTI", "SCIENZA"].index(str(curr.get('cat','BLOG')).upper()))
    new_x = st.text_area("Testo", value=curr['testo'], height=400)
    if st.button("SALVA"):
        all_a[s_idx].update({"titolo": new_t, "testo": new_x, "cat": new_c})
        save_a(all_a); st.session_state.mode = "view"; st.rerun()

elif st.session_state['mode'] == "new":
    st.subheader("Nuovo Articolo")
    t_n = st.text_input("Titolo")
    c_n = st.radio("Sezione", ["BLOG", "TESTI", "SCIENZA"])
    x_n = st.text_area("Testo", height=400)
    if st.button("PUBBLICA"):
        if t_n and x_n:
            all_a.insert(0, {"data": dt.now().strftime("%d/%m/%Y"), "titolo": t_n, "testo": x_n, "cat": c_n})
            save_a(all_a); st.session_state.update({"sel_idx": 0, "mode": "view"}); st.rerun()

# --- AREA EDITORE (TASTI RIPRISTINATI) ---
st.write("<br><br>---", unsafe_allow_html=True)
ce1, ce2 = st.columns(2)
with ce1:
    if st.button("➕ NUOVO ARTICOLO", use_container_width=True):
        st.session_state.mode = "new"; st.rerun()
with ce2:
    if st.button("📝 MODIFICA QUESTO ARTICOLO", use_container_width=True):
        st.session_state.mode = "edit"; st.rerun()
