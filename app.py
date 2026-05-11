import streamlit as st
import base64
import os
import json
from datetime import datetime

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="SORGENTE YOGA", layout="wide", page_icon="🧘")

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

def carica_articoli():
    if os.path.exists("archivio_articoli.json"):
        with open("archivio_articoli.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salva_tutti_articoli(articoli):
    with open("archivio_articoli.json", "w", encoding="utf-8") as f:
        json.dump(articoli, f, ensure_ascii=False, indent=4)

def aggiungi_articolo(nuovo):
    articoli = carica_articoli()
    articoli.insert(0, nuovo)
    salva_tutti_articoli(articoli)

# --- CARICAMENTO RISORSE ---
img_header = get_base64_image("header_yoga.png")
icon_archivio = get_base64_image("icona_archivio.png")
icon_testi = get_base64_image("icona_testi.png")
icon_storia = get_base64_image("icona_storia.png")
icon_scienza = get_base64_image("icona_scienza.png")

# --- CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #FDFCF0; }}
    .header-container {{ width: 100%; background-color: white; border-bottom: 3px solid #C5A059; margin-bottom: 30px; }}
    .header-image {{ width: 100%; height: 250px; background-image: url('data:image/png;base64,{img_header}'); background-size: cover; background-position: center; }}
    .header-title-bar {{ background-color: #1A2E44; padding: 15px; color: #FDFCF0; font-family: 'serif'; font-size: 1.8rem; letter-spacing: 3px; text-align: center; }}
    .article-box {{ background-color: white; padding: 40px; border-radius: 5px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-top: 20px; min-height: 300px; }}
    .icon-title-container {{ display: flex; align-items: center; gap: 12px; margin-top: 25px; margin-bottom: 10px; }}
    .icon-img {{ width: 35px; height: 35px; object-fit: contain; }}
    .icon-text {{ font-weight: bold; color: #1A2E44; font-family: 'serif'; font-size: 1.1rem; }}
    #MainMenu, footer, header {{visibility: hidden;}}
    </style>
    <div class="header-container">
        <div class="header-image"></div>
        <div class="header-title-bar">S O R G E N T E &nbsp; Y O G A</div>
    </div>
    """, unsafe_allow_html=True)

if 'admin' not in st.session_state: st.session_state['admin'] = False
if 'articolo_selezionato' not in st.session_state: st.session_state['articolo_selezionato'] = None

tutti_gli_articoli = carica_articoli()

col_main, col_nav = st.columns([0.7, 0.3], gap="large")

with col_main:
    if not st.session_state['admin']:
        with st.expander("🔑 Area Autore"):
            pwd = st.text_input("Password", type="password")
            if pwd == "sorgente2026":
                st.session_state['admin'] = True
                st.rerun()
    
    if st.session_state['admin']:
        st.info("✍️ MODALITÀ EDITORE")
        
        # TAB 1: SCRITTURA
        with st.expander("📝 SCRIVI NUOVO ARTICOLO", expanded=True):
            tit_n = st.text_input("Titolo")
            tes_n = st.text_area("Testo", height=250)
            if st.button("🚀 Pubblica Articolo"):
                if tit_n and tes_n:
                    aggiungi_articolo({"data": datetime.now().strftime("%d/%m/%Y"), "titolo": tit_n, "testo": tes_n})
                    st.success("Articolo pubblicato!")
                    st.rerun()

        # TAB 2: ELIMINAZIONE SINGOLA
        with st.expander("🗑️ GESTIONE ARCHIVIO (Elimina Singoli)"):
            if tutti_gli_articoli:
                for idx, a in enumerate(tutti_gli_articoli):
                    c_tit, c_del = st.columns([0.8, 0.2])
                    c_tit.write(f"**{a['titolo']}** ({a['data']})")
                    if c_del.button("Elimina", key=f"del_{idx}"):
                        nuova_lista = [art for i, art in enumerate(tutti_gli_articoli) if i != idx]
                        salva_tutti_articoli(nuova_lista)
                        st.session_state['articolo_selezionato'] = None
                        st.rerun()
            else:
                st.write("Nessun articolo da eliminare.")

        if st.button("🔒 Esci dalla modalità editore"):
            st.session_state['admin'] = False
            st.rerun()

    # Visualizzazione Articolo Selezionato o Ultimo
    art = st.session_state['articolo_selezionato'] if st.session_state['articolo_selezionato'] else (tutti_gli_articoli[0] if tutti_gli_articoli else None)
    if art:
        st.markdown(f"""
        <div class="article-box">
            <h1 style='font-family:serif; color:#1A2E44;'>{art['titolo']}</h1>
            <p style='font-style:italic; color:#C5A059;'>{art['data']} • Luca Valenti</p>
            <div style='font-family:serif; font-size:1.3rem; line-height:1.8; white-space: pre-wrap;'>{art['testo']}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.write("L'archivio è vuoto. Accedi per pubblicare il tuo primo studio.")

with col_nav:
    st.markdown("### 🏛️ BIBLIOTECA")
    
    # Archivio Blog
    st.markdown(f'<div class="icon-title-container"><img src="data:image/png;base64,{icon_archivio}" class="icon-img"><span class="icon-text">ARCHIVIO BLOG</span></div>', unsafe_allow_html=True)
    with st.expander("Sfoglia articoli", expanded=True):
        if tutti_gli_articoli:
            for i, a in enumerate(tutti_gli_articoli):
                if st.button(f"📄 {a['titolo']}", key=f"nav_{i}"):
                    st.session_state['articolo_selezionato'] = a
                    st.rerun()
        else:
            st.caption("Vuoto.")

    # Sezioni statiche (Testi, Storia, Scienza)
    st.markdown(f'<div class="icon-title-container"><img src="data:image/png;base64,{icon_testi}" class="icon-img"><span class="icon-text">TESTI CLASSICI</span></div>', unsafe_allow_html=True)
    with st.expander("Elenco testi"):
        st.write("• Yoga Sūtra")
        st.write("• Haṭha Yoga Pradīpikā")
