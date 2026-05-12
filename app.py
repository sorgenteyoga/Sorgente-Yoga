import streamlit as st
import base64
import os
import json
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="SORGENTE YOGA", layout="wide", page_icon="🧘")

# --- FUNZIONI DI SERVIZIO ---
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

# --- CSS E HEADER (VERSIONE RESPONSIVE) ---
css_code = f"""
    <style>
    .stApp {{ background-color: #FDFCF0; }}
    
    .block-container {{ 
        padding-top: 1rem !important; 
        padding-bottom: 1rem !important; 
        max-width: 95%; 
    }}

    .header-container {{ width: 100%; background-color: #FDFCF0; border-bottom: 3px solid #C5A059; margin-bottom: 25px; }}
    
    .header-image {{ 
        width: 100%; height: 120px;
        background-image: url('data:image/png;base64,{img_header}'); 
        background-size: contain; background-repeat: no-repeat; background-position: center; 
    }}

    .header-title-bar {{ 
        background-color: #1A2E44; padding: 10px; color: #FDFCF0; 
        font-family: 'serif'; font-size: 1.2rem;
        letter-spacing: 2px; text-align: center; 
    }}

    .article-box {{ 
        background-color: white; padding: 30px; border-radius: 5px; 
        box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-top: 10px; 
    }}

    /* Regole per Mobile (Cellulare) */
    @media (max-width: 768px) {{
        .header-image {{ height: 80px !important; }}
        .header-title-bar {{ font-size: 1rem !important; padding: 8px !important; }}
        .article-box {{ padding: 15px !important; }}
    }}

    .icon-title-container {{ display: flex; align-items: center; gap: 12px; margin-top: 25px; margin-bottom: 10px; }}
    .icon-img {{ width: 25px; height: 25px; object-fit: contain; }}
    .icon-text {{ font-weight: bold; color: #1A2E44; font-family: 'serif'; font-size: 1rem; }}
    .resource-link {{ text-decoration: none; color: #1A2E44 !important; font-weight: bold; display: block; padding: 8px 0; border-bottom: 1px solid #eee; }}
    
    #MainMenu, footer, header {{ visibility: hidden; }}
    </style>

    <div class="header-container">
        <div class="header-image"></div>
        <div class="header-title-bar">S O R G E N T E &nbsp; Y O G A</div>
    </div>
"""

st.markdown(css_code, unsafe_allow_html=True)

# --- LOGICA DI NAVIGAZIONE ---
if 'admin' not in st.session_state: st.session_state['admin'] = False
if 'articolo_selezionato' not in st.session_state: st.session_state['articolo_selezionato'] = None

tutti_gli_articoli = carica_articoli()

# --- LAYOUT A COLONNE ---
col_main, col_nav = st.columns([0.7, 0.3], gap="large")

with col_main:
    # AREA ACCESSO
    if not st.session_state['admin']:
        with st.expander("🔑 Area Autore"):
            pwd = st.text_input("Password", type="password")
            if pwd == "sorgente2026":
                st.session_state['admin'] = True
                st.rerun()
    
    # AREA EDITORE (BACKUP E SCRITTURA)
    if st.session_state['admin']:
        st.info("✍️ MODALITÀ EDITORE")
        
        if tutti_gli_articoli:
            json_string = json.dumps(tutti_gli_articoli, ensure_ascii=False, indent=4)
            st.download_button(
                label="📥 SCARICA BACKUP ARTICOLI",
                data=json_string,
                file_name=f"backup_yoga_{datetime.now().strftime('%d_%m_%Y')}.json",
                mime="application/json",
            )
            st.divider()

        with st.expander("📝 SCRIVI NUOVO ARTICOLO"):
            tit_n = st.text_input("Titolo nuovo")
            tes_n = st.text_area("Testo nuovo", height=250)
            if st.button("🚀 Pubblica"):
                if tit_n and tes_n:
                    aggiungi_articolo({"data": datetime.now().strftime("%d/%m/%Y"), "titolo": tit_n, "testo": tes_n})
                    st.rerun()

        with st.expander("✏️ MODIFICA ARTICOLO ESISTENTE"):
            if tutti_gli_articoli:
                nomi = [a['titolo'] for a in tutti_gli_articoli]
                scelta = st.selectbox("Seleziona articolo", nomi)
                idx = nomi.index(scelta)
                edit_tit = st.text_input("Titolo attuale", tutti_gli_articoli[idx]['titolo'])
                edit_tes = st.text_area("Testo attuale", tutti_gli_articoli[idx]['testo'], height=300)
                if st.button("💾 Salva Modifiche"):
                    tutti_gli_articoli[idx]['titolo'] = edit_tit
                    tutti_gli_articoli[idx]['testo'] = edit_tes
                    salva_tutti_articoli(tutti_gli_articoli)
                    st.success("Aggiornato con successo!")
                    st.rerun()

        if st.button("🔒 Esci"):
            st.session_state['admin'] = False
            st.rerun()

    # VISUALIZZAZIONE ARTICOLO
    art = st.session_state['articolo_selezionato'] if st.session_state['articolo_selezionato'] else (tutti_gli_articoli[0] if tutti_gli_articoli else None)
    if art:
        testo_html = art['testo'].replace('\n', '<br>')
        st.markdown(f"""
        <div class="article-box">
            <h1 style='font-family:serif; color:#1A2E44; margin-top:0; margin-bottom:10px;'>{art['titolo']}</h1>
            <p style='font-style:italic; color:#C5A059; margin-bottom:30px;'>{art['data']} • Luca Valenti</p>
            <div style="font-family:serif; font-size:1.2rem; line-height:1.7; color:#1A2E44
