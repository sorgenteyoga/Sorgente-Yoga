import streamlit as st
import base64, os, json
from datetime import datetime as dt

st.set_page_config(page_title="SORGENTE YOGA", layout="wide", page_icon="🧘")

def get_img(p):
    if os.path.exists(p):
        with open(p, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

def load_a():
    if os.path.exists("archivio_articoli.json"):
        try:
            with open("archivio_articoli.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_a(arts):
    with open("archivio_articoli.json", "w", encoding="utf-8") as f:
        json.dump(arts, f, ensure_ascii=False, indent=4)

ih = get_img("header_yoga.png")

st.markdown(f"""<style>
.stApp {{ background:#FDFCF0; }}
.block-container {{ padding: 1rem 5% !important; }}
.header-img {{ width:100%; height:100px; background:url('data:image/png;base64,{ih}') no-repeat center; background-size:contain; border-bottom:3px solid #C5A059; }}
.header-bar {{ background:#1A2E44; padding:8px; color:#FDFCF0; font-family:serif; text-align:center; letter-spacing:2px; font-size:1.2rem; margin-bottom:15px; }}
.art-box {{ background:white; padding:40px; border-radius:5px; box-shadow:0 2px 12px rgba(0,0,0,0.06); color:#1A2E44; min-height:600px; margin-top:10px; }}
#MainMenu, footer, header {{ visibility:hidden; }}
button[data-testid="stBaseButton-secondary"] {{
    background-color: #1A2E44 !important;
    color: #FDFCF0 !important;
    border: 1px solid #C5A059 !important;
    font-family: serif !important;
    font-weight: bold !important;
    height: 45px;
}}
</style>
<div class="header-img"></div><div class="header-bar">S O R G E N T E &nbsp; Y O G A</div>""", unsafe_allow_html=True)

if 'adm' not in st.session_state: st.session_state['adm'] = False
if 'sel' not in st.session_state: st.session_state['sel'] = None

all_a = load_a()
b_a = [a for a in all_a if a.get('cat', 'BLOG') == 'BLOG']
t_a = [a for a in all_a if a.get('cat') == 'TESTI']

# --- NAVIGAZIONE ---
c_nav = st.columns([0.2, 0.2, 0.15, 0.15, 0.3])
with c_nav[0]:
    with st.popover("📂 ARCHIVIO", use_container_width=True):
        if b_a:
            for i, a in enumerate(b_a):
                if st.button(f"📄 {a['titolo']}", key=f"btn_b_{i}", use_container_width=True):
                    st.session_state['sel'] = a
                    st.rerun()
        else: st.write("Nessun articolo nel blog")

with c_nav[1]:
    with st.popover("📜 TESTI ANTICHI", use_container_width=True):
        if t_a:
            for j, a in enumerate(t_a):
                if st.button(f"📜 {a['titolo']}", key=f"btn_t_{j}", use_container_width=True):
                    st.session_state['sel'] = a
                    st.rerun()
        else: st.write("Nessun testo antico")

with c_nav[2]:
    with st.popover("🏛️ STORIA", use_container_width=True):
        st.markdown('<a href="http://hyp.soas.ac.uk/" target="_blank" style="text-decoration:none; color:#1A2E44; font-weight:bold; display:block; text-align:center; padding:10px; border:1px solid #eee;">Hatha Yoga Project ↗</a>', unsafe_allow_html=True)

with c_nav[3]:
    with st.popover("🔬 SCIENZA", use_container_width=True):
        st.markdown('<a href="https://www.iayt.org/" target="_blank" style="text-decoration:none; color:#1A2E44; font-weight:bold; display:block; text-align:center; padding:10px; border:1px solid #eee;">IAYT Yoga Therapy ↗</a>', unsafe_allow_html=True)

# --- VISUALIZZAZIONE CONTENUTO ---
cur = st.session_state['sel'] if st.session_state['sel'] else (all_a[0] if all_a else None)

if cur:
    # Sanitizzazione testo per evitare errori di rendering HTML
    testo_render = cur["testo"].replace("\n", "<br>")
    st.markdown(f"""<div class="art-box">
        <h1 style="font-family:serif; color:#1A2E44;">{cur["titolo"]}</h1>
        <p style="color:#C5A059; font-style:italic; margin-bottom:25px; border-bottom:1px solid #eee; padding-bottom:10px;">{cur["data"]}</p>
        <div style="font-family:serif; font-size:1.25rem; line-height:1.8;">{testo_render}</div>
    </div>""", unsafe_allow_html=True)
else:
    st.info("Benvenuto su Sorgente Yoga. Seleziona un articolo dai menu in alto.")

# --- AREA AUTORE ---
st.write("<br><br>", unsafe_allow_html=True)
if not st.session_state['adm']:
    with st.expander("🔑"):
        pwd = st.text_input("Password", type="password", key="login_pwd")
        if st.button("Entra", key="login_btn") and pwd == "sorgente2026":
            st.session_state['adm'] = True
            st.rerun()
else:
    st.info("✍️ MODALITÀ EDITORE")
    t1, t2, t3 = st.tabs(["📝 NUOVO", "✏️ MODIFICA", "⚙️ EXTRA"])
    
    with t1:
        c_n = st.radio("Sezione:", ["BLOG", "TESTI"], key="rad_new")
        t_n = st.text_input("Titolo", key="txt_new_tit")
        x_n = st.text_area("Testo", height=400, key="txt_new_area")
        if st.button("PUBBLICA", key="btn_pub"):
            if t_n and x_n:
                all_a.insert(0, {"data": dt.now().strftime("%d/%m/%Y"), "titolo": t_n, "testo": x_n, "cat": c_n})
                save_a(all_a)
                st.rerun()

    with t2:
        if all_a:
            titoli = [x['titolo'] for x in all_a]
            scelto = st.selectbox("Seleziona articolo", titoli, key="sel_mod")
            idx = titoli.index(scelto)
            all_a[idx]['cat'] = st.radio("Sezione", ["BLOG", "TESTI"], index=0 if all_a[idx].get('cat','BLOG')=="BLOG" else 1, key="rad_mod")
            all_a[idx]['titolo'] = st.text_input("Titolo", all_a[idx]['titolo'], key="txt_mod_tit")
            all_a[idx]['testo'] = st.text_area("Testo", all_a[idx]['testo'], height=400, key="txt_mod_area")
            c_btns = st.columns(2)
            if c_btns[0].button("SALVA MODIFICHE", key="btn_save"):
                save_a(all_a)
                st.rerun()
            if c_btns[1].button("ELIMINA ARTICOLO", key="btn_del"):
                all_a.pop(idx)
                save_a(all_a)
                st.rerun()

    with t3:
        st.download_button("BACKUP DATI", json.dumps(all_a, ensure_ascii=False), "backup_yoga.json", key="btn_bak")
        if st.button("ESCI", key="btn_logout"):
            st.session_state['adm'] = False
            st.rerun()
