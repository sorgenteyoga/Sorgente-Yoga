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
        with open("archivio_articoli.json", "r", encoding="utf-8") as f: return json.load(f)
    return []

def save_a(arts):
    with open("archivio_articoli.json", "w", encoding="utf-8") as f: json.dump(arts, f, ensure_ascii=False, indent=4)

ih = get_img("header_yoga.png")

# CSS per Header e Navigazione
st.markdown(f"""<style>
.stApp {{ background:#FDFCF0; }}
.block-container {{ padding: 1rem 5% !important; }}
.header-img {{ width:100%; height:100px; background:url('data:image/png;base64,{ih}') no-repeat center; background-size:contain; border-bottom:3px solid #C5A059; }}
.header-bar {{ background:#1A2E44; padding:8px; color:#FDFCF0; font-family:serif; text-align:center; letter-spacing:2px; font-size:1.2rem; }}
.nav-bar {{ background:#eee; padding:5px; border-radius:5px; margin-bottom:20px; border:1px solid #ddd; }}
.art-box {{ background:white; padding:30px; border-radius:5px; box-shadow:0 2px 10px rgba(0,0,0,0.05); color:#1A2E44; min-height:400px; }}
#MainMenu, footer, header {{ visibility:hidden; }}
</style>
<div class="header-img"></div><div class="header-bar">S O R G E N T E &nbsp; Y O G A</div>""", unsafe_allow_html=True)

if 'adm' not in st.session_state: st.session_state['adm'] = False
if 'sel' not in st.session_state: st.session_state['sel'] = None

all_a = load_a()
b_a = [a for a in all_a if a.get('cat', 'BLOG') == 'BLOG']
t_a = [a for a in all_a if a.get('cat') == 'TESTI']

# --- BARRA DI NAVIGAZIONE ORIZZONTALE ---
n1, n2, n3, n4 = st.columns(4)

with n1:
    with st.popover("📂 ARCHIVIO BLOG", use_container_width=True):
        for i, a in enumerate(b_a):
            if st.button(f"📄 {a['titolo']}", key=f"b{i}", use_container_width=True):
                st.session_state['sel'] = a; st.rerun()

with n2:
    with st.popover("📜 TESTI ANTICHI", use_container_width=True):
        for j, a in enumerate(t_a):
            if st.button(f"📜 {a['titolo']}", key=f"t{j}", use_container_width=True):
                st.session_state['sel'] = a; st.rerun()

with n3:
    with st.popover("🏛️ STORIA", use_container_width=True):
        st.markdown('[Hatha Yoga Project ↗](http://hyp.soas.ac.uk/)')

with n4:
    with st.popover("🔬 SCIENZA", use_container_width=True):
        st.markdown('[IAYT Yoga Therapy ↗](https://www.iayt.org/)')

# --- CONTENUTO PRINCIPALE ---
cur = st.session_state['sel'] if st.session_state['sel'] else (all_a[0] if all_a else None)

if cur:
    st.markdown(f"""<div class="art-box">
        <h1 style="font-family:serif; margin-bottom:5px;">{cur["titolo"]}</h1>
        <p style="color:#C5A059; font-style:italic; margin-bottom:20px;">{cur["data"]}</p>
        <div style="font-family:serif; font-size:1.2rem; line-height:1.8;">{cur["testo"].replace("\\n","<br>")}</div>
    </div>""", unsafe_allow_html=True)

# --- AREA AUTORE (SPOSTATA IN FONDO PER PULIZIA) ---
st.write("---")
if not st.session_state['adm']:
    if st.button("🔑 Accesso Autore"):
        with st.form("pwd"):
            p = st.text_input("Password", type="password")
            if st.form_submit_button("Entra") and p == "sorgente2026":
                st.session_state['adm'] = True; st.rerun()
else:
    with st.expander("✍️ PANNELLO DI CONTROLLO EDITORE"):
        st.download_button("📥 BACKUP DATI", json.dumps(all_a, ensure_ascii=False), "yoga_db.json")
        col_new, col_mod = st.columns(2)
        with col_new:
            st.subheader("📝 NUOVO")
            ct = st.radio("Sezione", ["BLOG", "TESTI"], key="n_cat")
            tt = st.text_input("Titolo")
            tx = st.text_area("Testo", height=300)
            if st.button("🚀 Pubblica") and tt and tx:
                all_a.insert(0, {"data": dt.now().strftime("%d/%m/%Y"), "titolo": tt, "testo": tx, "cat": ct})
                save_a(all_a); st.rerun()
        with col_mod:
            st.subheader("✏️ MODIFICA")
            if all_a:
                s = st.selectbox("Scegli", [x['titolo'] for x in all_a])
                idx = [x['titolo'] for x in all_a].index(s)
                all_a[idx]['cat'] = st.radio("Sez", ["BLOG", "TESTI"], index=0 if all_a[idx].get('cat','BLOG')=="BLOG" else 1, key="e_cat")
                all_a[idx]['titolo'] = st.text_input("Titolo", all_a[idx]['titolo'], key="e_tt")
                all_a[idx]['testo'] = st.text_area("Testo", all_a[idx]['testo'], height=300, key="e_tx")
                if st.button("💾 Salva"): save_a(all_a); st.rerun()
                if st.button("🗑️ Elimina"): all_a.pop(idx); save_a(all_a); st.rerun()
    if st.button("🔒 Esci"): st.session_state['adm'] = False; st.rerun()
