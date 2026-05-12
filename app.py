import streamlit as st
import base64, os, json
from datetime import datetime as dt

st.set_page_config(page_title="SORGENTE YOGA", layout="wide", page_icon="🧘")

def load_a():
    if os.path.exists("archivio_articoli.json"):
        try:
            with open("archivio_articoli.json", "r", encoding="utf-8") as f:
                d = json.load(f)
                return d if isinstance(d, list) else []
        except:
            return []
    return []

def save_a(arts):
    with open("archivio_articoli.json", "w", encoding="utf-8") as f:
        json.dump(arts, f, ensure_ascii=False, indent=4)

def get_img(p):
    if os.path.exists(p):
        with open(p, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

all_a = load_a()
ih = get_img("header_yoga.png")

st.markdown(f"""<style>
.stApp {{ background:#FDFCF0; }}
.header-img {{ width:100%; height:100px; background:url('data:image/png;base64,{ih}') no-repeat center; background-size:contain; border-bottom:3px solid #C5A059; }}
.header-bar {{ background:#1A2E44; padding:8px; color:#FDFCF0; font-family:serif; text-align:center; letter-spacing:2px; font-size:1.2rem; margin-bottom:15px; }}
.art-box {{ background:white; padding:40px; border-radius:5px; box-shadow:0 2px 12px rgba(0,0,0,0.06); color:#1A2E44; min-height:500px; }}
#MainMenu, footer, header {{ visibility:hidden; }}
button[data-testid="stBaseButton-secondary"] {{ background-color:#1A2E44 !important; color:#FDFCF0 !important; border:1px solid #C5A059 !important; }}
</style>
<div class="header-img"></div><div class="header-bar">S O R G E N T E &nbsp; Y O G A</div>""", unsafe_allow_html=True)

if 'adm' not in st.session_state: st.session_state['adm'] = False
if 'sel' not in st.session_state: st.session_state['sel'] = None

b_a = [a for a in all_a if a.get('cat') == 'BLOG']
t_a = [a for a in all_a if a.get('cat') == 'TESTI']

c1, c2, c3, c4, c5 = st.columns([0.2, 0.2, 0.15, 0.15, 0.3])
with c1:
    with st.popover("📂 ARCHIVIO", use_container_width=True):
        if not b_a: st.write("Vuoto")
        for i, a in enumerate(b_a):
            if st.button(a['titolo'], key=f"b_{i}", use_container_width=True):
                st.session_state['sel'] = a; st.rerun()
with c2:
    with st.popover("📜 TESTI ANTICHI", use_container_width=True):
        if not t_a: st.write("Vuoto")
        for j, a in enumerate(t_a):
            if st.button(a['titolo'], key=f"t_{j}", use_container_width=True):
                st.session_state['sel'] = a; st.rerun()

display = st.session_state['sel'] if st.session_state['sel'] else (all_a[0] if all_a else None)
if display:
    st.markdown(f"""<div class="art-box">
        <h1 style="font-family:serif; color:#1A2E44;">{display["titolo"]}</h1>
        <p style="color:#C5A059; font-style:italic;">{display["data"]}</p>
        <div style="font-family:serif; font-size:1.25rem; line-height:1.8;">{display["testo"].replace(chr(10), '<br>')}</div>
    </div>""", unsafe_allow_html=True)

st.write("<br><br>---", unsafe_allow_html=True)
if not st.session_state['adm']:
    if st.button("🔑"):
        st.session_state['adm'] = True; st.rerun()
else:
    with st.expander("📝 PANNELLO DI CONTROLLO", expanded=True):
        pwd = st.text_input("Password", type="password")
        if pwd == "sorgente2026":
            t_new = st.text_input("Titolo")
            c_new = st.radio("Sezione", ["BLOG", "TESTI"])
            x_new = st.text_area("Testo", height=300)
            if st.button("SALVA E PUBBLICA"):
                if t_new and x_new:
                    all_a.insert(0, {"data": dt.now().strftime("%d/%m/%Y"), "titolo": t_new, "testo": x_new, "cat": c_new})
                    save_a(all_a); st.success("Pubblicato!"); st.rerun()
    if st.button("Esci"): st.session_state['adm'] = False; st.rerun()
