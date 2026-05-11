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

def salva_articolo(nuovo):
    articoli = carica_articoli()
    articoli.insert(0, nuovo)
    with open("archivio_articoli.json", "w", encoding="utf-8") as f:
        json.dump(articoli, f, ensure_ascii=False, indent=4)

def svuota_archivio():
    if os.path.exists("archivio_articoli.json"):
        os.remove("archivio_articoli.json")
    st.session_state['articolo_selezionato'] = None

# Caricamento risorse
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
        st.info("✍️ MODALITÀ EDITORE ATTIVA")
        tit_n = st.text_input("Titolo nuovo articolo")
        tes_n = st.text_area("Testo articolo", height=300)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🚀 Pubblica"):
                if tit_n and tes_n:
                    salva_articolo({"data": datetime.now().strftime("%d/%m/%Y"), "titolo": tit_n, "testo": tes_n})
                    st.rerun()
        with c2:
            if st.button("🗑️ Svuota Archivio"):
                svuota_archivio()
                st.warning("Archivio cancellato!")
                st.rerun()
        with c3:
            if st.button("🔒 Esci"):
                st.session_state['admin'] = False
                st.rerun()

    # Visualizzazione
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
        st.write("Nessun articolo presente. Accedi per scrivere il primo.")

with col_nav:
    st.markdown("### 🏛️ BIBLIOTECA")
    
    # Archivio
    st.markdown(f'<div class="icon-title-container"><img src="data:image/png;base64,{icon_archivio}" class="icon-img"><span class="icon-text">ARCHIVIO BLOG</span></div>', unsafe_allow_html=True)
    with st.expander("Sfoglia articoli", expanded=True):
        if tutti_gli_articoli:
            for i, a in enumerate(tutti_gli_articoli):
                if st.button(f"📄 {a['titolo']}", key=f"btn_{i}"):
                    st.session_state['articolo_selezionato'] = a
                    st.rerun()
        else: st.write("Vuoto.")

    # Altre sezioni...
    st.markdown(f'<div class="icon-title-container"><img src="data:image/png;base64,{icon_testi}" class="icon-img"><span class="icon-text">TESTI CLASSICI</span></div>', unsafe_allow_html=True)
    with st.expander("Elenco testi"):
        st.write("• Yoga Sūtra")
