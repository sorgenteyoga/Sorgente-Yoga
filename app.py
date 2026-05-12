import streamlit as st
import base64, os, json
from datetime import datetime as dt

st.set_page_config(page_title="SORGENTE YOGA", layout="wide", page_icon="🧘")

# --- FUNZIONI DI CARICAMENTO ---
def get_img(p):
    if os.path.exists(p):
        with open(p, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

def load_a():
    if os.path.exists("archivio_articoli.json"):
        try:
            with open("archivio_articoli.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except Exception:
            return []
    return []

def save_a(arts):
    with open("archivio_articoli.json", "w", encoding="utf-8") as f:
        json.dump(arts, f, ensure_ascii=False, indent=4)

# --- PREPARAZIONE DATI E IMMAGINI ---
ih = get_img("header_yoga.png")
all_a = load_a()

# Suddivisione categorie
b_a = [a for a in all_a if a.get('cat') == 'BLOG' or 'cat' not in a]
t_a = [a for a in all_a if a.get('cat') == 'TESTI']

# --- STILE CSS ---
st.markdown(f"""<style>
.stApp {{ background:#FDFCF0; }}
.block-container {{ padding: 1rem 5% !important; }}
.header-img {{ width:100%; height:100px; background:url('data:image/png;base64,{ih}') no-repeat center; background-size:contain; border-bottom:3px solid #C5A059; }}
.header-bar {{ background:#1A2E44; padding:8px; color:#FDFCF0; font-family:serif; text-align:center; letter-spacing:2px; font-size:1.2rem; margin-bottom:15px; }}
.art-box {{ background:white; padding:40px; border-radius:5px; box-shadow:0 2px 12px rgba(0,0,0,0.06); color:#1A2E44; min-height:500px; }}
#MainMenu, footer, header {{ visibility:hidden; }}
button[data-testid="stBaseButton-secondary"] {{
    background-color: #1A2E44 !important;
    color: #FDFCF0 !important;
    border: 1px solid #C5A059 !important;
    font-family: serif !important;
    font-weight: bold !important;
}}
</style>
<div class="header-img"></div><div class="header-bar">S O R G E N T E &nbsp; Y O G A</div>""", unsafe_allow_html=True)

# Inizializzazione stati
if 'adm' not in st.session_state: st.session_state['adm'] = False
if 'sel' not in st.session_state: st.session_state['sel'] = None

# --- NAVIGAZIONE ---
c_nav = st.columns([0.2, 0.2, 0.15, 0.15, 0.3])

with c_nav[0]:
    with st.popover("📂 ARCHIVIO", use_container_width=True):
        if b_a:
            for i, a in enumerate(b_a):
                if st.button(f"📄 {a['titolo']}", key=f"nav_blog_{i}", use_container_width=True):
                    st.session_state['sel'] = a
                    st.rerun()
        else: st.write("Archivio vuoto")

with c_nav[1]:
    with st.popover("📜 TESTI ANTICHI", use_container_width=True):
        if t_a:
            for j, a in enumerate(t_a):
                if st.button(f"📜 {a['titolo']}", key=f"nav_testi_{j}", use_container_width=True):
                    st.session_state['sel'] = a
                    st.rerun()
        else: st.write("Nessun testo antico")

with c_nav[2]:
    with st.popover("🏛️ STORIA", use_container_width=True):
        st.markdown('<a href="http://hyp.soas.ac.uk/" target="_blank" style="text-decoration:none; color:#1A2E44; font-weight:bold; display:block; text-align:center; padding:10px; border:1px solid #eee;">Hatha Yoga Project ↗</a>', unsafe_allow_html=True)

with c_nav[3]:
    with st.popover("🔬 SCIENZA", use_container_width=True):
        st.markdown('<a href="https://www.iayt.org/" target="_blank" style="text-decoration:none; color:#1A2E44; font-weight:bold; display:block; text-align:center; padding:10px; border:1px solid #eee;">IAYT Yoga Therapy ↗</a>', unsafe_allow_html=True)

# --- VISUALIZZAZIONE ARTICOLO ---
# Se non c'è una selezione, mostra l'ultimo inserito
display_art = st.session_state['sel'] if st.session_state['sel'] else (all_a[0] if all_a else None)

if display_art:
    st.markdown(f"""<div class="art-box">
        <h1 style="font-family:serif; color:#1A2E44;">{display_art["titolo"]}</h1>
        <p style="color:#C5A059; font-style:italic; margin-bottom:25px; border-bottom:1px solid #eee; padding-bottom:10px;">{display_art["data"]}</p>
        <div style="font-family:serif; font-size:1.25rem; line-height:1.8;">{display_art["testo"].replace('\n', '<br>')}</div>
    </div>""", unsafe_allow_html=True)
else:
    st.info("Benvenuto su Sorgente Yoga. Seleziona un contenuto dal menu superiore.")

# --- AREA EDITORE ---
st.divider()
if not st.session_state['adm']:
    with st.expander("🔑"):
        p = st.text_input("Password", type="password")
        if st.button("Accedi") and p == "sorgente2026":
            st.session_state['adm'] = True
            st.rerun()
else:
    st.success("MODALITÀ EDITORE ATTIVA")
    tab1, tab2, tab3 = st.tabs(["📝 NUOVO", "✏️ MODIFICA", "⚙️ SISTEMA"])
    
    with tab1:
        cat_n = st.radio("Sezione", ["BLOG", "TESTI"], key="new_cat")
        tit_n = st.text_input("Titolo", key="new_tit")
        txt_n = st.text_area("Testo", height=400, key="new_txt")
        if st.button("PUBBLICA ARTICOLO"):
            if tit_n and txt_n:
                new_art = {"data": dt.now().strftime("%d/%m/%Y"), "titolo": tit_n, "testo": txt_n, "cat": cat_n}
                all_a.insert(0, new_art)
                save_a(all_a)
                st.session_state['sel'] = new_art
                st.rerun()

    with tab2:
        if all_a:
            t_list = [x['titolo'] for x in all_a]
            to_edit = st.selectbox("Scegli articolo da modificare", t_list)
            idx = t_list.index(to_edit)
            
            all_a[idx]['cat'] = st.radio("Sposta in", ["BLOG", "TESTI"], index=0 if all_a[idx].get('cat')=='BLOG' else 1, key="mod_cat")
            all_a[idx]['titolo'] = st.text_input("Modifica Titolo", all_a[idx]['titolo'], key="mod_tit")
            all_a[idx]['testo'] = st.text_area("Modifica Testo", all_a[idx]['testo'], height=400, key="mod_txt")
            
            c_ed = st.columns(2)
            if c_ed[0].button("SALVA MODIFICHE"):
                save_a(all_a)
                st.session_state['sel'] = all_a[idx]
                st.rerun()
            if c_ed[1].button("ELIMINA DEFINITIVAMENTE"):
                all_a.pop(idx)
                save_a(all_a)
                st.session_state['sel'] = None
                st.rerun()

    with tab3:
        st.download_button("SCARICA DATABASE", json.dumps(all_a, ensure_ascii=False), "yoga_db.json")
        if st.button("ESCI DALL'AREA EDITORE"):
            st.session_state['adm'] = False
            st.rerun()
