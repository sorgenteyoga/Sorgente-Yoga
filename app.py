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

# Caricamento icone e header
ih, i_a, i_t, i_s, i_z = get_img("header_yoga.png"), get_img("icona_archivio.png"), get_img("icona_testi.png"), get_img("icona_storia.png"), get_img("icona_scienza.png")

st.markdown(f"""<style>
.stApp {{ background:#FDFCF0; }}
.block-container {{ padding: 1rem 3% !important; }}
.header-image {{ width:100%; height:100px; background:url('data:image/png;base64,{ih}') no-repeat center; background-size:contain; border-bottom:3px solid #C5A059; }}
.header-bar {{ background:#1A2E44; padding:8px; color:#FDFCF0; font-family:serif; text-align:center; letter-spacing:1px; font-size:1.1rem; margin-bottom:20px; }}
.art-box {{ background:white; padding:25px; border-radius:5px; box-shadow:0 2px 8px rgba(0,0,0,0.05); margin-bottom:20px; color:#1A2E44; }}
@media (max-width:768px) {{ .header-image {{ height:60px; }} .art-box {{ padding:15px; }} .header-bar {{ font-size:0.9rem; }} }}
.i-title {{ display:flex; align-items:center; gap:8px; margin-top:15px; font-family:serif; font-weight:bold; color:#1A2E44; }}
.r-link {{ text-decoration:none; color:#1A2E44 !important; font-weight:bold; display:block; padding:8px 0; border-bottom:1px solid #eee; }}
#MainMenu, footer, header {{ visibility:hidden; }}
</style>
<div class="header-image"></div><div class="header-bar">S O R G E N T E &nbsp; Y O G A</div>""", unsafe_allow_html=True)

if 'adm' not in st.session_state: st.session_state['adm'] = False
if 'sel' not in st.session_state: st.session_state['sel'] = None

all_a = load_a()
b_a = [a for a in all_a if a.get('cat', 'BLOG') == 'BLOG']
t_a = [a for a in all_a if a.get('cat') == 'TESTI']

c1, c2 = st.columns([0.7, 0.3], gap="large")

with c1:
    # Visualizzazione Articolo
    cur = st.session_state['sel'] if st.session_state['sel'] else (all_a[0] if all_a else None)
    if cur:
        st.markdown(f'<div class="art-box"><h1 style="font-family:serif; margin-bottom:5px;">{cur["titolo"]}</h1><p style="color:#C5A059; font-style:italic; margin-bottom:20px;">{cur["data"]}</p><div style="font-family:serif; font-size:1.15rem; line-height:1.7;">{cur["testo"].replace("\\n","<br>")}</div></div>', unsafe_allow_html=True)
    else:
        st.info("Benvenuti su Sorgente Yoga. Seleziona un contenuto dalla biblioteca.")

    st.divider()
    # Gestione Autore
    if not st.session_state['adm']:
        with st.expander("🔑 Area Autore"):
            if st.text_input("Password", type="password") == "sorgente2026":
                st.session_state['adm'] = True; st.rerun()
    else:
        st.info("✍️ MODALITÀ EDITORE")
        with st.expander("📝 NUOVO ARTICOLO"):
            ct = st.radio("Sezione", ["BLOG", "TESTI"], key="n_cat")
            tt = st.text_input("Titolo")
            tx = st.text_area("Testo", height=450)
            if st.button("🚀 Pubblica") and tt and tx:
                all_a.insert(0, {"data": dt.now().strftime("%d/%m/%Y"), "titolo": tt, "testo": tx, "cat": ct})
                save_a(all_a); st.rerun()
        with st.expander("✏️ MODIFICA / ELIMINA"):
            if all_a:
                s = st.selectbox("Scegli articolo", [x['titolo'] for x in all_a])
                idx = [x['titolo'] for x in all_a].index(s)
                all_a[idx]['cat'] = st.radio("Sez", ["BLOG", "TESTI"], index=0 if all_a[idx].get('cat','BLOG')=="BLOG" else 1, key="e_cat")
                all_a[idx]['titolo'] = st.text_input("Tit", all_a[idx]['titolo'], key="e_tt")
                all_a[idx]['testo'] = st.text_area("Txt", all_a[idx]['testo'], height=500, key="e_tx")
                if st.button("💾 Salva"): save_a(all_a); st.rerun()
                if st.button("🗑️ Elimina"): all_a.pop(idx); save_a(all_a); st.rerun()
        if st.button("🔒 Esci"): st.session_state['adm'] = False; st.rerun()

with c2:
    st.markdown("### 🏛️ BIBLIOTECA")
    # Sezione Blog
    st.markdown(f'<div class="i-title"><img src="data:image/png;base64,{i_a}" width="22"> ARCHIVIO</div>', unsafe_allow_html=True)
    with st.expander("Articoli", expanded=True):
        for i, a in enumerate(b_a):
            if st.button(f"📄 {a['titolo']}", key=f"b{i}"): st.session_state['sel'] = a; st.rerun()
    
    # Sezione Testi Antichi
    st.markdown(f'<div class="i-title"><img src="data:image/png;base64,{i_t}" width="22"> TESTI ANTICHI</div>', unsafe_allow_html=True)
    with st.expander("Elenco"):
        for j, a in enumerate(t_a):
            if st.button(f"📜 {a['titolo']}", key=f"t{j}"): st.session_state['sel'] = a; st.rerun()
            
    # Risorse esterne
    st.markdown(f'<div class="i-title"><img src="data:image/png;base64,{i_s}" width="22"> STORIA</div>', unsafe_allow_html=True)
    st.markdown('<a class="r-link" href="http://hyp.soas.ac.uk/" target="_blank">Hatha Yoga Project ↗</a>', unsafe_allow_html=True)
    st.markdown(f'<div class="i-title"><img src="data:image/png;base64,{i_z}" width="22"> SCIENZA</div>', unsafe_allow_html=True)
    st.markdown('<a class="r-link" href="https://www.iayt.org/" target="_blank">IAYT Yoga Therapy ↗</a>', unsafe_allow_html=True)
    
