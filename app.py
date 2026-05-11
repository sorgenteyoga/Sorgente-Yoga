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

# --- CSS AGGIORNATO CON MARGINI DI SICUREZZA ---
st.markdown(f"""
    <style>
    /* Spazio standard in cima alla pagina */
    .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 95%;
    }}
    
    .stApp {{ background-color: #FDFCF0; }}
    
    /* Header Container con sfondo bianco */
    .header-container {{ 
        width: 100%; 
        background-color: white; 
        border-bottom: 3px solid #C5A059; 
        margin-bottom: 25px; 
    }}
    
    /* Immagine Header rimpicciolita e con CUSCINETTO DI SICUREZZA (Padding) */
    .header-image {{ 
        width: 100%; 
        height: 180px; /* RIDOTTA per essere più sottile ed elegante */
        background-image: url('data:image/png;base64,{img_header}'); 
        background-size: contain; /* MOSTRA L'IMMAGINE INTERA */
        background-repeat: no-repeat;
        background-position: center; 
        background-color: white;
        
        /* AGGIUNTO PADDING INTERNO: crea spazio bianco intorno all'immagine */
        /* così i margini non appariranno mai tagliati */
        box-sizing: border-box;
        padding: 15px; /* 15 pixel di respiro su tutti i lati */
    }}
    
    .header-title-bar {{ 
        background-color: #1A2E44; 
        padding: 12px; 
        color: #FDFCF0; 
        font-family: 'serif'; 
        font-size: 1.7rem; 
        letter-spacing: 3px; 
        text-align: center; 
    }}
    
    .article-box {{ background-color: white; padding: 40px; border-radius: 5px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-top: 10px; min-height: 300px; }}
    .icon-title-container {{ display: flex; align-items: center; gap: 12px; margin-top: 25px; margin-bottom: 10px; }}
    .icon-img {{ width: 30px; height: 30px; object-fit: contain; }}
    .icon-text {{ font-weight: bold; color: #1A2E44; font-family: 'serif'; font-size: 1.1rem; letter-spacing: 1px;}}
    .resource-link {{ text-decoration: none; color: #1A2E44 !important; font-weight: bold; display: block; padding: 8px 0; border-bottom: 1px solid #eee; }}
    
    #MainMenu, footer, header {{visibility: hidden;}}
    </style>
    
    <div class="header-container">
        <div class="header-image"></div>
        <div class="header-title-bar">S O R G E N T E &nbsp; Y O G A</div>
    </div>
    """, unsafe_allow_html=True)

# --- LOGICA DI SESSIONE ---
if 'admin' not in st.session_state: st.session_state['admin'] = False
if 'articolo_selezionato' not in st.session_state: st.session_state['articolo_selezionato'] = None

tutti_gli_articoli = carica_articoli()

col_main, col_nav = st.columns([0.7, 0.3], gap="large")

