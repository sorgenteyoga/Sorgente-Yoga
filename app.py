import streamlit as st
import base64, os, json, requests
from datetime import datetime as dt

st.set_page_config(page_title="SORGENTE YOGA", layout="wide", page_icon="🧘")

# --- CONFIGURAZIONE GITHUB ---
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

# --- INTERFACCIA E CSS ADATTIVO ---
all_a = load_a()
ih = get_img("header_yoga.png")

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
    
    .art-box {{ background: white; padding:30px; border-radius:8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); color:#1A2E44; min-height:500px; }}
    
    div[data-testid="stPopover"] button[kind="secondary"] {{
        background: transparent !important; border: none !important; color: #1A2E44 !important;
        text-align: left !important; padding: 5px 0px !important; font-size: 1.1rem !important; justify-content: flex-start !important;
    }}
    div[data-testid="stPopover"] button[kind="secondary"]:hover {{ color: #C5A059 !important; text-decoration: underline !important; }}

    @media (max-width: 768px) {{
        .header-img {{ height: 80px !important; background-size: cover !important; }}
        .header-bar {{ font-size: 1.1rem !important; letter-spacing: 1px !important; padding: 10px !important; }}
        .art-box {{ padding: 20px !important; }}
        .art-box h1 {{ font-size: 1.4rem !important; line-height: 1.2 !important; }}
        div[data-testid="column"]:first-child {{ display: none !important; }}
    }}
</style>
<div class="header-img"></div>
<div class="header-bar">S O R G E N T E &nbsp; Y O G A</div>""", unsafe_allow_html=True)

if 'sel_idx' not in st.session_state: st.session_state['sel_idx'] = 0 if all_a else None
if 'mode' not in st.session_state: st.session_state['mode'] = "view"

# --- NAVIGAZIONE ---
vuoto, c1, c2, c3 = st.columns([0.15, 0.25, 0.25, 0.25])

with c1:
    with st.popover("📂 ARCHIVIO", use_container_width=True):
        blog_list = [(i, a) for i, a in enumerate(all_a) if str(a.get('cat','')).upper() == 'BLOG' or not a.get('cat')]
        for idx, a in blog_list:
            if st.button(a['titolo'], key=f"b_{idx}", use_container_width=True):
                st.session_state['sel_idx'] = idx; st.session_state['mode'] = "view"; st.rerun()

with c2:
    with st.popover("📜 TESTI ANTICHI", use_container_width=True):
        testi_list = [(i, a) for i, a in enumerate(all_a) if str(a.get('cat','')).upper() == 'TESTI']
        for idx, a in testi_list:
            if st.button(a['titolo'], key=f"t_{idx}", use_container_width=True):
                st.session_state['sel_idx'] = idx; st.session_state['mode'] = "view"; st.rerun()

with c3:
    with st.popover("🔬 SCIENZA", use_container_width=True):
        sci_list = [(i, a) for i, a in enumerate(all_a) if str(a.get('cat','')).upper() == 'SCIENZA']
        for idx, a in sci_list:
            if st.button(a['titolo'], key=f"s_{idx}", use_container_width=True):
                st.session_state['sel_idx'] = idx; st.session_state['mode'] = "view"; st.rerun()

# --- AREA CONTENUTO ---
s_idx = st.session_state['sel_idx']

if st.session_state['mode'] == "view":
    if s_idx is not None and s_idx < len(all_a):
        display = all_a[s_idx]
        st.markdown(f"""<div class="art-box">
            <h1 style="font-family:serif; color:#1A2E44; margin-top:0;">{display["titolo"]}</h1>
            <p style="color:#C5A059; font-style:italic;">{display["data"]}</p>
            <hr style="border:0; border-top:1px solid #eee; margin:20px 0;">
            <div style="font-family:serif; font-size:1.1rem; line-height:1.6; color:#333;">
                {display["testo"].replace(chr(10), '<br>')}
            </div>
        </div>""", unsafe_allow_html=True)

elif st.session_state['mode'] == "edit" and s_idx is not None:
    st.subheader("Modifica Articolo")
    curr = all_a[s_idx]
    new_t = st.text_input("Titolo", value=curr['titolo'])
    cat_options = ["BLOG", "TESTI", "SCIENZA"]
    try: idx_cat = cat_options.index(str(curr.get('cat','')).upper())
    except: idx_cat = 0
    new_c = st.radio("Sezione", cat_options, index=idx_cat)
    new_x = st.text_area("Testo", value=curr['testo'], height=400)
    if st.button("SALVA MODIFICHE"):
        all_a[s_idx] = {"data": curr['data'], "titolo": new_t, "testo": new_x, "cat": new_c}
        save_a(all_a)
        st.session_state['mode'] = "view"; st.rerun()

elif st.session_state['mode'] == "new":
    st.subheader("Nuovo Articolo")
    t_n = st.text_input("Titolo")
    c_n = st.radio("Sezione", ["BLOG", "TESTI", "SCIENZA"])
    x_n = st.text_area("Testo", height=400)
    if st.button("PUBBLICA"):
        if t_n and x_n:
            all_a.insert(0, {"data": dt.now().strftime("%d/%m/%Y"), "titolo": t_n, "testo": x_n, "cat": c_n})
            save_a(all_a)
            st.session_state['sel_idx'] = 0
            st.session_state['mode'] = "view"; st.rerun()

# --- AREA EDITORE ---
st.write("<br><br>---", unsafe_allow_html=True)
ce1, ce2 = st.columns(2)
with ce1:
    if st.button("➕ NUOVO ARTICOLO", use_container_width=True):
        st.session_state['mode'] = "new"; st.rerun()
with ce2:
    if st.button("📝 MODIFICA QUESTO ARTICOLO", use_container_width=True):
        st.session_state['mode'] = "edit"; st.rerun()
