import streamlit as st
import base64, os, json
from datetime import datetime as dt

st.set_page_config(page_title="SORGENTE YOGA", layout="wide", page_icon="🧘")

# --- FUNZIONI DATI ---
def load_a():
    if os.path.exists("archivio_articoli.json"):
        try:
            with open("archivio_articoli.json", "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content.startswith('{') and not content.startswith('['):
                    content = "[" + content + "]"
                d = json.loads(content)
                return d if isinstance(d, list) else []
        except: return []
    return []

def save_a(arts):
    with open("archivio_articoli.json", "w", encoding="utf-8") as f:
        json.dump(arts, f, ensure_ascii=False, indent=4)

def get_img(p):
    if os.path.exists(p):
        try:
            with open(p, "rb") as f: return base64.b64encode(f.read()).decode()
        except: return ""
    return ""

# --- SETUP ---
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
        found_blog = False
        for i, a in enumerate(all_a):
            # Se la categoria è BLOG o se manca del tutto, lo mettiamo qui
            if str(a.get('cat', '')).upper() == 'BLOG' or not a.get('cat'):
                found_blog = True
                if st.button(a['titolo'], key=f"b_{i}", use_container_width=True):
                    st.session_state['sel_idx'] = i
                    st.session_state['mode'] = "view"
                    st.rerun()
        if not found_blog: st.write("Nessun articolo")

with c2:
    with st.popover("📜 TESTI ANTICHI", use_container_width=True):
        found_testi = False
        for i, a in enumerate(all_a):
            if str(a.get('cat', '')).upper() == 'TESTI':
                found_testi = True
                if st.button(a['titolo'], key=f"t_{i}", use_container_width=True):
                    st.session_state['sel_idx'] = i
                    st.session_state['mode'] = "view"
                    st.rerun()
        if not found_testi: st.write("Nessun testo antico")

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
    else:
        st.info("Benvenuto in Sorgente Yoga. Seleziona un articolo o creane uno nuovo.")

elif st.session_state['mode'] == "edit" and idx is not None:
    st.subheader("Modifica Articolo")
    curr = all_a[idx]
    new_t = st.text_input("Titolo", value=curr['titolo'])
    new_c = st.radio("Sezione", ["BLOG", "TESTI"], index=0 if str(curr.get('cat','')).upper()=="BLOG" else 1)
    new_x = st.text_area("Testo", value=curr['testo'], height=400)
    c_edit1, c_edit2 = st.columns(2)
    if c_edit1.button("SALVA MODIFICHE", use_container_width=True):
        all_a[idx] = {"data": curr['data'], "titolo": new_t, "testo": new_x, "cat": new_c}
        save_a(all_a)
        st.session_state['mode'] = "view"
        st.rerun()
    if c_edit2.button("ANNULLA", use_container_width=True):
        st.session_state['mode'] = "view"
        st.rerun()

elif st.session_state['mode'] == "new":
    st.subheader("Nuovo Articolo")
    t_n = st.text_input("Titolo")
    c_n = st.radio("Sezione", ["BLOG", "TESTI"])
    x_n = st.text_area("Testo", height=400)
    c_new1, c_new2 = st.columns(2)
    if c_new1.button("PUBBLICA", use_container_width=True):
        if t_n and x_n:
            all_a.insert(0, {"data": dt.now().strftime("%d/%m/%Y"), "titolo": t_n, "testo": x_n, "cat": c_n})
            save_a(all_a)
            st.session_state['sel_idx'] = 0
            st.session_state['mode'] = "view"
            st.rerun()
    if c_new2.button("ANNULLA", use_container_width=True):
        st.session_state['mode'] = "view"
        st.rerun()

# --- AREA EDITORE (In fondo) ---
st.write("<br><br>---", unsafe_allow_html=True)
ce1, ce2 = st.columns(2)

with ce1:
    if st.button("➕ NUOVO ARTICOLO", use_container_width=True):
        st.session_state['mode'] = "new"
        st.rerun()
with ce2:
    if st.button("📝 MODIFICA QUESTO ARTICOLO", use_container_width=True):
        st.session_state['mode'] = "edit"
        st.rerun()