with col_main:
    # AREA ACCESSO
    if not st.session_state['admin']:
        with st.expander("🔑 Area Autore"):
            pwd = st.text_input("Password", type="password")
            if pwd == "sorgente2026":
                st.session_state['admin'] = True
                st.rerun()
    
    # AREA EDITORE
    if st.session_state['admin']:
        st.info("✍️ MODALITÀ EDITORE")
        with st.expander("📝 SCRIVI NUOVO ARTICOLO", expanded=True):
            tit_n = st.text_input("Titolo")
            tes_n = st.text_area("Testo", height=300)
            if st.button("🚀 Pubblica Articolo"):
                if tit_n and tes_n:
                    aggiungi_articolo({"data": datetime.now().strftime("%d/%m/%Y"), "titolo": tit_n, "testo": tes_n})
                    st.success("Articolo pubblicato!")
                    st.rerun()

        with st.expander("🗑️ GESTIONE ARCHIVIO"):
            if tutti_gli_articoli:
                for idx, a in enumerate(tutti_gli_articoli):
                    c_tit, c_del = st.columns([0.8, 0.2])
                    c_tit.write(f"**{a['titolo']}** ({a['data']})")
                    if c_del.button("Elimina", key=f"del_{idx}"):
                        nuova_lista = [art for i, art in enumerate(tutti_gli_articoli) if i != idx]
                        salva_tutti_articoli(nuova_lista)
                        st.session_state['articolo_selezionato'] = None
                        st.rerun()

        if st.button("🔒 Esci dalla modalità editore"):
            st.session_state['admin'] = False
            st.rerun()

    # VISUALIZZAZIONE ARTICOLO
    art = st.session_state['articolo_selezionato'] if st.session_state['articolo_selezionato'] else (tutti_gli_articoli[0] if tutti_gli_articoli else None)
    if art:
        st.markdown(f"""
        <div class="article-box">
            <h1 style='font-family:serif; color:#1A2E44; margin-top:0;'>{art['titolo']}</h1>
            <p style='font-style:italic; color:#C5A059;'>{art['data']} • Luca Valenti</p>
            <div style='font-family:serif; font-size:1.3rem; line-height:1.8; white-space: pre-wrap;'>{art['testo']}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.write("Benvenuti su Sorgente Yoga. Accedi per iniziare a pubblicare.")

with col_nav:
    st.markdown("### 🏛️ BIBLIOTECA")
    
    # ARCHIVIO
    st.markdown(f'<div class="icon-title-container"><img src="data:image/png;base64,{icon_archivio}" class="icon-img"><span class="icon-text">ARCHIVIO BLOG</span></div>', unsafe_allow_html=True)
    with st.expander("Sfoglia articoli", expanded=True):
        if tutti_gli_articoli:
            for i, a in enumerate(tutti_gli_articoli):
                if st.button(f"📄 {a['titolo']}", key=f"nav_{i}"):
                    st.session_state['articolo_selezionato'] = a
                    st.rerun()
        else: st.caption("Vuoto.")

    # TESTI CLASSICI
    st.markdown(f'<div class="icon-title-container"><img src="data:image/png;base64,{icon_testi}" class="icon-img"><span class="icon-text">TESTI CLASSICI</span></div>', unsafe_allow_html=True)
    with st.expander("Elenco testi"):
        st.write("• Yoga Sūtra (Patañjali)")
        st.write("• Haṭha Yoga Pradīpikā")
        st.write("• Gheraṇḍa Saṃhitā")
        st.write("• Bhagavad Gītā")

    # RICERCA STORICA
    st.markdown(f'<div class="icon-title-container"><img src="data:image/png;base64,{icon_storia}" class="icon-img"><span class="icon-text">RICERCA STORICA</span></div>', unsafe_allow_html=True)
    with st.expander("Siti e Progetti"):
        st.markdown('<a class="resource-link" href="http://hyp.soas.ac.uk/" target="_blank">Hatha Yoga Project ↗</a>', unsafe_allow_html=True)
        st.markdown('<a class="resource-link" href="https://journalofyogastudies.org/index.php/JoYS/issue/archive" target="_blank">Journal of Yoga Studies ↗</a>', unsafe_allow_html=True)

    # SCIENZA
    st.markdown(f'<div class="icon-title-container"><img src="data:image/png;base64,{icon_scienza}" class="icon-img"><span class="icon-text">SCIENZA</span></div>', unsafe_allow_html=True)
    with st.expander("Istituti e Ricerche"):
        st.markdown('<a class="resource-link" href="https://sleep.hms.harvard.edu/faculty-staff/sat-bir-singh-khalsa" target="_blank">Harvard (Dr. Khalsa) ↗</a>', unsafe_allow_html=True)
        st.markdown('<a class="resource-link" href="https://www.iayt.org/" target="_blank">IAYT Yoga Therapy ↗</a>', unsafe_allow_html=True)
        st.markdown('<a class="resource-link" href="https://www.kym.org/" target="_blank">KYM Tradition ↗</a>', unsafe_allow_html=True)
