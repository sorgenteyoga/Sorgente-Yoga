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
    return None

# Funzione per caricare gli articoli salvati
def carica_articoli():
    if os.path.exists("archivio_articoli.json"):
        with open("archivio_articoli.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Funzione per salvare un nuovo articolo
def salva_articolo(nuovo_articolo):
    articoli = carica_articoli()
    # Aggiungiamo l'articolo in cima alla lista
    articoli.insert(0, nuovo_articolo)
    with open("archivio_articoli.json", "w", encoding="utf-8") as f:
        json.dump(articoli, f, ensure_ascii=False, indent=4)

# Carichiamo l'immagine dell'header
img_base64 = get_base64_image("header_yoga.png")

# --- DESIGN ESTETICO ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #FDFCF0; }}
    .header-container {{ width: 100%; background-color: white; border-bottom: 3px solid #C5A059; margin-bottom: 30px; }}
    .header-image {{ width: 100%; height: 250px; background-image: url('data:image/png;base64,{img_base64 if img_base64 else ""}'); background-size: cover; background-position: center; }}
    .header-title-bar {{ background-color: #1A2E44; padding: 15px; color: #FDFCF0; font-family: 'serif'; font-size: 1.8rem; letter-spacing: 3px; text-align: center; }}
    .article-box {{ background-color: white; padding: 40px; border-radius: 5px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-top: 20px; min-height: 400px; }}
    h1 {{ font-family: 'serif'; color: #1A2E44; font-size: 2.8rem; margin-bottom: 5px; }}
    .author-sub {{ font-style: italic; color: #C5A059; font-size: 1.1rem; margin-bottom: 30px; }}
    .article-content {{ font-family: 'serif'; font-size: 1.3rem; line-height: 1.8; color: #2D2D2D; white-space: pre-wrap; }}
    .resource-link {{ text-decoration: none; color: #1A2E44 !important; font-weight: bold; display: block; padding: 8px 0; }}
    .history-item {{ padding: 10px; border-bottom: 1px solid #eee; cursor: pointer; color: #1A2E44; }}
    .history-item:hover {{ background-color: #f9f9f9; }}
    </style>
    
    <div class="header-container">
        <div class="header-image"></div>
        <div class="header-title-bar">S O R G E N T E &nbsp; Y O G A</div>
    </div>
    """, unsafe_allow_html=True)

# --- INIZIALIZZAZIONE STATO ---
if 'admin' not in st.session_state: st.session_state['admin'] = False
if 'articolo_selezionato' not in st.session_state: st.session_state['articolo_selezionato'] = None

# Carichiamo tutti gli articoli dal file
tutti_gli_articoli = carica_articoli()

col_main, col_nav = st.columns([0.7, 0.3], gap="large")

with col_main:
    # --- ACCESSO E EDITOR ---
    if not st.session_state['admin']:
        with st.expander("🔑 Area Riservata"):
            pwd = st.text_input("Password", type="password")
            if pwd == "sorgente2026":
                st.session_state['admin'] = True
                st.rerun()
    
    if st.session_state['admin']:
        st.markdown("### ✍️ Nuovo Articolo")
        titolo_nuovo = st.text_input("Titolo dell'articolo")
        testo_nuovo = st.text_area("Testo dell'articolo", height=300)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Pubblica e Salva nell'Archivio"):
                if titolo_nuovo and testo_nuovo:
                    nuovo_art = {
                        "data": datetime.now().strftime("%d/%m/%Y"),
                        "titolo": titolo_nuovo,
                        "testo": testo_nuovo
                    }
                    salva_articolo(nuovo_art)
                    st.success("Articolo salvato correttamente!")
                    st.rerun()
                else:
                    st.warning("Inserisci sia il titolo che il testo.")
        with c2:
            if st.button("Esci (Logout)"):
                st.session_state['admin'] = False
                st.rerun()

    # --- VISUALIZZAZIONE ARTICOLO ---
    # Se l'utente ha cliccato su un articolo vecchio, mostra quello, altrimenti mostra l'ultimo inserito
    if st.session_state['articolo_selezionato']:
        art_da_mostrare = st.session_state['articolo_selezionato']
    elif tutti_gli_articoli:
        art_da_mostrare = tutti_gli_articoli[0]
    else:
        art_da_mostrare = {"titolo": "Benvenuti su Sorgente Yoga", "data": "", "testo": "L'archivio è vuoto. Inizia a scrivere il tuo primo articolo."}

    st.markdown(f"""
    <div class="article-box">
        <h1>{art_da_mostrare['titolo']}</h1>
        <div class="author-sub">Pubblicato il {art_da_mostrare['data']} • Ricerca a cura di Luca Valenti</div>
        <div class="article-content">{art_da_mostrare['testo']}</div>
    </div>
    """, unsafe_allow_html=True)

with col_nav:
    # --- ARCHIVIO ARTICOLI ---
    st.markdown("### 📚 ARCHIVIO BLOG")
    if tutti_gli_articoli:
        for i, art in enumerate(tutti_gli_articoli):
            if st.button(f"📄 {art['titolo']}", key=f"art_{i}"):
                st.session_state['articolo_selezionato'] = art
                st.rerun()
    else:
        st.write("Nessun articolo presente.")

    st.markdown("---")
    st.markdown("### 🏛️ BIBLIOTECA")
    with st.expander("📖 TESTI CLASSICI"):
        st.write("• Yoga Sūtra")
        st.write("• Haṭha Yoga Pradīpikā")

    with st.expander("📜 RICERCA STORICA", expanded=True):
        st.markdown('<a class="resource-link" href="http://hyp.soas.ac.uk/" target="_blank">Hatha Yoga Project ↗</a>', unsafe_allow_html=True)
