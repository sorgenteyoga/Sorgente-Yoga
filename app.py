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
        for i, a in enumerate(b_a):
            if st.button(f"📄 {a['titolo']}", key=f"b{i}", use_container_width=True):
                st.session_state['sel'] = a; st.rerun()
with c_nav[1]:
    with st.popover("📜 TESTI ANTICHI", use_container_width=True):
        for j, a in enumerate(t_a):
            if st.button(f"📜 {a['titolo']}", key=f"t{j}", use_container_width=True):
                st.session_state['sel'] = a; st.rerun()
with c_nav[2]:
    with st.popover("🏛️ STORIA", use_container_width=True):
        st.markdown('<a href="http://hyp.soas.ac.uk/" target="_blank" style="text-decoration:none; color:#1A2E44; font-weight:bold; display:block; text-align:center; padding:10px; border:1px solid #eee;">Hatha Yoga Project ↗</a>', unsafe_allow_html=True)
with c_nav[3]:
    with st.popover("🔬 SCIENZA", use_container_width=True):
        st.markdown('<a href="https://www.iayt.org/" target="_blank" style="text-decoration:none; color:#1A2E44; font-weight:bold; display:block; text-align:center; padding:10px; border:1px solid #eee;">IAYT Yoga Therapy ↗</a>', unsafe_allow_html=True)

# --- CONTENUTO ---
cur = st.session_state['sel'] if st.session_state['sel'] else (all_a[0] if all_a else None)
if cur:
    st.markdown(f"""<div class="art-box">
        <h1 style="font-family:serif; color:#1A2E44;">{cur["titolo"]}</h1>
        <p style="color:#C5A059; font-style:italic; margin-bottom:25px; border-bottom:1px solid #eee; padding-bottom:10px;">{cur["data"]}</p>
        <div style="font-family:serif; font-size:1.25rem; line-height:1.8;">{cur["testo"].replace("\\n","<br>")}</div>
    </div>""", unsafe_allow_html=True)

# --- AREA AUTORE CORRETTA ---
st.write("<br><br>", unsafe_allow_html=True)
if not st.session_state['adm']:
    with st.expander("🔑"):
        p = st.text_input("Password", type="password")
        if st.button("Entra") and p == "sorgente2026":
            st.session_state['adm'] = True; st.rerun()
else:
    st.info("✍️ PANNELLO EDITORE ATTIVO")
    # Uso dei TAB per separare nettamente le funzioni
    t_nuovo, t_modifica, t_opzioni = st.tabs(["📝 NUOVO ARTICOLO", "✏️ MODIFICA ESISTENTE", "⚙️ OPZIONI"])
    
    with t_nuovo:
        ct_n = st.radio("Destinazione:", ["BLOG", "TESTI"], key="new_cat_radio")
        tt_n = st.text_input("Titolo Nuovo Articolo", key="new_tit")
        tx_n = st.text_area("Contenuto", height=400, key="new_tx")
        if st.button("🚀 PUBBLICA ORA"):
            if tt_n and tx_n:
                all_a.insert(0, {"data": dt.now().strftime("%d/%m/%Y"), "titolo": tt_n, "testo": tx_n, "cat": ct_n})
                save_a(all_a); st.rerun()
            else:
                st.error("Inserisci titolo e testo!")

    with t_modifica:
        if all_a:
            titles = [x['titolo'] for x in all_a]
            s_edit = st.selectbox("Seleziona l'articolo da modificare:", titles, key="sel_edit")
            idx = titles.index(s_edit)
            # Carichiamo i dati solo di quel specifico articolo
            all_a[idx]['cat'] = st.radio("Sposta in:", ["BLOG", "TESTI"], index=0 if all_a[idx].get('cat','BLOG')=="BLOG" else 1, key="e_cat")
            all_a[idx]['titolo'] = st.text_input("Modifica Titolo", all_a[idx]['titolo'], key="e_tt")
            all_a[idx]['testo'] = st.text_area("Modifica Testo", all_a[idx]['testo'], height=400, key="e_tx")
            col_btns = st.columns([0.2, 0.2, 0.6])
            with col_btns[0]:
                if st.button("💾 SALVA"): save_a(all_a); st.rerun()
            with col_btns[1]:
                if st.button("🗑️ ELIMINA"): all_a.pop(idx); save_a(all_a); st.rerun()
        else:
            st.warning("Nessun articolo presente nell'archivio.")

    with t_opzioni:
        st.download_button("📥 SCARICA BACKUP (JSON)", json.dumps(all_a, ensure_ascii=False), "sorgente_yoga_backup.json")
        if st.button("🔒 ESCI DALLA MODALITÀ EDITORE"):
            st.session_state['adm'] = False; st.rerun()
