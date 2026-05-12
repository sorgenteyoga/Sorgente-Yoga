import streamlit as st
import base64, os, json, requests
from datetime import datetime as dt

st.set_page_config(page_title="SORGENTE YOGA", layout="wide", page_icon="🧘")

# --- CONFIGURAZIONE GITHUB ---
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
GITHUB_REPO = st.secrets.get("GITHUB_REPO")
FILE_PATH = "archivio_articoli.json"

def save_to_github(content):
    if not GITHUB_TOKEN or not GITHUB_REPO:
        return
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    r = requests.get(url, headers=headers)
    sha = r.json().get('sha') if r.status_code == 200 else None
    data = {
        "message": f"Aggiornamento Sorgente Yoga {dt.now().strftime('%d/%m/%Y %H:%M')}",
        "content": base64.b64encode(content.encode("utf-8")).decode("utf-8"),
        "sha": sha
    }
    requests.put(url, headers=headers, data=json.dumps(data))

# --- FUNZIONI DATI ---
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

# --- INTERFACCIA E STILE ---
all_a = load_a()
ih = get_img("header_yoga.png")

st.markdown(f"""<style>
    .stApp {{ background-color: #FDFCF0 !important; }}
    .header-img {{ width:100%; height:100px; background: url('data:image/png;base64,{ih}') no-repeat center; background-size: contain; border-bottom: 3px solid #C5A059; }}
    .header-bar {{ background:#1A2E44; padding:15px; color:#FDFCF0; font-family: serif; text-align:center; font-size:1.6rem; letter-spacing:2px; margin-bottom:20px; }}
    .art-box {{ background: white; padding:40px; border-radius:8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); color:#1A2E44; min-height:500px; }}
    #MainMenu, footer, header {{ visibility:hidden; }}
</style>
<div class="header-img"></div>
<div class="header-bar">S O R G E N T E &nbsp; Y O G A</div>""", unsafe_allow_html=True)

if 'sel_idx' not in st.session_state: st.session_state['sel_idx'] = 0 if all_a else None
if 'mode' not in st.session_state: st.session_state['mode'] = "view"

# --- NAVIGAZIONE ---
c1, c2, c3, c4, c5 = st.columns([0.2, 0.2, 0.15, 0.15, 0.3])

with c1:
    with st.popover("📂 ARCHIVIO", use_container_width=True):
        for i, a in enumerate(all_a):
            if str(a.get('cat', '')).upper() == 'BLOG' or not a.get('cat'):
                if st.button(a['titolo'], key=f"b_{i}", use_container_width=True):
                    st.session_state['sel_idx'] = i
                    st.session_state['mode'] = "view"
                    st.rerun()

with c2:
    with st.popover("📜 TESTI ANTICHI", use_container_width=True):
        for i, a in enumerate(all_a):
            if str(a.get('cat', '')).upper() == 'TESTI':
                if st.button(a['titolo'], key=f"t_{i}", use_container_width=True):
                    st.session_state['sel_idx'] = i
                    st.session_state['mode'] = "view"
                    st.rerun()

# --- AREA CONTENUTO ---
idx = st.session_state['sel_idx']

if st.session_state['mode'] == "view":
    if idx is not None and idx < len(all_a):
        display = all_a[idx]
        st.markdown(f"""<div class="art-box">
            <h1 style="font-family:serif; color:#1A2E44; margin-top:0;">{display["titolo"]}</h1>
            <p style="color:#C5A059; font-style:italic;">{display["data"]}</p>
            <hr style="border:0; border-top:1px solid #eee; margin:20px 0;">
            <div style="font-family:serif; font-size:1.2rem; line-height:1.8; color:#333;">
                {display["testo"].replace(chr(10), '<br>')}
            </div>
        </div>""", unsafe_allow_html=True)

elif st.session_state['mode'] == "edit" and idx is not None:
    st.subheader("Modifica Articolo")
    curr = all_a[idx]
    new_t = st.text_input("Titolo", value=curr['titolo'])
    new_c = st.radio("Sezione", ["BLOG", "TESTI"], index=0 if str(curr.get('cat','')).upper()=="BLOG" else 1)
    new_x = st.text_area("Testo", value=curr['testo'], height=400)
    if st.button("SALVA MODIFICHE"):
        all_a[idx] = {"data": curr['data'], "titolo": new_t, "testo": new_x, "cat": new_c}
        save_a(all_a)
        st.session_state['mode'] = "view"; st.rerun()

elif st.session_state['mode'] == "new":
    st.subheader("Nuovo Articolo")
    t_n = st.text_input("Titolo")
    c_n = st.radio("Sezione", ["BLOG", "TESTI"])
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
