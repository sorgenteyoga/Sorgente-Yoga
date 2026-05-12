import streamlit as st
import base64, os, json
from datetime import datetime

st.set_page_config(page_title="SORGENTE YOGA", layout="wide", page_icon="🧘")

def get_base64_image(p):
    if os.path.exists(p):
        with open(p, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

def carica_articoli():
    if os.path.exists("archivio_articoli.json"):
        with open("archivio_articoli.json", "r", encoding="utf-8") as f: return json.load(f)
    return []

def salva_tutti_articoli(arts):
    with open("archivio_articoli.json", "w", encoding="utf-8") as f: json.dump(arts, f, ensure_ascii=False, indent=4)

img_h = get_base64_image("header_yoga.png")
i_arc = get_base64_image("icona_archivio.png")
i_tes = get_base64_image("icona_testi.png")
i_sto = get_base64_image("icona_storia.png")
i_sci = get_base64_image("icona_scienza.png")

st.markdown(f"""
<style>
.stApp {{ background-color: #FDFCF0; }}
.block-container {{ padding: 1rem 5% !important; }}
.header-container {{ border-bottom: 3px solid #C5A059; margin-bottom: 25px; }}
.header-image {{ width: 100%; height: 120px; background: url('data:image/png;base64,{img_h}') no-repeat center; background-size: contain; }}
.header-title-bar {{ background: #1A2E44; padding: 10px; color: #FDFCF0; font-family: serif; font-size: 1.2rem; text-align: center; letter-spacing: 2px; }}
.article-box {{ background: white; padding: 30px; border-radius: 5px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }}
@media (max-width: 768px) {{ .header-image {{ height: 80px; }} .article-box {{ padding: 15px; }} }}
.icon-title {{ display: flex; align-items: center; gap: 10px; margin-top: 20px; font-family: serif; font-weight: bold; color: #1A2E44; }}
.resource-link {{ text-decoration: none; color: #1A2E44 !important; font-weight: bold; display: block; padding: 5px 0; border-bottom: 1px solid #eee; }}
#MainMenu, footer, header {{ visibility: hidden; }}
</style>
<div class="header-container"><div class="header-image"></div><div class="header-title-bar">S O R G E N T E &nbsp; Y O G A</div></div>
""", unsafe_allow_html=True)

if 'admin' not in st.session_state: st.session_state['admin'] = False
if 'art_sel' not in st.session_state: st.session_state['art_sel'] = None

tutti = carica_articoli()
arts_blog = [a for a in tutti if a.get('categoria', 'ARCHIVIO BLOG') == 'ARCHIVIO BLOG']
arts_antichi = [a for a in tutti if a.get('categoria') == 'TESTI ANTICHI']

c_main, c_nav = st.columns([0.7, 0.3], gap="large")

with c_main:
    if not st.session_state['admin']:
        with st.expander("🔑 Area Autore"):
            if st.text_input("Password", type="password") == "sorgente2026":
                st.session_state['admin'] = True
                st.rerun()
    else:
        st.info("✍️ MODALITÀ EDITORE")
        if tutti:
            st.download_button("📥 BACKUP", json.dumps(tutti, ensure_ascii=False), "backup.json")
        with st.expander("📝 NUOVO"):
            cat = st.radio("Sezione", ["ARCHIVIO BLOG", "TESTI ANTICHI"])
            tit = st.text_input("Titolo")
            tes = st.text_area("Testo", height=200)
            if st.button("🚀 Pubblica") and tit and tes:
                tutti.insert(0, {"data": datetime.now().strftime("%d/%m/%Y"), "titolo": tit, "testo": tes, "categoria": cat})
                salva_tutti_articoli(tutti)
                st.rerun()
        with st.expander("✏️ MODIFICA / ELIMINA"):
            if tutti:
                sel = st.selectbox("Articolo", [a['titolo'] for a in tutti])
                idx = [a['titolo'] for a in tutti].index(sel)
                tutti[idx]['categoria'] = st.radio("Cat", ["ARCHIVIO BLOG", "TESTI ANTICHI"], index=0 if tutti[idx].get('categoria', 'ARCHIVIO BLOG') == "ARCHIVIO BLOG" else 1)
                tutti[idx]['titolo'] = st.text_input("Titolo attuale", tutti[idx]['titolo'])
                tutti[idx]['testo'] = st.text_area("Testo attuale", tutti[idx]['testo'], height=200)
                if st.button("💾 Salva"):
                    salva_tutti_articoli(tutti)
                    st.rerun()
                if st.button("🗑️ Elimina"):
                    tutti.pop(idx)
                    salva_tutti_articoli(tutti)
                    st.rerun()
        if st.button("🔒 Esci"):
            st.session_state['admin'] = False
            st.rerun()

    art = st.session_state['art_sel'] if st.session_state['art_sel'] else (tutti[0] if tutti else None)
    if art:
        txt = art['testo'].replace('\n', '<br>')
        st.markdown(f'<div class="article-box"><h1 style="font-family:serif; color:#1A2E44;">{art["titolo"]}</h1><p style="color:#C5A059;">{art["data"]} • {art.get("categoria","Blog")}</p><div style="font-family:serif; font-size:1.2rem; line-height:1.7;">{txt}</div></div>', unsafe_allow_html=True)
    else: st.write("Benvenuti su Sorgente Yoga.")

with c_nav:
    st.markdown("### 🏛️ BIBLIOTECA")
    st.markdown(f'<div class="icon-title"><img src="data:image/png;base64,{i_arc}" width="25"> ARCHIVIO BLOG</div>', unsafe_allow_html=True)
    with st.expander("Articoli", expanded=True):
        for i, a in enumerate(arts_blog):
            if st.button(f"📄 {a['titolo']}", key=f"b{i}"):
                st.session_state['art_sel'] = a
                st.rerun()
    st.markdown(f'<div class="icon-title"><img src="data:image/png;base64,{i_tes}" width="25"> TESTI ANTICHI</div>', unsafe_allow_html=True)
    with st.expander("Elenco"):
        for j, a in enumerate(arts_antichi):
            if st.button(f"📜 {a['titolo']}", key=f"t{j}"):
                st.session_state['art_sel'] = a
                st.rerun()
    st.markdown(f'<div class="icon-title"><img src="data:image/png;base64,{i_sto}" width="25"> RICERCA STORICA</div>', unsafe_allow_html=True)
    with st.expander("Link"):
        st.markdown('<a class="resource-link" href="http://hyp.soas.ac.uk/" target="_blank">Hatha Yoga Project ↗</a>', unsafe_allow_html=True)
    st.markdown(f'<div class="icon-title"><img src="data:image/png;base64,{i_sci}" width="25"> SCIENZA</div>', unsafe_allow_html=True)
    with st.expander("Link"):
        st.markdown('<a class="resource-link" href="https://www.iayt.org/" target="_blank">IAYT Yoga Therapy ↗</a>', unsafe_allow_html=True)
